#consider the below DICOM metadata coming from the .dcm file of the WSI slide
'''# DICOM Meta Elements
(0008,0016) SOP Class UID                 = 1.2.840.10008.5.1.4.1.1.77.1.6  # VL Whole Slide Microscopy Image Storage
(0020,000D) Study Instance UID            = 1.2.826.0.1.3680043.123456789.1.1
(0020,000E) Series Instance UID           = 1.2.826.0.1.3680043.123456789.2.1
(0008,0018) SOP Instance UID              = 1.2.826.0.1.3680043.123456789.3.1

# Patient/Study Context
(0010,0010) Patient Name                  = Doe^John
(0010,0020) Patient ID                    = PAT123
(0020,0010) Study ID                      = STU456

# Specimen Details (Pathology)
(0040,0600) Specimen UID                  = 1.2.826.0.1.3680043.789.1.1
(0040,0602) Specimen Preparation Sequence = 
  (0040,0006) Specimen Short Description  = "Breast biopsy, malignant tumor"
  (0040,0007) Specimen Detailed Description = "Invasive ductal carcinoma, grade 3"

# Image Parameters
(0048,0001) Image Type                    = ORIGINAL\PRIMARY\VOLUME
(0048,0006) Total Pixel Matrix Columns    = 100000  # Slide width in pixels
(0048,0007) Total Pixel Matrix Rows       = 80000   # Slide height
(0048,0010) Total Pixel Matrix Focal Planes = 1     # Z-stacks (if 3D)
(0048,0005) Number of Optical Paths       = 1       # Brightfield, fluorescence, etc.
(0048,0002) Acquisition DateTime          = 20231010120000'''

