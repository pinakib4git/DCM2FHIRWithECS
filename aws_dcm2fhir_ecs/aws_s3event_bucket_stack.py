from aws_cdk import (
    NestedStack,
    aws_s3 as s3,
    aws_iam as iam,
    aws_s3_deployment as s3_deploy,
    RemovalPolicy,
    Duration,
    CfnOutput
)
from constructs import Construct
from random import randint
import random
import json
import os
import uuid

#generate the random number
random_number = randint(10, 99)

class S3BucketStackEvent(NestedStack):
    def __init__(self, scope: Construct, id: str, resource_prefix: str = None, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)
                
        
        empty_dir = os.path.join(os.path.dirname(__file__), "emptyfolder")
        # Create S3 bucket-2 with configuration matching your existing bucket
        self.event_bucket = s3.Bucket(
            self, "MyConfiguredevent_bucket",
            bucket_name= f"{resource_prefix}-new-dicom-image-lake",  # Remove for auto-generated name
            versioned=True,
            encryption=s3.BucketEncryption.S3_MANAGED,
            block_public_access=s3.BlockPublicAccess.BLOCK_ALL,
            removal_policy=RemovalPolicy.DESTROY,
            event_bridge_enabled=True
            )

        # Create each folder separately to avoid nested folder issues
        folders = ["inputfile", "HealthLake-Output-Import", "processed", "logs", "temp"]
        for i, folder in enumerate(folders):
            s3_deploy.BucketDeployment(
                self, f"CreateFolder{i}",
                destination_bucket=self.event_bucket,
                sources=[s3_deploy.Source.asset(empty_dir)],
                destination_key_prefix=f"{folder}/",
                retain_on_delete=False
            )

        # Set the S3-bucket name
        self.bucket_name = f"{resource_prefix}-new-dicom-image-lake"
        
        # Output important information
        CfnOutput(self, "BucketARN", value=self.event_bucket.bucket_arn)
        CfnOutput(self, "BucketURL", value=self.event_bucket.bucket_website_url)