from aws_cdk import NestedStack
from aws_cdk import CfnOutput
from aws_cdk import aws_kms as kms
from constructs import Construct

class KMSKeyStack(NestedStack):
    def __init__(self, scope: Construct, construct_id: str, resource_prefix: str = None, **kwargs):
        super().__init__(scope, construct_id, **kwargs)
        
        # Create KMS key
        KMSKeyInstance = kms.Key(
            self,  f"{resource_prefix}-EncryptionKey",
            enable_key_rotation=True,
            description="Key for encrypting resources"
        )
        #get the kms_key value from above instance
        self.kms_key = KMSKeyInstance.key_id
        # Output important information
        CfnOutput(self, "KMSKeyID", value=KMSKeyInstance.key_id)
