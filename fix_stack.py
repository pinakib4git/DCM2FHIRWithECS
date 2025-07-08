import boto3
import argparse

def continue_update_rollback(stack_name, region='us-east-1'):
    """
    Attempts to continue the update rollback for a stack in UPDATE_ROLLBACK_FAILED state.
    
    Args:
        stack_name (str): The name of the CloudFormation stack
        region (str): AWS region where the stack is deployed
    """
    try:
        # Create CloudFormation client
        cfn = boto3.client('cloudformation', region_name=region)
        
        # Continue update rollback
        print(f"Attempting to continue update rollback for stack: {stack_name}")
        response = cfn.continue_update_rollback(
            StackName=stack_name
        )
        
        print(f"Successfully initiated continue-update-rollback: {response}")
        print("Check the AWS CloudFormation console to monitor the progress.")
        
    except Exception as e:
        print(f"Error continuing update rollback: {str(e)}")

def delete_stack(stack_name, region='us-east-1'):
    """
    Deletes a CloudFormation stack.
    
    Args:
        stack_name (str): The name of the CloudFormation stack
        region (str): AWS region where the stack is deployed
    """
    try:
        # Create CloudFormation client
        cfn = boto3.client('cloudformation', region_name=region)
        
        # Delete the stack
        print(f"Attempting to delete stack: {stack_name}")
        response = cfn.delete_stack(
            StackName=stack_name
        )
        
        print(f"Successfully initiated stack deletion: {response}")
        print("Check the AWS CloudFormation console to monitor the progress.")
        
    except Exception as e:
        print(f"Error deleting stack: {str(e)}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Fix CloudFormation stack in UPDATE_ROLLBACK_FAILED state')
    parser.add_argument('--stack-name', default='DCM2FHIRMasterStack', help='Name of the CloudFormation stack')
    parser.add_argument('--region', default='us-east-1', help='AWS region')
    parser.add_argument('--action', choices=['continue-rollback', 'delete'], required=True, 
                        help='Action to perform: continue-rollback or delete')
    
    args = parser.parse_args()
    
    if args.action == 'continue-rollback':
        continue_update_rollback(args.stack_name, args.region)
    elif args.action == 'delete':
        delete_stack(args.stack_name, args.region)