import boto3
import datetime

# Initialize the RDS client
rds_client = boto3.client('rds')

# Define the RDS cluster identifier
RDS_CLUSTER_IDENTIFIER = 'aurora-cluster-demo'

def lambda_handler(event, context):
    # Get the current day of the week (0 = Monday, 6 = Sunday)
    current_day = datetime.datetime.now().weekday()

    # Check if it's a weekend (Saturday = 5, Sunday = 6)
    if current_day in [5, 6]:  # Weekend
        # Stop the RDS cluster if it's running
        response = rds_client.describe_db_clusters(DBClusterIdentifier=RDS_CLUSTER_IDENTIFIER)
        cluster_status = response['DBClusters'][0]['Status']

        if cluster_status == 'available':
            print("Stopping RDS cluster...")
            rds_client.stop_db_cluster(DBClusterIdentifier=RDS_CLUSTER_IDENTIFIER)
            return {
                'statusCode': 200,
                'body': 'RDS cluster stopped successfully.'
            }
        else:
            return {
                'statusCode': 200,
                'body': 'RDS cluster is already stopped.'
            }
    else:  # Weekday
        # Start the RDS cluster if it's stopped
        response = rds_client.describe_db_clusters(DBClusterIdentifier=RDS_CLUSTER_IDENTIFIER)
        cluster_status = response['DBClusters'][0]['Status']

        if cluster_status == 'stopped':
            print("Starting RDS cluster...")
            rds_client.start_db_cluster(DBClusterIdentifier=RDS_CLUSTER_IDENTIFIER)
            return {
                'statusCode': 200,
                'body': 'RDS cluster started successfully.'
            }
        else:
            return {
                'statusCode': 200,
                'body': 'RDS cluster is already running.'
            }
