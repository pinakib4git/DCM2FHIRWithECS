import aws_cdk as core
import aws_cdk.assertions as assertions

from aws_dcm2fhir_project.aws_dcm2fhir_project_stack import AwsDcm2FhirProjectStack

# example tests. To run these tests, uncomment this file along with the example
# resource in aws_dcm2fhir_project/aws_dcm2fhir_project_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = AwsDcm2FhirProjectStack(app, "aws-dcm2fhir-project")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
