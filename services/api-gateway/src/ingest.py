import json
import os
import boto3 # AWS SDK for Python

# 로컬 테스트 환경을 위한 엔드포인트 설정
# LOCALSTACK_ENDPOINT_URL 환경 변수가 있으면 해당 URL을 사용
endpoint_url = os.environ.get('LOCALSTACK_ENDPOINT_URL')

# Kinesis 클라이언트 초기화
kinesis_client = boto3.client('kinesis', endpoint_url=endpoint_url)
# 환경 변수에서 스트림 이름을 가져옵니다. Terraform에서 설정할 예정입니다.
STREAM_NAME = os.environ.get('KINESIS_STREAM_NAME', 'ad-scouter-ingest-stream')

def handler(event, context):
    """
    API Gateway를 통해 SDK로부터 데이터 수집 요청을 처리하고,
    검증된 데이터를 Kinesis 데이터 스트림으로 전송합니다.
    """
    # CORS preflight 요청(OPTIONS) 처리 (기존과 동일)
    if event.get('requestContext', {}).get('http', {}).get('method') == 'OPTIONS':
        return {
            'statusCode': 204,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'POST, OPTIONS',
                'Access-Control-Allow-Headers': 'Content-Type'
            }
        }
    
    try:
        body = json.loads(event.get('body', '{}'))
        api_key = body.get('apiKey')
        event_name = body.get('eventName')
        
        # 기본 유효성 검사
        if not api_key:
            return {'statusCode': 401, 'body': json.dumps({'message': 'Unauthorized: API Key is missing.'})}
        
        if not event_name:
            return {'statusCode': 400, 'body': json.dumps({'message': 'Bad Request: eventName is missing.'})}
        
        if not STREAM_NAME:
            raise ValueError("KINESIS_STREAM_NAME environment variable is not set.")

        # --- Kinesis로 데이터 전송 ---
        # 데이터를 Kinesis 스트림으로 보냅니다.
        # PartitionKey는 데이터를 샤드에 분산시키는 역할을 합니다. apiKey를 사용해 동일 고객사의 데이터는 동일 샤드로 보내도록 합니다.
        response = kinesis_client.put_record(
            StreamName=STREAM_NAME,
            Data=json.dumps(body), # 전체 요청 본문을 데이터로 사용
            PartitionKey=api_key
        )
        
        print(f"Successfully put record to Kinesis. ShardId: {response['ShardId']}, SequenceNumber: {response['SequenceNumber']}")

        # 성공 응답 반환 (기존과 동일)
        return {
            'statusCode': 202,
            'headers': {'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*'},
            'body': json.dumps({'message': 'Event received successfully.'})
        }

    except json.JSONDecodeError:
        return {'statusCode': 400, 'body': json.dumps({'message': 'Bad Request: Invalid JSON format.'})}
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return {'statusCode': 500, 'body': json.dumps({'message': 'Internal Server Error.'})}