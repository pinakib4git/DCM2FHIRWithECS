import os
from aws_cdk import App, Environment
from aws_dcm2fhir_ecs.master_stack import MasterStack

app = App()

# Define your environment
env = Environment(
    account="241003932265",
    region="us-east-1"
)

# Use a unique environment name to avoid conflicts with the failed stack
environment_var = "uat"  # Changed from test1 to test2

# Create the master stack with the environment and a different stack name
# to avoid conflict with the failed stack
master_stack = MasterStack(app, "FHIRWithECS-MasterStack-PRD", environment=environment_var)
app.synth()