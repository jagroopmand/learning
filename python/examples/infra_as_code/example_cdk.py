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

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # --- DataBucket (maps to AWS::S3::Bucket) ---
        data_bucket = s3.Bucket(
            self, "DataBucket",
            encryption=s3.BucketEncryption.S3_MANAGED,  # SSEAlgorithm: AES256
            versioned=True,                              # VersioningConfiguration: Enabled
        )

        # --- DataAccessRole (maps to AWS::IAM::Role) ---
        data_access_role = iam.Role(
            self, "DataAccessRole",
            assumed_by=iam.ServicePrincipal("ec2.amazonaws.com"),
        )

        # Maps to the inline "BucketReadWrite" policy in the CFN template:
        # s3:GetObject + s3:PutObject on ${DataBucket.Arn}/*
        # grant_read_write() generates this exact statement, scoped to the
        # bucket's object ARN pattern, without hand-writing the !Sub interpolation.
        data_bucket.grant_read_write(data_access_role)
