from aws_cdk import (
    NestedStack,
    CfnOutput,
    aws_healthlake as healthlake,
    aws_iam as iam,
    RemovalPolicy
)
from constructs import Construct

class HealthLakeStack(NestedStack):
    def __init__(self, scope: Construct, construct_id: str, resource_prefix: str = None, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Create an Amazon HealthLake data store
        # Note: HealthLake supports FHIR R4 data stores
        healthlake_datastore = healthlake.CfnFHIRDatastore(
            self, "HealthLakeDataStore",
            datastore_type_version="R4",  # FHIR version R4
            datastore_name= f"{resource_prefix}-FHIRV4HealthLakeDataStore"
    )
    #get the healthlake datastore_id from the datastore instance
        self.healthlake_datastore_id = healthlake_datastore.attr_datastore_id
        self.healthlake_datastore_arn = healthlake_datastore.attr_datastore_arn
        # Output important information
        CfnOutput(self, "HealthLakeDataStoreID", value=healthlake_datastore.attr_datastore_id)
        CfnOutput(self, "HealthLakeDataStoreARN", value=healthlake_datastore.attr_datastore_arn)
