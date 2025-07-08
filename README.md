# AWS DCM2FHIR Project

This project contains a CDK application that deploys infrastructure for converting DICOM files to FHIR format using AWS services.

## Architecture

The solution uses the following AWS services:
- Amazon S3 for storage
- AWS Lambda for processing
- AWS Step Functions for orchestration
- Amazon EventBridge for event handling
- AWS KMS for encryption
- Amazon HealthLake for FHIR data storage

## Prerequisites

- AWS CLI configured with appropriate credentials
- Node.js 14.x or later
- Python 3.9 or later
- AWS CDK Toolkit

## Installation

1. Clone the repository
2. Install dependencies:

```bash
pip install -r requirements.txt
```

## Deployment

To deploy the stack:

```bash
cdk deploy DCM2FHIRMasterStack-New
```

## Project Structure

- `aws_dcm2fhir_ecs/` - Main project code
  - `master_stack.py` - Main stack that creates all nested stacks
  - `aws_lambda_stack.py` - Lambda functions for processing
  - `aws_s3_stack.py` - S3 buckets for storage
  - `aws_stepfunction_stack.py` - Step Functions for workflow
  - `aws_eventbridge_new_stack.py` - EventBridge for event handling
  - `aws_kmskey_stack.py` - KMS keys for encryption
  - `aws_healthlake_stack.py` - HealthLake for FHIR data
  - 'aws_ecs_stack.py' - ECS task execution for WSI Transform step (Refer README_ECS_Migration.md for more details on ECR, Docker, ECS Task, Roles and all)
  - Lambda function code in respective directories

## Contributing

Please follow standard Git workflow:
1. Create a feature branch
2. Make changes
3. Submit a pull request

## License

[Specify your license]
