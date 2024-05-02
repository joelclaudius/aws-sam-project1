import os
import boto3
import requests
from bs4 import BeautifulSoup

region_name = 'us-east-1'

s3 = boto3.client('s3')
dynamodb = boto3.client('dynamodb', region_name = region_name)

def download_documents(url, bucket_name):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        links = soup.find_all('a', href=True)
        for link in links:
            document_url = link['href']
            if document_url.endswith('.txt'):
                document_name = os.path.basename(document_url)
                document_content = requests.get(document_url).text
                # Upload document content to S3
                s3.put_object(Bucket=bucket_name, Key=document_name, Body=document_content)
                # Save metadata to DynamoDB
                dynamodb.put_item(
                    TableName='GutenbergMetadata',
                    Item={
                        'DocumentId': {'S': document_name},
                        'Title': {'S': link.text.strip()},
                        'URL': {'S': document_url}
                    }
                )

def lambda_handler(event, context):
    # URL of the Gutenberg website
    gutenberg_url = 'https://www.gutenberg.org/'
    bucket_name = event['BUCKET_NAME']

    # Download documents from Gutenberg and store them in S3 with metadata in DynamoDB
    download_documents(gutenberg_url, bucket_name)

    return {
        'statusCode': 200,
        'body': 'Documents downloaded and uploaded to S3 with metadata'
    }