#another DICOM Sample from WSI - EXAMPLE-2
'''(0002,0000) File Meta Information Group Length  UL: 222
(0002,0001) File Meta Information Version       OB: b'\x00\x01'
(0002,0002) Media Storage SOP Class UID         UI: VL Whole Slide Microscopy Image Storage
(0002,0003) Media Storage SOP Instance UID      UI: 1.3.6.1.4.1.5962.99.1.3073532328.211211830.1686700745128.9.0
(0002,0010) Transfer Syntax UID                 UI: JPEG 2000 Image Compression
(0002,0012) Implementation Class UID            UI: 1.3.6.1.4.1.5962.99.2
(0002,0013) Implementation Version Name         SH: 'PIXELMEDJAVA001'
(0002,0016) Source Application Entity Title     AE: 'OURAETITLE'
-------------------------------------------------
(0008,0008) Image Type                          CS: ['DERIVED', 'PRIMARY', 'VOLUME', 'NONE']
(0008,0012) Instance Creation Date              DA: '20230613'
(0008,0013) Instance Creation Time              TM: '235906.563'
(0008,0014) Instance Creator UID                UI: 1.3.6.1.4.1.5962.99.3
(0008,0016) SOP Class UID                       UI: VL Whole Slide Microscopy Image Storage
(0008,0017) Acquisition UID                     UI: 1.3.6.1.4.1.5962.99.1.3073532328.211211830.1686700745128.3.0
(0008,0018) SOP Instance UID                    UI: 1.3.6.1.4.1.5962.99.1.3073532328.211211830.1686700745128.9.0
(0008,0019) Pyramid UID                         UI: 1.3.6.1.4.1.5962.99.1.3073532328.211211830.1686700745128.2.0
(0008,0020) Study Date                          DA: '20090716'
(0008,0021) Series Date                         DA: '20090716'
(0008,0022) Acquisition Date                    DA: '20090716'
(0008,0023) Content Date                        DA: '20090716'
(0008,002A) Acquisition DateTime                DT: '20090716181506'
(0008,0030) Study Time                          TM: '181506'
(0008,0031) Series Time                         TM: '181506'
(0008,0032) Acquisition Time                    TM: '181506'
(0008,0033) Content Time                        TM: '181506'
(0008,0050) Accession Number                    SH: ''
(0008,0060) Modality                            CS: 'SM'
(0008,0070) Manufacturer                        LO: 'Leica Biosystems'
(0008,0090) Referring Physician's Name          PN: '^^^^'
(0008,0110)  Coding Scheme Identification Sequence  2 item(s) ----
   (0008,0102) Coding Scheme Designator            SH: 'DCM'
   (0008,010C) Coding Scheme UID                   UI: DICOM Controlled Terminology
   (0008,0112) Coding Scheme Registry              LO: 'HL7'
   (0008,0115) Coding Scheme Name                  ST: 'DICOM Controlled Terminology'
   ---------
   (0008,0102) Coding Scheme Designator            SH: 'SCT'
   (0008,010C) Coding Scheme UID                   UI: 2.16.840.1.113883.6.96
   (0008,0112) Coding Scheme Registry              LO: 'HL7'
   (0008,0115) Coding Scheme Name                  ST: 'SNOMED CT using SNOMED-CT style values'
   ---------
(0008,0201) Timezone Offset From UTC            SH: '+0000'
(0008,1090) Manufacturer's Model Name           LO: 'Aperio converted by com.pixelmed.convert.TIFFToDicom'
(0008,9206) Volumetric Properties               CS: 'VOLUME'
(0010,0010) Patient's Name                      PN: ''
(0010,0020) Patient ID                          LO: ''
(0010,0030) Patient's Birth Date                DA: ''
(0010,0040) Patient's Sex                       CS: ''
(0018,1000) Device Serial Number                LO: 'SS1283'
(0018,1020) Software Versions                   LO: ['v10.0.50', 'Tue Oct  4 18:39:42 EDT 2022']
(0018,9004) Content Qualification               CS: 'RESEARCH'
(0018,A001)  Contributing Equipment Sequence  2 item(s) ----
   (0008,0070) Manufacturer                        LO: 'PixelMed'
   (0008,0080) Institution Name                    LO: 'PixelMed'
   (0008,0081) Institution Address                 ST: 'Bangor, PA'
   (0008,1040) Institutional Department Name       LO: 'Software Development'
   (0008,1090) Manufacturer's Model Name           LO: 'com.pixelmed.convert.TIFFToDicom'
   (0018,1020) Software Versions                   LO: 'Vers. Tue Oct  4 18:39:42 EDT 2022'
   (0018,A002) Contribution DateTime               DT: '20230613235906.791+0000'
   (0018,A003) Contribution Description            ST: 'TIFF to DICOM conversion'
   (0040,A170)  Purpose of Reference Code Sequence  1 item(s) ----
      (0008,0100) Code Value                          SH: '109103'
      (0008,0102) Coding Scheme Designator            SH: 'DCM'
      (0008,0104) Code Meaning                        LO: 'Modifying Equipment'
      ---------
   ---------
   (0008,0070) Manufacturer                        LO: 'PixelMed'
   (0008,0080) Institution Name                    LO: 'PixelMed'
   (0008,0081) Institution Address                 ST: 'Bangor, PA'
   (0008,1040) Institutional Department Name       LO: 'Software Development'
   (0008,1090) Manufacturer's Model Name           LO: 'com.pixelmed.apps.SetCharacteristicsFromSummary'
   (0018,1020) Software Versions                   LO: 'Vers. Tue Oct  4 18:39:42 EDT 2022'
   (0018,A002) Contribution DateTime               DT: '20230613235906.806+0000'
   (0018,A003) Contribution Description            ST: 'Set characteristics from summary'
   (0040,A170)  Purpose of Reference Code Sequence  1 item(s) ----
      (0008,0100) Code Value                          SH: '109103'
      (0008,0102) Coding Scheme Designator            SH: 'DCM'
      (0008,0104) Code Meaning                        LO: 'Modifying Equipment'
      ---------
   ---------
(0020,000D) Study Instance UID                  UI: 1.3.6.1.4.1.5962.99.1.3073532328.211211830.1686700745128.5.0
(0020,000E) Series Instance UID                 UI: 1.3.6.1.4.1.5962.99.1.3073532328.211211830.1686700745128.4.0
(0020,0010) Study ID                            SH: ''
(0020,0011) Series Number                       IS: None
(0020,0013) Instance Number                     IS: '1'
(0020,0020) Patient Orientation                 CS: ''
(0020,0052) Frame of Reference UID              UI: 1.3.6.1.4.1.5962.99.1.3073532328.211211830.1686700745128.7.0
(0020,1040) Position Reference Indicator        LO: 'SLIDE_CORNER'
(0020,4000) Image Comments                      LT: Array of 530 elements
(0020,9221)  Dimension Organization Sequence  1 item(s) ----
   (0020,9164) Dimension Organization UID          UI: 1.3.6.1.4.1.5962.99.1.3073532328.211211830.1686700745128.14.0
   ---------
(0020,9222)  Dimension Index Sequence  2 item(s) ----
   (0020,9164) Dimension Organization UID          UI: 1.3.6.1.4.1.5962.99.1.3073532328.211211830.1686700745128.14.0
   (0020,9165) Dimension Index Pointer             AT: (0048,021F)
   (0020,9167) Functional Group Pointer            AT: (0048,021A)
   (0020,9421) Dimension Description Label         LO: 'Row Position'
   ---------
   (0020,9164) Dimension Organization UID          UI: 1.3.6.1.4.1.5962.99.1.3073532328.211211830.1686700745128.14.0
   (0020,9165) Dimension Index Pointer             AT: (0048,021E)
   (0020,9167) Functional Group Pointer            AT: (0048,021A)
   (0020,9421) Dimension Description Label         LO: 'Column Position'
   ---------
(0020,9311) Dimension Organization Type         CS: 'TILED_FULL'
(0028,0002) Samples per Pixel                   US: 3
(0028,0004) Photometric Interpretation          CS: 'YBR_ICT'
(0028,0006) Planar Configuration                US: 0
(0028,0008) Number of Frames                    IS: '4209'
(0028,0010) Rows                                US: 256
(0028,0011) Columns                             US: 256
(0028,0100) Bits Allocated                      US: 8
(0028,0101) Bits Stored                         US: 8
(0028,0102) High Bit                            US: 7
(0028,0103) Pixel Representation                US: 0
(0028,0301) Burned In Annotation                CS: 'NO'
(0028,0302) Recognizable Visual Features        CS: 'NO'
(0028,2110) Lossy Image Compression             CS: '01'
(0028,2112) Lossy Image Compression Ratio       DS: '13.424'
(0028,2114) Lossy Image Compression Method      CS: 'ISO_15444_1'
(0040,0512) Container Identifier                LO: 'SLIDE_1'
(0040,0513)  Issuer of the Container Identifier Sequence  0 item(s) ----
(0040,0518)  Container Type Code Sequence  1 item(s) ----
   (0008,0100) Code Value                          SH: '433466003'
   (0008,0102) Coding Scheme Designator            SH: 'SCT'
   (0008,0104) Code Meaning                        LO: 'Microscope slide'
   ---------
(0040,0555)  Acquisition Context Sequence  0 item(s) ----
(0040,0560)  Specimen Description Sequence  1 item(s) ----
   (0040,0551) Specimen Identifier                 LO: 'SPECIMEN_1'
   (0040,0554) Specimen UID                        UI: 1.3.6.1.4.1.5962.99.1.3073532328.211211830.1686700745128.6.0
   (0040,0562)  Issuer of the Specimen Identifier Sequence  0 item(s) ----
   (0040,0610)  Specimen Preparation Sequence  0 item(s) ----
   ---------
(0048,0001) Imaged Volume Width                 FL: 3.8404252529144287
(0048,0002) Imaged Volume Height                FL: 4.370750427246094
(0048,0003) Imaged Volume Depth                 FL: 0.0
(0048,0006) Total Pixel Matrix Columns          UL: 15374
(0048,0007) Total Pixel Matrix Rows             UL: 17497
(0048,0008)  Total Pixel Matrix Origin Sequence  1 item(s) ----
   (0040,072A) X Offset in Slide Coordinate System DS: '14.299895'
   (0040,073A) Y Offset in Slide Coordinate System DS: '38.2149112066508'
   ---------
(0048,0010) Specimen Label in Image             CS: 'NO'
(0048,0011) Focus Method                        CS: 'AUTO'
(0048,0012) Extended Depth of Field             CS: 'NO'
(0048,0015) Recommended Absent Pixel CIELab Val US: [65535, 0, 0]
(0048,0102) Image Orientation (Slide)           DS: [0, -1, 0, -1, 0, 0]
(0048,0105)  Optical Path Sequence  1 item(s) ----
   (0022,0016)  Illumination Type Code Sequence  1 item(s) ----
      (0008,0100) Code Value                          SH: '111744'
      (0008,0102) Coding Scheme Designator            SH: 'DCM'
      (0008,0104) Code Meaning                        LO: 'Brightfield illumination'
      ---------
   (0028,2000) ICC Profile                         OB: Array of 141992 elements
   (0048,0106) Optical Path Identifier             SH: '0'
   (0048,0108)  Illumination Color Code Sequence  1 item(s) ----
      (0008,0100) Code Value                          SH: '414298005'
      (0008,0102) Coding Scheme Designator            SH: 'SCT'
      (0008,0104) Code Meaning                        LO: 'Full Spectrum'
      ---------
   (0048,0112) Objective Lens Power                DS: '40'
   ---------
(0048,0302) Number of Optical Paths             UL: 1
(0048,0303) Total Pixel Matrix Focal Planes     UL: 1
(5200,9229)  Shared Functional Groups Sequence  1 item(s) ----
   (0028,9110)  Pixel Measures Sequence  1 item(s) ----
      (0018,0050) Slice Thickness                     DS: '0'
      (0028,0030) Pixel Spacing                       DS: [.0002498, .0002498]
      ---------
   (0040,0710)  Whole Slide Microscopy Image Frame Type Sequence  1 item(s) ----
      (0008,9007) Frame Type                          CS: ['DERIVED', 'PRIMARY', 'VOLUME', 'NONE']
      ---------
   ---------
(7FE0,0010) Pixel Data                          OB: Array of 60150804 elements
(FFFC,FFFC) Data Set Trailing Padding           OB: Array of 175872 elements'''


