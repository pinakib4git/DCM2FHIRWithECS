#!/bin/bash

# Build and push WSI Transform container to ECR
# Usage: ./build_and_push.sh <account-id> <region> <repository-name>

ACCOUNT_ID=$1
REGION=$2
REPO_NAME=$3

if [ -z "$ACCOUNT_ID" ] || [ -z "$REGION" ] || [ -z "$REPO_NAME" ]; then
    echo "Usage: $0 <account-id> <region> <repository-name>"
    exit 1
fi

ECR_URI="${ACCOUNT_ID}.dkr.ecr.${REGION}.amazonaws.com/${REPO_NAME}"

echo "Building Docker image..."
cd aws_dcm2fhir_ecs/wsi_container
docker build -t wsi-transform .

echo "Tagging image..."
docker tag wsi-transform:latest ${ECR_URI}:latest

echo "Logging into ECR..."
aws ecr get-login-password --region ${REGION} | docker login --username AWS --password-stdin ${ECR_URI}

echo "Pushing image to ECR..."
docker push ${ECR_URI}:latest

echo "Image pushed successfully to ${ECR_URI}:latest"