from aws_cdk import (
    NestedStack,
    aws_ecs as ecs,
    aws_ecr as ecr,
    aws_iam as iam,
    aws_logs as logs,
    CfnOutput,
    RemovalPolicy
)
from constructs import Construct
import os

class ECSStack(NestedStack):
    def __init__(self, scope: Construct, id: str, resource_prefix: str = None, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)
        
        resource_prefix = resource_prefix or "dcm2fhir"
        
        # Create ECR repository for WSI Transform container
        self.ecr_repository = ecr.Repository(
            self, "WSITransformRepository",
            repository_name=f"{resource_prefix}-wsi-transform",
            removal_policy=RemovalPolicy.DESTROY,
            image_scan_on_push=True
        )
        
        # Create ECS cluster
        self.ecs_cluster = ecs.Cluster(
            self, "WSIProcessingCluster",
            cluster_name=f"{resource_prefix}-wsi-cluster"
        )
        
        # Create task execution role
        self.task_execution_role = iam.Role(
            self, "WSITaskExecutionRole",
            role_name=f"{resource_prefix}-wsi-task-execution-role",
            assumed_by=iam.ServicePrincipal("ecs-tasks.amazonaws.com"),
            managed_policies=[
                iam.ManagedPolicy.from_aws_managed_policy_name("service-role/AmazonECSTaskExecutionRolePolicy")
            ]
        )
        
        # Create task role with S3 permissions
        self.task_role = iam.Role(
            self, "WSITaskRole",
            role_name=f"{resource_prefix}-wsi-task-role",
            assumed_by=iam.ServicePrincipal("ecs-tasks.amazonaws.com"),
            managed_policies=[
                iam.ManagedPolicy.from_aws_managed_policy_name("AmazonS3FullAccess")
            ]
        )
        
        # Create CloudWatch log group
        self.log_group = logs.LogGroup(
            self, "WSITaskLogGroup",
            log_group_name=f"/ecs/{resource_prefix}-wsi-transform",
            removal_policy=RemovalPolicy.DESTROY
        )
        
        # Create ECS task definition
        self.task_definition = ecs.FargateTaskDefinition(
            self, "WSITaskDefinition",
            family=f"{resource_prefix}-wsi-transform-task",
            cpu=1024,
            memory_limit_mib=2048,
            execution_role=self.task_execution_role,
            task_role=self.task_role
        )
        
        # Add container to task definition
        self.container = self.task_definition.add_container(
            "WSITransformContainer",
            image=ecs.ContainerImage.from_ecr_repository(self.ecr_repository, "latest"),
            logging=ecs.LogDrivers.aws_logs(
                stream_prefix="wsi-transform",
                log_group=self.log_group
            ),
            environment={
                "AWS_DEFAULT_REGION": self.region
            }
        )
        
        # Outputs
        CfnOutput(self, "ECRRepositoryURI", value=self.ecr_repository.repository_uri)
        CfnOutput(self, "ECSClusterName", value=self.ecs_cluster.cluster_name)
        CfnOutput(self, "TaskDefinitionArn", value=self.task_definition.task_definition_arn)
        CfnOutput(self, "TaskExecutionRoleArn", value=self.task_execution_role.role_arn)
        CfnOutput(self, "TaskRoleArn", value=self.task_role.role_arn)
        
        # Expose properties for other stacks
        self.cluster_arn = self.ecs_cluster.cluster_arn
        self.task_definition_arn = self.task_definition.task_definition_arn