import pydicom
import json
from datetime import datetime
import boto3
import pydicom
from io import BytesIO
import json
import logging
from botocore.exceptions import ClientError
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    try:
        #parameters = event.get('parameters', {})
        s3_bucketname = event.get('S3_LandingBucketName')
        s3_key = event.get('S3_DICOMFileKey')
        output_s3_bucket = event.get('S3_FHIROutPutBucketName')
        output_s3_key = event.get('S3_CustomFHIRFileName')

        # Get the image metadata
        image_metadata = getImageMetadata(s3_bucketname, s3_key)
        fhir_data=create_fhir_structure(image_metadata)
        save_fhir = save_fhir_json(fhir_data, output_s3_bucket, output_s3_key)
        return save_fhir
    
    except Exception as e:
        print(f"Error Lambda Handler to Process FHIR conversion flow: {str(e)}")
        raise

def getImageMetadata(bucket_name, s3_key, aws_access_key_id=None, aws_secret_access_key=None):
    try:
        # Initialize S3 client (configure credentials appropriately)
        s3 = boto3.client(
            's3',
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key
        )
        # Fetch DICOM file from S3
        response = s3.get_object(Bucket=bucket_name, Key=s3_key)
        dicom_bytes = response['Body'].read()
        # Load DICOM bytes into pydicom
        dicom_file = BytesIO(dicom_bytes)
        ds = pydicom.dcmread(dicom_file, stop_before_pixels=True)  # Skip pixel data for faster metadata extraction
        logging.info(f"Image Data from dcm file ds=: {ds}")
        # Extract metadata into a dictionary
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
            "AcquisitionTime" : ds.AcquisitionDateTime  if 'AcquisitionDateTime' in ds else None,
            "SeriesInstanceUID" : ds.SeriesInstanceUID if 'SeriesInstanceUID' in ds else None,
            "DimensionOrganizationType" : ds.DimensionOrganizationType if 'DimensionOrganizationType' in ds else None,
            "SeriesDescription" : ds.SeriesDescription if 'SeriesDescription' in ds else None,
            "InstanceNumber" : ds.InstanceNumber if 'InstanceNumber' in ds else None,
            "SeriesNumber" : ds.SeriesNumber if 'SeriesNumber' in ds else None,
            "MediaStorageSOPClassUID" : ds.MediaStorageSOPClassUID if 'MediaStorageSOPClassUID' in ds else None
            }
        
        return metadata
    except Exception as e:
        print(f"Error mapping metadata from DICOM to metadata object: {str(e)}")
        raise

