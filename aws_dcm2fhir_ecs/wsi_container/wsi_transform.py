import pydicom
import json
import os
import sys
from datetime import datetime
import boto3
from io import BytesIO
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_image_metadata(bucket_name, s3_key):
    try:
        s3 = boto3.client('s3')
        response = s3.get_object(Bucket=bucket_name, Key=s3_key)
        dicom_bytes = response['Body'].read()
        
        dicom_file = BytesIO(dicom_bytes)
        ds = pydicom.dcmread(dicom_file, stop_before_pixels=True)
        
        metadata = {
            "SOPClassUID": ds.SOPClassUID,
            "StudyInstanceUID": ds.StudyInstanceUID,
            "SeriesInstanceUID": ds.SeriesInstanceUID,
            "PatientName": str(ds.PatientName) if 'PatientName' in ds else None,
            "PatientID": ds.PatientID if 'PatientID' in ds else None,
            "StudyDate": ds.StudyDate if 'StudyDate' in ds else None,
            "Modality": ds.Modality if 'Modality' in ds else None,
            "SpecimenUID": ds.SpecimenUID if 'SpecimenUID' in ds else None,
            "TotalPixelMatrixColumns": ds.TotalPixelMatrixColumns if 'TotalPixelMatrixColumns' in ds else None,
            "TotalPixelMatrixRows": ds.TotalPixelMatrixRows if 'TotalPixelMatrixRows' in ds else None,
            "AcquisitionTime": ds.AcquisitionDateTime if 'AcquisitionDateTime' in ds else None,
            "DimensionOrganizationType": ds.DimensionOrganizationType if 'DimensionOrganizationType' in ds else None,
            "SeriesDescription": ds.SeriesDescription if 'SeriesDescription' in ds else None,
            "InstanceNumber": ds.InstanceNumber if 'InstanceNumber' in ds else None,
            "SeriesNumber": ds.SeriesNumber if 'SeriesNumber' in ds else None,
            "MediaStorageSOPClassUID": ds.MediaStorageSOPClassUID if 'MediaStorageSOPClassUID' in ds else None
        }
        return metadata
    except Exception as e:
        logger.error(f"Error extracting metadata: {str(e)}")
        raise

def create_fhir_structure(metadata):
    try:
        fhir_data = {
            "resourceType": "ImagingStudy",
            "id": metadata['StudyInstanceUID'],
            "status": "available",
            "subject": {
                "reference": f"Patient/{metadata['PatientName']}",
                "display": str(metadata['PatientName'])
            },
            "started": datetime.strptime(metadata['AcquisitionTime'], '%Y%m%d%H%M%S').strftime('%Y-%m-%dT%H:%M:%SZ'),
            "modality": [{
                "system": "http://dicom.nema.org/resources/ontology/DCM",
                "code": metadata['Modality']
            }],
            "series": create_series_structure(metadata)
        }
        return fhir_data
    except Exception as e:
        logger.error(f"Error creating FHIR structure: {str(e)}")
        raise

def create_series_structure(metadata):
    try:
        str_description = metadata['SeriesDescription'] if metadata.get('SeriesDescription') else "Whole Slide Image Pathology Scan"
        
        return [{
            "uid": metadata['SeriesInstanceUID'],
            "number": metadata['InstanceNumber'],
            "modality": {
                "system": "http://dicom.nema.org/resources/ontology/DCM",
                "code": metadata['Modality']
            },
            "description": str_description,
            "numberOfInstances": metadata['InstanceNumber'],
            "instance": create_instance_structure(metadata)
        }]
    except Exception as e:
        logger.error(f"Error creating series structure: {str(e)}")
        raise

def create_instance_structure(metadata):
    try:
        return [{
            "uid": metadata['StudyInstanceUID'],
            "number": 1,
            "sopClass": {
                "system": "urn:ietf:rfc:3986",
                "code": metadata['SOPClassUID']
            }
        }]
    except Exception as e:
        logger.error(f"Error creating instance structure: {str(e)}")
        raise

def save_fhir_json(fhir_data, bucket_name, file_key):
    try:
        s3_client = boto3.client('s3')
        json_data = json.dumps(fhir_data, indent=2)
        
        response = s3_client.put_object(
            Bucket=bucket_name,
            Key=file_key,
            Body=json_data,
            ContentType='application/json'
        )
        logger.info(f"Successfully saved FHIR data to s3://{bucket_name}/{file_key}")
        return response
    except Exception as e:
        logger.error(f"Error saving FHIR JSON: {str(e)}")
        raise

def main():
    try:
        # Get parameters from environment variables (set by ECS task)
        s3_bucketname = os.environ.get('S3_LandingBucketName')
        s3_key = os.environ.get('S3_DICOMFileKey')
        output_s3_bucket = os.environ.get('S3_FHIROutPutBucketName')
        output_s3_key = os.environ.get('S3_CustomFHIRFileName')
        
        if not all([s3_bucketname, s3_key, output_s3_bucket, output_s3_key]):
            raise ValueError("Missing required environment variables")
        
        logger.info(f"Processing DICOM file: s3://{s3_bucketname}/{s3_key}")
        
        # Process the DICOM file
        image_metadata = get_image_metadata(s3_bucketname, s3_key)
        fhir_data = create_fhir_structure(image_metadata)
        save_fhir_json(fhir_data, output_s3_bucket, output_s3_key)
        
        logger.info("WSI Transform completed successfully")
        
    except Exception as e:
        logger.error(f"WSI Transform failed: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()