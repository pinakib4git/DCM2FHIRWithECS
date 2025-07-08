from aws_cdk import (
    App,
    Stack,
    NestedStack,
    aws_stepfunctions as sfn,
    aws_iam as iam,
    aws_s3_assets as s3_assets,
    CfnOutput
)
from constructs import Construct
import json
import os
import uuid

class StepFunctionStack(NestedStack):
    def __init__(self, scope: Construct, id: str, resource_prefix: str = None, 
                 lambda_manage_config_name: str = None, lambda_transform_name: str = None, 
                 lambda_convert_ndjson_name: str = None, healthlake_datastore_id: str = None,
                 cluster_arn: str = None, task_definition_arn: str = None, **kwargs) -> None:
        # Remove custom parameters from kwargs before passing to parent
        filtered_kwargs = {k: v for k, v in kwargs.items() if k not in ['resource_prefix', 'lambda_manage_config_name', 'lambda_transform_name', 'lambda_convert_ndjson_name', 'healthlake_datastore_id', 'cluster_arn', 'task_definition_arn']}
        super().__init__(scope, id, **filtered_kwargs)
        
        # Create IAM Role with dynamic name for Step Function
        step_function_role = iam.Role(
            self, "StepFunctionExecutionRole",
            role_name=f"{resource_prefix}-StepFunctionRole",
            assumed_by=iam.ServicePrincipal("states.amazonaws.com"),
            description="Role for Step Function accessing S3, Health Imaging, and HealthLake"
        )

        # Attach required managed policies
        step_function_role.add_managed_policy(
            iam.ManagedPolicy.from_aws_managed_policy_name("AmazonS3FullAccess")
        )
        step_function_role.add_managed_policy(
            iam.ManagedPolicy.from_aws_managed_policy_name("AWSHealthImagingFullAccess")
        )
        step_function_role.add_managed_policy(
            iam.ManagedPolicy.from_aws_managed_policy_name("AmazonHealthLakeFullAccess")
        )
        step_function_role.add_managed_policy(
            iam.ManagedPolicy.from_aws_managed_policy_name("AWSLambda_FullAccess")
        )
        step_function_role.add_managed_policy(
            iam.ManagedPolicy.from_aws_managed_policy_name("AmazonECS_FullAccess")
        )

        # Get the path to the stepfunction_ecs.json file using relative path
        stepfunction_path = os.path.join(os.path.dirname(__file__), "stepfunction_ecs.json")
        
        # Create an asset from your existing Step Functions JSON file
        state_machine_json = s3_assets.Asset(
            self, 
            "StateMachineJson", 
            path=stepfunction_path
        )

        # Load and modify the Step Functions definition with dynamic parameters
        with open(stepfunction_path, "r") as f:
            definition_json = json.load(f)
        
        # Replace Lambda function names and ECS resources in the definition
        definition_str = json.dumps(definition_json)
        if lambda_manage_config_name:
            definition_str = definition_str.replace(
                "arn:aws:lambda:us-east-1:229055855186:function:ManageConfig4DICOMToFHIRConversionProcess:$LATEST",
                f"arn:aws:lambda:{self.region}:{self.account}:function:{lambda_manage_config_name}:$LATEST"
            )
        if lambda_convert_ndjson_name:
            definition_str = definition_str.replace(
                "arn:aws:lambda:us-east-1:229055855186:function:convertFHIRtoNDJSON:$LATEST",
                f"arn:aws:lambda:{self.region}:{self.account}:function:{lambda_convert_ndjson_name}:$LATEST"
            )
        if cluster_arn:
            definition_str = definition_str.replace(
                "CLUSTER_ARN_PLACEHOLDER",
                cluster_arn
            )
        if task_definition_arn:
            definition_str = definition_str.replace(
                "TASK_DEFINITION_ARN_PLACEHOLDER",
                task_definition_arn
            )
        
        # Create the Step Function using the high-level construct with dynamic name
        self.state_machine = sfn.StateMachine(
            self, "MyHealthStateMachine",
            state_machine_name=f"{resource_prefix}-ProcessDICOMFilesConvertFHIR",
            definition_body=sfn.DefinitionBody.from_string(definition_str),
            role=step_function_role,
            state_machine_type=sfn.StateMachineType.STANDARD
        )

        # Output the state machine ARN
        CfnOutput(self, "StateMachineARN", value=self.state_machine.state_machine_arn)
        CfnOutput(self, "StateMachineName", value=self.state_machine.state_machine_name)

        #Add the cfnout for all the above resources created
        CfnOutput(self, "StepFunctionRoleName", value=step_function_role.role_name)
        CfnOutput(self, "StepFunctionRoleArn", value=step_function_role.role_arn)

