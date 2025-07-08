from aws_cdk import (
    NestedStack,
    Stack,
    aws_events as events,
    aws_events_targets as targets,
    aws_s3 as s3,
    aws_stepfunctions as sfn,
    aws_iam as iam,
    Environment,
    RemovalPolicy,
    CfnOutput
)
from constructs import Construct

# EventBridge Stack - receives Step Function stack as input
class EventBridgeStack(NestedStack):
    def __init__(self, scope: Construct, construct_id: str, processing_workflow: None, 
                 source_bucket_name: str, source_bucket: None, env: Environment, resource_prefix: str = None, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Create an S3 bucket
        self.bucket = source_bucket

        # Reference the state machine from the input stack
        state_machine = processing_workflow

        # Create IAM role for EventBridge to invoke Step Function
        eventbridge_role = iam.Role(
            self, 
            f"{resource_prefix}-EventBridgeInvokeStepFunctionRole",
            assumed_by=iam.ServicePrincipal("events.amazonaws.com"),
            description=f"{resource_prefix}-Role for EventBridge to invoke Step Function"
        )
        
        # 3. Attach Step Functions Full Access policy (managed policy)
        eventbridge_role.add_managed_policy(
            iam.ManagedPolicy.from_aws_managed_policy_name("AWSStepFunctionsFullAccess")
        )
        eventbridge_role.add_managed_policy(
            iam.ManagedPolicy.from_aws_managed_policy_name("AmazonS3FullAccess")
        )
        eventbridge_role.add_managed_policy(
            iam.ManagedPolicy.from_aws_managed_policy_name("AWSHealthImagingFullAccess")
        )
        eventbridge_role.add_managed_policy(
            iam.ManagedPolicy.from_aws_managed_policy_name("AmazonHealthLakeFullAccess")
        )
        eventbridge_role.add_managed_policy(
            iam.ManagedPolicy.from_aws_managed_policy_name("AWSLambda_FullAccess")
        )
        eventbridge_role.add_managed_policy(
            iam.ManagedPolicy.from_aws_managed_policy_name("AWSStepFunctionsFullAccess")
        )

        # Add explicit permission to start Step Function execution
        eventbridge_role.add_to_policy(
            iam.PolicyStatement(
                actions=["states:StartExecution"],
                resources=[state_machine.state_machine_arn],
                effect=iam.Effect.ALLOW
            )
        )

        # Create EventBridge rule to capture S3 object creation events
        rule = events.Rule(
            self, 
            "S3ObjectCreatedRule",
            event_pattern=events.EventPattern(
                source=["aws.s3"],
                detail_type=["Object Created"],
                detail={
                    "bucket": {
                        "name": [source_bucket_name]
                    },
                    "object": {
                        "key": [{
                            "prefix": "inputfile/"
                        }]
                    }
                }
            ),
            description="Rule to capture S3 object creation events in inputfile folder"
        )

        # Add Step Function as target for the EventBridge rule
        rule.add_target(
            targets.SfnStateMachine(
                machine=state_machine,
                role=eventbridge_role,
                input=events.RuleTargetInput.from_event_path("$")  # Pass the entire event
            )
        )

        #Add the cfnout for all the above resources created
        CfnOutput(self, "EventBridgeRuleName", value=rule.rule_name)
        CfnOutput(self, "EventBridgeRoleName", value=eventbridge_role.role_name)
        CfnOutput(self, "EventBridgeRoleArn", value=eventbridge_role.role_arn)
        CfnOutput(self, "EventBridgeRuleArn", value=rule.rule_arn)