#create the FHIR file from the subsections of DICOM file and map to FHIR file
def create_fhir_structure(metadata):
    try:
        """Create FHIR ImagingStudy structure from DICOM metadata"""
        fhir_data = {
            "resourceType": "ImagingStudy", #ok to keep "ImagingStudy" as the value for this resourceType for WSI Imaging
            "id": metadata['StudyInstanceUID'], #replace-1 with new variable for StudyInstanceUID which indicated
            "status": "available", #This is ok to keep as-is
            "subject": {
                "reference": f"Patient/{metadata['PatientName']}",
                "display": str(metadata['PatientName'])
            },
            "started": datetime.strptime(metadata['AcquisitionTime'], '%Y%m%d%H%M%S').strftime('%Y-%m-%dT%H:%M:%SZ'),
            "modality": [

                {
                    "system": "http://dicom.nema.org/resources/ontology/DCM",
                    "code": metadata['Modality'] #replace with Modality reference
                }
            ],
            "series": create_series_structure(metadata)
        }
        return fhir_data
    
    except Exception as e1:
        print(f"create FHIR structure has an issue to map fields: {str(e1)}")
        raise

def create_series_structure(metadata):
    try:
        if (len(str(metadata['SeriesDescription']).strip())>0):
            str_description = metadata['SeriesDescription']
        else:
            str_description = "Whole Slide Image Pathology Scan"

        return [{
            "uid": metadata['SeriesInstanceUID'],
            "number": metadata['InstanceNumber'], #replace with InstanceNumber
            "modality": {
                "system": "http://dicom.nema.org/resources/ontology/DCM",
                "code": metadata['Modality'] #replace with Modality reference
            },
                #"description": "Whole Slide Image Pathology Scan",
                "description" : str_description or "WSI Image Scan - Default Decsription", #replace-1 with SeriesDescription
                "numberOfInstances": metadata['InstanceNumber'], #replace with InstanceNumber
                "instance": create_instance_structure(metadata)
        }]
    
    except Exception as e:
        print(f"create series structure has an issue to map uid, modality, number and others: {str(e)}")
        raise


def create_instance_structure(metadata):
    try:
        """Create instance structure for FHIR data"""
        return [{
            "uid": metadata['StudyInstanceUID'],
            "number": 1,
            "sopClass": {
                "system": "urn:ietf:rfc:3986", #Uniform Resource Name (URN) following the DICOM UID format
                "code": metadata['SOPClassUID']
            }

        }]
    except Exception as e:
        print(f"create instance structure has an issue to map uid, sopClass and others: {str(e)}")
        raise


#Save the FHIR V4 file in S3 bucket
def save_fhir_json(fhir_data, bucket_name, file_key):
    try:
        """Save FHIR data to JSON file in S3 bucket"""
        # Initialize S3 client
        s3_client = boto3.client('s3')  
        # Convert FHIR data to JSON string
        json_data = json.dumps(fhir_data, indent=2) 
        # Upload the JSON data to S3
        write_response = s3_client.put_object(
                Bucket=bucket_name,
                Key=file_key,
                Body=json_data,
                ContentType='application/json'
            )   
        print(f"Successfully saved FHIR data to s3://{bucket_name}/{file_key}")
        return write_response


    except Exception as e:
        print(f"Error writing the FHIR JSON into S3 bucket: {str(e)}")
        raise
