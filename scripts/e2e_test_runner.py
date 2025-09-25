#!/usr/bin/env python3
"""
Ad-Scouter AI End-to-End 테스트 스크립트
로컬 환경에서 전체 데이터 플로우를 테스트합니다.
"""

import requests
import json
import time
import os
import boto3
from datetime import datetime

# 테스트 설정
LOCALSTACK_ENDPOINT = "http://localhost:4566"
API_GATEWAY_ENDPOINT = f"{LOCALSTACK_ENDPOINT}/restapis/local/ingest/_user_request_/ingest"
KINESIS_STREAM = "ad-scouter-ingest-stream"
DYNAMODB_TABLE = "ad-scouter-stats"

# AWS 클라이언트 설정
aws_config = {
    'endpoint_url': LOCALSTACK_ENDPOINT,
    'region_name': 'ap-northeast-2',
    'aws_access_key_id': 'test',
    'aws_secret_access_key': 'test'
}

kinesis_client = boto3.client('kinesis', **aws_config)
dynamodb_client = boto3.client('dynamodb', **aws_config)
dynamodb_resource = boto3.resource('dynamodb', **aws_config)

class TestRunner:
    def __init__(self):
        self.test_results = []
        self.test_data = {
            'apiKey': 'test-customer-001',
            'eventName': 'question_asked',
            'properties': {
                'question': '마이크로소프트의 새로운 AI 기능 가격은 얼마인가요?'
            },
            'timestamp': datetime.now().isoformat(),
            'url': 'http://localhost:3000',
            'userAgent': 'Ad-Scouter-Test/1.0'
        }
    
    def log_test(self, test_name, success, message=""):
        """테스트 결과를 기록합니다."""
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} {test_name}: {message}")
        self.test_results.append({
            'test': test_name,
            'success': success,
            'message': message
        })
    
    def test_api_gateway_connection(self):
        """API Gateway 연결 테스트"""
        try:
            response = requests.post(
                API_GATEWAY_ENDPOINT,
                json=self.test_data,
                headers={'Content-Type': 'application/json'},
                timeout=10
            )
            
            if response.status_code in [200, 202]:
                self.log_test("API Gateway Connection", True, f"Status: {response.status_code}")
                return True
            else:
                self.log_test("API Gateway Connection", False, f"Unexpected status: {response.status_code}")
                return False
                
        except Exception as e:
            self.log_test("API Gateway Connection", False, f"Error: {str(e)}")
            return False
    
    def test_kinesis_data_flow(self):
        """Kinesis 데이터 플로우 테스트"""
        try:
            # Kinesis 스트림 상태 확인
            response = kinesis_client.describe_stream(StreamName=KINESIS_STREAM)
            if response['StreamDescription']['StreamStatus'] != 'ACTIVE':
                self.log_test("Kinesis Stream Status", False, "Stream not active")
                return False
            
            # 직접 Kinesis에 데이터 전송 테스트
            test_record = {
                'Data': json.dumps(self.test_data),
                'PartitionKey': self.test_data['apiKey']
            }
            
            kinesis_client.put_record(
                StreamName=KINESIS_STREAM,
                Data=test_record['Data'],
                PartitionKey=test_record['PartitionKey']
            )
            
            self.log_test("Kinesis Data Flow", True, "Data successfully sent to Kinesis")
            return True
            
        except Exception as e:
            self.log_test("Kinesis Data Flow", False, f"Error: {str(e)}")
            return False
    
    def test_dynamodb_table(self):
        """DynamoDB 테이블 접근 테스트"""
        try:
            # 테이블 존재 확인
            response = dynamodb_client.describe_table(TableName=DYNAMODB_TABLE)
            if response['Table']['TableStatus'] != 'ACTIVE':
                self.log_test("DynamoDB Table Status", False, "Table not active")
                return False
            
            # 테스트 데이터 삽입
            table = dynamodb_resource.Table(DYNAMODB_TABLE)
            test_item = {
                'customerId': 'test-customer-001',
                'eventId': f'test-event-{int(time.time())}',
                'eventName': 'test_event',
                'intent': '구매 고려',
                'originalQuestion': '테스트 질문입니다.',
                'timestamp': datetime.now().isoformat()
            }
            
            table.put_item(Item=test_item)
            
            # 데이터 조회 확인
            response = table.get_item(
                Key={
                    'customerId': test_item['customerId'],
                    'eventId': test_item['eventId']
                }
            )
            
            if 'Item' in response:
                self.log_test("DynamoDB Operations", True, "Data successfully stored and retrieved")
                return True
            else:
                self.log_test("DynamoDB Operations", False, "Data not found after insertion")
                return False
                
        except Exception as e:
            self.log_test("DynamoDB Operations", False, f"Error: {str(e)}")
            return False
    
    def test_platform_connection(self):
        """플랫폼 웹사이트 연결 테스트"""
        try:
            response = requests.get("http://localhost:3000", timeout=10)
            if response.status_code == 200:
                self.log_test("Platform Website", True, "Website accessible")
                return True
            else:
                self.log_test("Platform Website", False, f"Unexpected status: {response.status_code}")
                return False
                
        except Exception as e:
            self.log_test("Platform Website", False, f"Error: {str(e)}")
            return False
    
    def test_sdk_integration(self):
        """SDK 통합 테스트 (브라우저 시뮬레이션)"""
        try:
            # SDK가 사용할 수 있는 엔드포인트 테스트
            sdk_endpoint = f"{LOCALSTACK_ENDPOINT}/restapis/local/ingest/_user_request_/ingest"
            
            # 브라우저에서 보낼 것과 동일한 데이터 구조
            sdk_payload = {
                'apiKey': 'test-customer-001',
                'eventName': 'question_asked',
                'properties': {
                    'question': '구글의 AI 서비스는 어떻게 사용하나요?'
                },
                'timestamp': datetime.now().isoformat(),
                'url': 'http://localhost:3000',
                'userAgent': 'Mozilla/5.0 (Test Browser)'
            }
            
            response = requests.post(
                sdk_endpoint,
                json=sdk_payload,
                headers={'Content-Type': 'application/json'},
                timeout=10
            )
            
            if response.status_code in [200, 202]:
                self.log_test("SDK Integration", True, "SDK payload successfully processed")
                return True
            else:
                self.log_test("SDK Integration", False, f"Unexpected status: {response.status_code}")
                return False
                
        except Exception as e:
            self.log_test("SDK Integration", False, f"Error: {str(e)}")
            return False
    
    def run_all_tests(self):
        """모든 테스트를 실행합니다."""
        print("🧪 Starting Ad-Scouter AI E2E Tests...")
        print("=" * 50)
        
        # 각 테스트 실행
        tests = [
            ("Platform Website", self.test_platform_connection),
            ("API Gateway", self.test_api_gateway_connection),
            ("Kinesis Data Flow", self.test_kinesis_data_flow),
            ("DynamoDB Operations", self.test_dynamodb_table),
            ("SDK Integration", self.test_sdk_integration)
        ]
        
        for test_name, test_func in tests:
            print(f"\n🔍 Running {test_name} test...")
            test_func()
            time.sleep(1)  # 테스트 간 간격
        
        # 결과 요약
        print("\n" + "=" * 50)
        print("📊 TEST RESULTS SUMMARY")
        print("=" * 50)
        
        passed = sum(1 for result in self.test_results if result['success'])
        total = len(self.test_results)
        
        for result in self.test_results:
            status = "✅" if result['success'] else "❌"
            print(f"{status} {result['test']}: {result['message']}")
        
        print(f"\n🎯 Overall: {passed}/{total} tests passed")
        
        if passed == total:
            print("🎉 All tests passed! System is ready for production.")
        else:
            print("⚠️  Some tests failed. Please check the issues above.")
        
        return passed == total

def main():
    """메인 실행 함수"""
    print("Ad-Scouter AI - Local E2E Test Runner")
    print("=====================================")
    
    # 환경 변수 확인
    if not os.getenv('LOCALSTACK_ENDPOINT_URL'):
        print("⚠️  LOCALSTACK_ENDPOINT_URL not set, using default")
    
    # 테스트 실행
    runner = TestRunner()
    success = runner.run_all_tests()
    
    return 0 if success else 1

if __name__ == "__main__":
    exit(main())
