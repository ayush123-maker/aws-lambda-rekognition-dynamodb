from decimal import Decimal
import boto3
import json
import os # Added for environment variable
import urllib.parse # Added for handling object keys with spaces/special chars

# Get the DynamoDB table name from environment variable for flexibility
TABLE_NAME = os.environ.get('DYNAMODB_TABLE', 'ImageAnalysisResults') # Default if not set

# Initialize AWS clients
# It's good practice to initialize them outside the handler for potential reuse
s3_client = boto3.client('s3')
rekognition_client = boto3.client('rekognition')
dynamodb = boto3.resource('dynamodb') # Using resource for simpler PutItem
table = dynamodb.Table(TABLE_NAME)

print(f"Lambda function initializing. Target DynamoDB Table: {TABLE_NAME}")

def lambda_handler(event, context):
    print("Received event:", json.dumps(event, indent=2))

    # Get the bucket name and object key from the S3 event record
    try:
        # Handle potential URL encoding in object keys (e.g., spaces become '+')
        bucket_name = event['Records'][0]['s3']['bucket']['name']
        object_key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'], encoding='utf-8')
        print(f"Processing object {object_key} from bucket {bucket_name}")
    except KeyError as e:
        print(f"Error extracting bucket/key from event: {e}")
        print("Full event:", json.dumps(event, indent=2))
        return {'statusCode': 400, 'body': 'Error parsing S3 event structure'}

    try:
        # Call Rekognition to detect labels
        print(f"Calling Rekognition DetectLabels for {object_key}...")
        response = rekognition_client.detect_labels(
            Image={
                'S3Object': {
                    'Bucket': bucket_name,
                    'Name': object_key
                }
            },
            MaxLabels=10, # Limit the number of labels returned
            MinConfidence=75 # Only include labels with confidence >= 75%
        )
        print("Rekognition response received.")

        # Extract label names
        labels = [{'Name': label['Name'], 'Confidence': Decimal(str(round(label['Confidence'], 2)))} for label in response['Labels']]
        print(f"Detected labels: {labels}")

        # Store the results in DynamoDB
        print(f"Storing results in DynamoDB table {TABLE_NAME}...")
        db_response = table.put_item(
            Item={
                'ImageName': object_key, # Partition Key
                'Labels': labels,
                'Bucket': bucket_name # Adding bucket name as extra info
            }
        )
        print("Successfully stored results in DynamoDB.")
        print("DynamoDB put_item response:", db_response)

        return {
            'statusCode': 200,
            'body': json.dumps(f'Successfully processed {object_key} and stored labels.')
        }

    except Exception as e:
        print(f"Error during processing: {str(e)}")
        # Potentially more specific error handling here
        # (e.g., catch rekognition_client.exceptions.InvalidS3ObjectException)
        return {
            'statusCode': 500,
            'body': json.dumps(f'Error processing {object_key}: {str(e)}')
        }
