import boto3

s3 = boto3.client('s3')

def upload_to_stuvia(document_key):
    # Get document content from S3
    response = s3.get_object(Bucket='your-bucket-name', Key=document_key)
    document_content = response['Body'].read().decode('utf-8')

    # Placeholder logic for uploading to Stuvia
    print(f"Uploading document '{document_key}' to Stuvia")

def lambda_handler(event, context):
    # Sample document key for demonstration purposes
    document_key = event['Records'][0]['s3']['object']['key']

    # Upload document to Stuvia
    upload_to_stuvia(document_key)

    return {
        'statusCode': 200,
        'body': 'Document uploaded to Stuvia'
    }
