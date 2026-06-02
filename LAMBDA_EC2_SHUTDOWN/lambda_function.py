import boto3

def lambda_handler(event, context):
    
    ec2 = boto3.client('ec2')

    # Find all running instances
    response = ec2.describe_instances(
        Filters=[
            {
                'Name': 'instance-state-name',
                'Values': ['running']
            }
        ]
    )

    # Pull out the instance IDs
    instance_ids = []
    for reservation in response['Reservations']:
        for instance in reservation['Instances']:
            instance_ids.append(instance['InstanceId'])

    # If nothing is running, exit cleanly
    if not instance_ids:
        print("No running instances found. Nothing to stop.")
        return {
            'statusCode': 200,
            'body': 'No running instances found. Nothing to stop.'
        }

    print(f"Found {len(instance_ids)} running instance(s): {instance_ids}")
    print("Initiating stop...")

    # Stop all running instances
    stop_response = ec2.stop_instances(InstanceIds=instance_ids)

    # Log what happened
    for instance in stop_response['StoppingInstances']:
        iid = instance['InstanceId']
        prev = instance['PreviousState']['Name']
        curr = instance['CurrentState']['Name']
        print(f"  {iid}: {prev} → {curr}")

    return {
        'statusCode': 200,
        'body': f"Successfully stopped {len(instance_ids)} instance(s): {instance_ids}"
    }