#!/usr/bin/env python3
"""
LocalStack 리소스 생성 스크립트
"""

import boto3
import json

# LocalStack 설정
LOCALSTACK_ENDPOINT = "http://localhost:4566"
REGION = "ap-northeast-2"

# AWS 클라이언트 설정
aws_config = {
    'endpoint_url': LOCALSTACK_ENDPOINT,
    'region_name': REGION,
    'aws_access_key_id': 'test',
    'aws_secret_access_key': 'test'
}

def create_kinesis_stream():
    """Kinesis 스트림 생성"""
    try:
        kinesis_client = boto3.client('kinesis', **aws_config)
        
        # 스트림 생성
        response = kinesis_client.create_stream(
            StreamName='ad-scouter-ingest-stream',
            ShardCount=1
        )
        print("✅ Kinesis stream created successfully")
        return True
    except Exception as e:
        if "ResourceInUseException" in str(e):
            print("ℹ️  Kinesis stream already exists")
            return True
        else:
            print(f"❌ Failed to create Kinesis stream: {e}")
            return False

def create_dynamodb_table():
    """DynamoDB 테이블 생성"""
    try:
        dynamodb_client = boto3.client('dynamodb', **aws_config)
        
        # 테이블 생성
        response = dynamodb_client.create_table(
            TableName='ad-scouter-stats',
            AttributeDefinitions=[
                {
                    'AttributeName': 'customerId',
                    'AttributeType': 'S'
                },
                {
                    'AttributeName': 'eventId',
                    'AttributeType': 'S'
                }
            ],
            KeySchema=[
                {
                    'AttributeName': 'customerId',
                    'KeyType': 'HASH'
                },
                {
                    'AttributeName': 'eventId',
                    'KeyType': 'RANGE'
                }
            ],
            BillingMode='PAY_PER_REQUEST'
        )
        print("✅ DynamoDB table created successfully")
        return True
    except Exception as e:
        if "ResourceInUseException" in str(e):
            print("ℹ️  DynamoDB table already exists")
            return True
        else:
            print(f"❌ Failed to create DynamoDB table: {e}")
            return False

def create_s3_bucket():
    """S3 버킷 생성"""
    try:
        s3_client = boto3.client('s3', **aws_config)
        
        bucket_name = 'ad-scouter-test-bucket'
        response = s3_client.create_bucket(
            Bucket=bucket_name,
            CreateBucketConfiguration={'LocationConstraint': REGION}
        )
        print(f"✅ S3 bucket '{bucket_name}' created successfully")
        return True
    except Exception as e:
        if "BucketAlreadyOwnedByYou" in str(e) or "BucketAlreadyExists" in str(e):
            print(f"ℹ️  S3 bucket already exists")
            return True
        else:
            print(f"❌ Failed to create S3 bucket: {e}")
            return False

def main():
    """메인 실행 함수"""
    print("🚀 Creating LocalStack resources...")
    print("=" * 40)
    
    success_count = 0
    total_tests = 3
    
    # 리소스 생성
    if create_kinesis_stream():
        success_count += 1
    
    if create_dynamodb_table():
        success_count += 1
    
    if create_s3_bucket():
        success_count += 1
    
    print("=" * 40)
    print(f"📊 Results: {success_count}/{total_tests} resources created successfully")
    
    if success_count == total_tests:
        print("🎉 All resources are ready for testing!")
    else:
        print("⚠️  Some resources failed to create.")
    
    return success_count == total_tests

if __name__ == "__main__":
    exit(0 if main() else 1)
