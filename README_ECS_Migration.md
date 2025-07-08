# WSI Transform Lambda to ECS Migration

This document outlines the conversion of the WSITransform Lambda function to an ECS containerized task.

## Changes Made

### 1. Container Implementation
- **Location**: `aws_dcm2fhir_ecs/wsi_container/`
- **Files**:
  - `Dockerfile`: Container definition with Python 3.12 base image
  - `requirements.txt`: Python dependencies (boto3, pydicom, botocore)
  - `wsi_transform.py`: Containerized version of WSI transform logic

### 2. ECS Infrastructure
- **File**: `aws_dcm2fhir_ecs/aws_ecs_stack.py`
- **Components**:
  - ECR Repository for container images
  - ECS Fargate Cluster
  - Task Definition with 1024 CPU / 2048 MB memory
  - IAM roles for task execution and S3 access
  - CloudWatch log group

### 3. Step Functions Update
- **File**: `aws_dcm2fhir_ecs/stepfunction_ecs.json`
- **Changes**:
  - Replaced Lambda invoke with ECS runTask.sync
  - Added container environment variable overrides
  - Configured Fargate networking

### 4. CDK Stack Updates
- **Modified Files**:
  - `master_stack.py`: Added ECS stack integration
  - `aws_stepfunction_stack.py`: Added ECS parameters support

## Deployment Steps

### 1. Deploy Infrastructure
```bash
cdk deploy DCM2FHIRMasterStack-PRD
```

### 2. Build and Push Container
```bash
# Make script executable
chmod +x build_and_push.sh

# Build and push (replace with your values)
./build_and_push.sh 241003932265 us-east-1 uat-xxx-wsi-transform
```

### 3. Update Task Definition
After pushing the container, the ECS task will automatically use the `latest` tag.

## Key Benefits

1. **Scalability**: ECS tasks can handle larger workloads than Lambda
2. **Flexibility**: No 15-minute execution limit
3. **Resource Control**: Configurable CPU/memory allocation
4. **Cost Efficiency**: Pay only for task execution time
5. **Container Portability**: Can be used with EKS or other container platforms

## Environment Variables

The ECS task receives these environment variables from Step Functions:
- `S3_LandingBucketName`: Input DICOM bucket
- `S3_DICOMFileKey`: DICOM file key
- `S3_FHIROutPutBucketName`: Output FHIR bucket
- `S3_CustomFHIRFileName`: Output file name

## Monitoring

- CloudWatch logs: `/ecs/{resource_prefix}-wsi-transform`
- ECS task metrics available in CloudWatch
- Step Functions execution tracking

## Rollback Plan

To revert to Lambda-based execution:
1. Update Step Functions to use `stepfunction.json` instead of `stepfunction_ecs.json`
2. Redeploy the stack
3. Remove ECS stack if no longer needed