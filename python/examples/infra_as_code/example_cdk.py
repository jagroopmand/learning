# stacks/authz_service_stack.py
from aws_cdk import (
    Stack,
    Duration,
    RemovalPolicy,
    aws_dynamodb as dynamodb,
    aws_lambda as _lambda,
    aws_iam as iam,
    aws_apigateway as apigw,
)
from constructs import Construct


class AuthzServiceStack(Stack):
    """
    Policy decision service: API Gateway -> Lambda -> DynamoDB (policy store).
    Mirrors a real internal pattern: least-privilege IAM per resource,
    no wildcard actions, no wildcard resource ARNs.
    """

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # --- Policy store (DynamoDB) ---
        policy_table = dynamodb.Table(
            self, "PolicyTable",
            table_name="authz-policies",
            partition_key=dynamodb.Attribute(
                name="pk", type=dynamodb.AttributeType.STRING
            ),
            sort_key=dynamodb.Attribute(
                name="sk", type=dynamodb.AttributeType.STRING
            ),
            billing_mode=dynamodb.BillingMode.PAY_PER_REQUEST,
            point_in_time_recovery=True,
            removal_policy=RemovalPolicy.RETAIN,  # never auto-delete prod data
        )

        # --- Execution role: scoped to exactly what the function needs ---
        decision_role = iam.Role(
            self, "DecisionFunctionRole",
            assumed_by=iam.ServicePrincipal("lambda.amazonaws.com"),
            description="Least-privilege role for the PDP decision function",
        )

        # Grant only the specific actions on the specific table — CDK's
        # grant_read_data() generates a scoped policy automatically,
        # equivalent to hand-writing Resource: !GetAtt PolicyTable.Arn
        # in raw CloudFormation, but without risk of typoing the ARN.
        policy_table.grant_read_data(decision_role)

        decision_role.add_to_policy(
            iam.PolicyStatement(
                sid="AllowLogsOnly",
                effect=iam.Effect.ALLOW,
                actions=[
                    "logs:CreateLogGroup",
                    "logs:CreateLogStream",
                    "logs:PutLogEvents",
                ],
                resources=[f"arn:aws:logs:{self.region}:{self.account}:*"],
            )
        )

        # --- Lambda: the decision function itself ---
        decision_fn = _lambda.Function(
            self, "DecisionFunction",
            runtime=_lambda.Runtime.PYTHON_3_12,
            handler="handler.evaluate",
            code=_lambda.Code.from_asset("lambda/decision"),
            role=decision_role,
            timeout=Duration.seconds(3),
            memory_size=256,
            environment={
                "POLICY_TABLE_NAME": policy_table.table_name,
            },
        )

        # --- API Gateway front door ---
        api = apigw.LambdaRestApi(
            self, "AuthzApi",
            handler=decision_fn,
            proxy=False,
        )
        decisions = api.root.add_resource("decisions")
        decisions.add_method("POST")  # POST /decisions -> decision_fn