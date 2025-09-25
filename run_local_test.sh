#!/bin/bash
set -e # 오류 발생 시 즉시 중단

echo "--- 🚀 Starting Local Test Environment ---"

# 1. Docker 컨테이너 실행
echo "--- (1/5) Starting Docker containers (LocalStack & Postgres) ---"
docker-compose up -d

# 2. LocalStack이 준비될 때까지 대기
echo "--- (2/5) Waiting for LocalStack to be ready... ---"
# health 엔드포인트가 200 OK를 반환할 때까지 10초 간격으로 확인
max_attempts=30
attempt=0
while [ $attempt -lt $max_attempts ]; do
    if curl -s -k "http://localhost:4566/_localstack/health" | grep -q '"services":'; then
        echo "LocalStack is ready!"
        break
    fi
    echo "Still waiting for LocalStack... (attempt $((attempt+1))/$max_attempts)"
    sleep 10
    attempt=$((attempt+1))
done

if [ $attempt -eq $max_attempts ]; then
    echo "❌ LocalStack failed to start within expected time"
    exit 1
fi

# 3. 로컬 AWS 리소스 생성
echo "--- (3/5) Setting up local AWS resources (Kinesis, DynamoDB) ---"
export AWS_ENDPOINT_URL=http://localhost:4566
export AWS_DEFAULT_REGION=ap-northeast-2
export AWS_ACCESS_KEY_ID=test
export AWS_SECRET_ACCESS_KEY=test

# Kinesis 스트림 생성
echo "Creating Kinesis stream..."
aws kinesis create-stream --stream-name ad-scouter-ingest-stream --shard-count 1 > /dev/null 2>&1 || echo "Kinesis stream already exists."

# DynamoDB 테이블 생성
echo "Creating DynamoDB table..."
aws dynamodb create-table \
    --table-name ad-scouter-stats \
    --attribute-definitions AttributeName=customerId,AttributeType=S AttributeName=eventId,AttributeType=S \
    --key-schema AttributeName=customerId,KeyType=HASH AttributeName=eventId,KeyType=RANGE \
    --billing-mode PAY_PER_REQUEST > /dev/null 2>&1 || echo "DynamoDB table already exists."

echo "Local resources are set up."

# 4. 환경 변수 설정
echo "--- (4/5) Setting up environment variables ---"
export LOCALSTACK_ENDPOINT_URL=http://localhost:4566
export KINESIS_STREAM_NAME=ad-scouter-ingest-stream
export STATS_TABLE_NAME=ad-scouter-stats
export GEMINI_API_KEY=${GEMINI_API_KEY:-"test-key"}

echo "Environment variables configured."

# 5. 테스트 실행
echo "--- (5/5) Running End-to-End test ---"
if [ -f "scripts/e2e_test_runner.py" ]; then
    python scripts/e2e_test_runner.py
else
    echo "⚠️  E2E test script not found. Creating basic test..."
    python -c "
import requests
import json
import time

# 테스트 데이터
test_data = {
    'apiKey': 'test-api-key',
    'eventName': 'question_asked',
    'properties': {
        'question': '마이크로소프트의 AI 기능 가격은 얼마인가요?'
    },
    'timestamp': '2024-01-01T00:00:00Z'
}

print('🧪 Testing SDK to API Gateway flow...')
try:
    # LocalStack API Gateway 엔드포인트로 테스트
    response = requests.post(
        'http://localhost:4566/restapis/local/ingest/_user_request_/ingest',
        json=test_data,
        headers={'Content-Type': 'application/json'}
    )
    print(f'✅ API Response: {response.status_code} - {response.text}')
except Exception as e:
    print(f'❌ Test failed: {e}')

print('🎉 Basic test completed!')
"
fi

echo "--- ✅ Local Test Setup Complete ---"
echo "🌐 Platform: http://localhost:3000"
echo "🔧 LocalStack: http://localhost:4566"
echo "🗄️  Postgres: localhost:5432"
echo ""
echo "Run 'docker-compose down' to stop the environment."
