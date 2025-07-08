from aws_cdk import (
    Stack,
    aws_cloudformation as cfn
)
from constructs import Construct
from .aws_s3event_bucket_stack import S3BucketStackEvent
from .aws_stepfunction_stack import StepFunctionStack
from .aws_eventbridge_new_stack import EventBridgeStack
from .aws_lambda_stack import LambdaIAMStack
from .aws_kmskey_stack import KMSKeyStack
from .aws_healthlake_stack import HealthLakeStack
from .aws_s3_stack import S3BucketStack
from .aws_ecs_stack import ECSStack
import json
import os
import uuid

class MasterStack(Stack):
    def __init__(self, scope: Construct, id: str, environment: str = None, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)
        # Get environment from context or use default
        env = environment or "dev"
        
        # Create a unique identifier for resources based on stack ID
        # This ensures resources have unique names across deployments
        stack_name = Stack.of(self).stack_name
        
        # Use provided suffix or generate a short unique identifier (first 3 chars of a UUID)
        unique_id = str(uuid.uuid4())[:3]
        
        # Create resource prefix with environment, stack name and unique ID
        resource_prefix_var = f"{env}-{unique_id}"

        # Create KMS stack first (if other stacks depend on it)
        kms_stack = KMSKeyStack(self, "KMSStack", resource_prefix=resource_prefix_var)

        # Create the S3 bucket which leads the Eventbridge Rule
        s3_event = S3BucketStackEvent(self, "S3BucketEventStack", resource_prefix=resource_prefix_var)

        # Create S3 bucket stack
        s3_stack = S3BucketStack(self, "S3BucketStack", resource_prefix=resource_prefix_var)

        # Create the HealthLake stack
        healthlake_stack = HealthLakeStack(self, "HealthLakeStack" , resource_prefix=resource_prefix_var)
        
        # Create ECS stack for WSI Transform
        ecs_stack = ECSStack(
            self,
            "ECSStack",
            resource_prefix=resource_prefix_var
        )
        
        # Create Lambda stack
        lambda_stack = LambdaIAMStack(
            self, 
            "LambdaIAMStack",
            healthlake_datastore_id=healthlake_stack.healthlake_datastore_id,
            healthlake_datastore_arn=healthlake_stack.healthlake_datastore_arn,
            kms_key=kms_stack.kms_key,
            resource_prefix=resource_prefix_var,
            s3fhiroutputbucketname=s3_stack.fhir_outcome_bucket, 
            dicominputbucketname = s3_event.bucket_name, 
            dicomoutputbucketname = s3_stack.dicom_output_bucket
        )

        # Create Step Functions stack with Lambda function names, ECS resources and HealthLake datastore ID
        step_functions_stack = StepFunctionStack(
            self, 
            "StepFunctionsStack",
            resource_prefix=resource_prefix_var,
            lambda_manage_config_name=lambda_stack.lambda_manage_config_name,
            lambda_transform_name=lambda_stack.lambda_transform_name,
            lambda_convert_ndjson_name=lambda_stack.lambda_convert_ndjson_name,
            healthlake_datastore_id=healthlake_stack.healthlake_datastore_id,
            cluster_arn=ecs_stack.cluster_arn,
            task_definition_arn=ecs_stack.task_definition_arn
        )
        
        # Add explicit dependencies
        step_functions_stack.add_dependency(lambda_stack)
        step_functions_stack.add_dependency(healthlake_stack)
        step_functions_stack.add_dependency(ecs_stack)

        # Create EventBridge stack with dependencies from other stacks
        eventbridge_stack = EventBridgeStack(
            self, 
            "EventBridgeStack", 
            source_bucket=s3_event.event_bucket,
            source_bucket_name= s3_event.bucket_name,
            processing_workflow=step_functions_stack.state_machine,
            resource_prefix=resource_prefix_var,
            env=self.node.try_get_context("env")
        )
