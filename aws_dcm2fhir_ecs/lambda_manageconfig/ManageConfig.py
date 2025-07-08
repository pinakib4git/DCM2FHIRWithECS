import json
import random
import os


def lambda_handler(event, context):
    RandomNum = random.randint(100,999)
    S3_LandingBucketName = event.get('S3BucketName')   
    S3_DICOMFileKey = event.get('S3BucketKey')
    S3_CustomFHIRFileName = f"Custom-FHIR-Files/CustomFHIRFile{RandomNum}.json"
    
    #get the environment parameters from the config file
    S3_FHIROutPutBucketName = os.environ['S3_FHIROutPutBucketName']         
    DICOM_InputBucketName = os.environ['DICOM_InputBucketName']
    DICOM_OutputBucketName=os.environ['DICOM_OutputBucketName']
    HealthLake_ImportExecutionRoleArn = os.environ['JobProcessingIAMRole']
    KMSKeyID_HealthLakeImportJob = os.environ['KMS_KEY_ID']
    ImageStore_CreateImportRoleArn = os.environ['JobProcessingIAMRole']
    HL_DS_ID = os.environ['HEALTHLAKE_DATASTORE_ID']
    #derive configuration based on paremeters from Environment variables and fixed prefixes
    ImageImportJob_InputS3Bucket = f"{DICOM_InputBucketName}/inputfile/"
    ImageImportJob_OutputS3Bucket = f"{DICOM_OutputBucketName}/outputfiles/"
    S3_HealthLakeImportBucketName = f"{S3_FHIROutPutBucketName}/Custom-FHIR-Files/"
    S3_HealthLakeOutputBucketName = f"{S3_FHIROutPutBucketName}/HealthLake-Output/"
    ImageStoreID_ImportJob = f"HealthImagingDataStore-{RandomNum}"
    
    
    # Return all parameters to drive the process end to end
    return {
        'statusCode': 200,
        'S3_LandingBucketName': S3_LandingBucketName,
        'S3_DICOMFileKey': S3_DICOMFileKey,
        'S3_FHIROutPutBucketName': S3_FHIROutPutBucketName,
        'S3_CustomFHIRFileName' :  S3_CustomFHIRFileName,
        'S3_HealthLakeImportBucketName': S3_HealthLakeImportBucketName,
        'S3_HealthLakeOutputBucketName': S3_HealthLakeOutputBucketName,
        'HealthLake_ImportExecutionRoleArn':HealthLake_ImportExecutionRoleArn,
        'ImageStore_CreateImportRoleArn':ImageStore_CreateImportRoleArn,
        'ImageStoreID_ImportJob' : ImageStoreID_ImportJob,
        'ImageImportJob_OutputS3Bucket':ImageImportJob_OutputS3Bucket,
        'ImageImportJob_InputS3Bucket':ImageImportJob_InputS3Bucket,
        'KMSKeyID_HealthLakeImportJob':KMSKeyID_HealthLakeImportJob,
        'HL_DS_ID':HL_DS_ID
    }
