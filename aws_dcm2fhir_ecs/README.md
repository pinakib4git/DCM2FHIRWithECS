# AWS DCM2FHIR Project

This project contains CDK code to deploy a Step Function workflow that processes DICOM files and converts them to FHIR format.

## Resource Naming Strategy

To avoid resource naming conflicts when deploying multiple instances of this stack, we use a combination of:

1. Environment name (from context or default "dev")
2. Stack name (from CDK)
3. Custom suffix or auto-generated UUID

### Example Usage

```python
# Create a Step Function stack with an explicit suffix
StepFunctionStack(self, "StepFunctionStack1", resource_suffix="team-a")

# Create another Step Function stack with a different suffix
StepFunctionStack(self, "StepFunctionStack2", resource_suffix="team-b")

# Create a Step Function stack with an auto-generated UUID suffix
StepFunctionStack(self, "StepFunctionStack3")
```

This ensures that each deployment gets unique resource names, even when deployed from the same CDK app.

## Deployment

To deploy with a specific environment:

```
cdk deploy -c env=prod
```

The default environment is "dev" if not specified.