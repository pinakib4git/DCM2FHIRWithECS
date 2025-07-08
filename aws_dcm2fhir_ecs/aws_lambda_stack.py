from aws_cdk import (
    Stack,
    NestedStack,
    aws_lambda as lambda_,
    aws_iam as iam,
    Duration,
    CfnOutput
)
from constructs import Construct
import os

class LambdaIAMStack(NestedStack):
    def __init__(self, scope: Construct, id: str, healthlake_datastore_id=None, healthlake_datastore_arn=None,kms_key=None, resource_prefix: str = None, s3fhiroutputbucketname=None, dicominputbucketname = None, dicomoutputbucketname = None, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        resource_prefix = resource_prefix or "test-100"
        # Create IAM Role with explicit name
        lambda_role = iam.Role(
            self, "LambdaExecutionRole",
            role_name= f"{resource_prefix}-TransformWSIAndManageConfig-Lambda-Role",
            assumed_by=iam.ServicePrincipal("lambda.amazonaws.com"),
            description="Role for Lambda accessing S3, Health Imaging, and HealthLake"
        )

        # Add managed policies
        lambda_role.add_managed_policy(
            iam.ManagedPolicy.from_aws_managed_policy_name("AmazonS3FullAccess")
        )
        lambda_role.add_managed_policy(
            iam.ManagedPolicy.from_aws_managed_policy_name("AWSHealthImagingFullAccess")
        )
        lambda_role.add_managed_policy(
            iam.ManagedPolicy.from_aws_managed_policy_name("AmazonHealthLakeFullAccess")
        )
        lambda_role.add_managed_policy(
            iam.ManagedPolicy.from_aws_managed_policy_name("AWSLambda_FullAccess")
        )
        lambda_role.add_managed_policy(
            iam.ManagedPolicy.from_aws_managed_policy_name("AWSStepFunctionsFullAccess")
        )

        # Get the current directory path
        current_dir = os.path.dirname(__file__)
        
        # Set the file path for the .py file from the directory path
        lambda1_zip_path = os.path.join(
            current_dir,
            "lambda_manageconfig",
            "ManageConfig.zip"
        )

        # Create Lambda function1 from local code
        my_lambda1 = lambda_.Function(
            self, "MyLambdaFunctionToManageConfig",
            function_name= f"{resource_prefix}-ManageConfig4DICOMToFHIRConversionProcess",
            runtime=lambda_.Runtime("python3.12"),
            handler="ManageConfig.lambda_handler",
            code=lambda_.Code.from_asset(lambda1_zip_path),  # Direct path to zip file
            role=lambda_role,
            timeout=Duration.seconds(300),
            environment={
                "HEALTHLAKE_DATASTORE_ID": healthlake_datastore_id or "",
                "KMS_KEY_ID": kms_key if kms_key else "",
                "JobProcessingIAMRole": lambda_role.role_arn,
                "HEALTHLAKE_DATASTORE_ARN": healthlake_datastore_arn or "",
                "S3_FHIROutPutBucketName" : s3fhiroutputbucketname or "",
                "DICOM_InputBucketName" : dicominputbucketname or "",
                "DICOM_OutputBucketName" : dicomoutputbucketname or ""
            }
        )

        # Output the Lambda-1 ARN
        CfnOutput(self, "LambdaArn1", value=my_lambda1.function_arn)

        # Lambda 2 Configuration - Direct reference to zip file
        lambda2_zip_path = os.path.join(
            current_dir,
            "lambda_wsitransform",
            "WSITransform.zip"
        )

        # Create Lambda function2 from local code
        my_lambda2 = lambda_.Function(
            self, "MyLambdaFunctionToTransform",
            function_name= f"{resource_prefix}-ProcessDICOMFilesConvertFHIR",
            runtime=lambda_.Runtime("python3.12"),
            handler="WSITransform.lambda_handler",
            code=lambda_.Code.from_asset(lambda2_zip_path),  # Direct path to zip file
            #code = lambda_.Code.from_asset("/Users/bpinaki/Documents/HCLS/TFC/aws-dcm2fhir-project/aws_dcm2fhir_project/lambda_wsitransform"),
            role=lambda_role,
            timeout=Duration.seconds(300),
            environment={
                "ENV_VAR": "production"
            }
        )

        # Output the Lambda-2 ARN
        CfnOutput(self, "LambdaArn2", value=my_lambda2.function_arn)

        # Lambda 3 Configuration - Direct reference to zip file
        lambda3_zip_path = os.path.join(
            current_dir,
            "lambda_convertndjson",
            "convert2ndjson.zip"
        )

        # Create Lambda function3 from local code
        my_lambda3 = lambda_.Function(
            self, "convertFHIRtoNDJSON",
            function_name= f"{resource_prefix}-convertFHIRtoNDJSON",
            runtime=lambda_.Runtime("python3.12"),
            handler="convert2ndjson.lambda_handler",
            code=lambda_.Code.from_asset(lambda3_zip_path),  # Direct path to zip file 
            #code = lambda_.Code.from_asset("/Users/bpinaki/Documents/HCLS/TFC/aws-dcm2fhir-project/aws_dcm2fhir_project/lambda_convertndjson"),
            role=lambda_role,
            timeout=Duration.seconds(300),
            environment={
                "ENV_VAR": "production"
            }
        )

        # Output the Lambda-3 ARN
        CfnOutput(self, "LambdaArn3", value=my_lambda3.function_arn)
        #Add the cfnout for all the above resources created
        CfnOutput(self, "LambdaRoleName", value=lambda_role.role_name)
        CfnOutput(self, "LambdaRoleArn", value=lambda_role.role_arn)
        CfnOutput(self, "Lambda1Name", value=my_lambda1.function_name)
        CfnOutput(self, "Lambda2Name", value=my_lambda2.function_name)
        CfnOutput(self, "Lambda3Name", value=my_lambda3.function_name)
        
        # Expose Lambda function names as properties for other stacks to reference
        self.lambda_manage_config_name = my_lambda1.function_name
        self.lambda_transform_name = my_lambda2.function_name
        self.lambda_convert_ndjson_name = my_lambda3.function_name
