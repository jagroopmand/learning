from aws_cdk import (
    Stack,
    aws_s3 as s3,
    aws_iam as iam,
)
from constructs import Construct


class ExampleCdkStack(Stack):
    """
    CDK equivalent of example_cfn.yaml:
    - S3 bucket, encrypted (SSE-S3/AES256), versioned
    - IAM role assumable by EC2, granted read/write on the bucket
    """
    """

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # --- DataBucket (maps to AWS::S3::Bucket) ---
        data_bucket = s3.Bucket(
            self, "DataBucket",
            encryption=s3.BucketEncryption.S3_MANAGED,
            versioned=True,
        )

        # --- DataAccessRole (maps to AWS::IAM::Role) ---
        data_access_role = iam.Role(
            self, "DataAccessRole",
            assumed_by=iam.ServicePrincipal("ec2.amazonaws.com"),
        )

        # Exact match to the CFN inline policy: GetObject + PutObject only,
        # scoped to ${DataBucket.Arn}/* — no DeleteObject, no bucket-level
        # actions. bucket.grant() takes the raw IAM actions and builds the
        # correctly-scoped resource ARN(s) for you (object-level here,
        # since these are object actions).
        data_bucket.grant(
            data_access_role,
            "s3:GetObject",
            "s3:PutObject",
        )
