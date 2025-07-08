import json
import os
import logging
import boto3
from botocore.exceptions import ClientError

logger = logging.getLogger()
logger.setLevel(logging.INFO)

s3 = boto3.client('s3')

def convert_json_to_ndjson(json_data):
    """Convert JSON data to NDJSON format."""
    items = json_data if isinstance(json_data, list) else [json_data]
    return '\n'.join(json.dumps(item, ensure_ascii=False) for item in items) + '\n'

def extract_s3_info(event):
    """Extract S3 bucket and key information from event."""
    if 'Records' in event:
        record = event['Records'][0]['s3']
        source_bucket = record['bucket']['name']
        source_key = record['object']['key']
        destination_bucket = os.environ.get('DESTINATION_BUCKET', source_bucket)
        destination_key = os.path.splitext(source_key)[0] + '.ndjson'
    else:
        source_bucket = event.get('source_bucket', os.environ.get('SOURCE_BUCKET'))
        source_key = event.get('source_key')
        destination_bucket = event.get('destination_bucket', os.environ.get('DESTINATION_BUCKET', source_bucket))
        destination_key = event.get('destination_key', os.path.splitext(source_key)[0] + '.ndjson')
    
    if not source_bucket or not source_key:
        raise ValueError("Source bucket and key must be provided")
    
    return source_bucket, source_key, destination_bucket, destination_key

def lambda_handler(event, context):
    """AWS Lambda function handler to convert JSON files from S3 to NDJSON format."""
    try:
        logger.info(f"Processing event: {json.dumps(event)}")
        
        source_bucket, source_key, destination_bucket, destination_key = extract_s3_info(event)
        
        logger.info(f"Converting s3://{source_bucket}/{source_key} to s3://{destination_bucket}/{destination_key}")
        
        # Read and parse JSON from S3
        response = s3.get_object(Bucket=source_bucket, Key=source_key)
        json_data = json.loads(response['Body'].read().decode('utf-8'))
        
        # Convert to NDJSON and upload
        ndjson_content = convert_json_to_ndjson(json_data)
        s3.put_object(
            Bucket=destination_bucket,
            Key=destination_key,
            Body=ndjson_content.encode('utf-8'),
            ContentType='application/x-ndjson'
        )
        
        logger.info(f"Successfully converted and uploaded to s3://{destination_bucket}/{destination_key}")
        
        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': 'Successfully converted JSON to NDJSON',
                'source': f"s3://{source_bucket}/{source_key}",
                'destination': f"s3://{destination_bucket}/{destination_key}"
            })
        }
        
    except (ClientError, json.JSONDecodeError, ValueError) as e:
        logger.error(f"Error: {e}")
        return {
            'statusCode': 400 if isinstance(e, (json.JSONDecodeError, ValueError)) else 500,
            'body': json.dumps(f"Error: {str(e)}")
        }
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return {
            'statusCode': 500,
            'body': json.dumps(f"Unexpected error: {str(e)}")
        }