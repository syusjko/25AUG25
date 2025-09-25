import json
import os

def handler(event, context):
    """
    API Gateway를 통해 SDK로부터 데이터 수집 요청을 처리하는 Lambda 핸들러.
    
    - 요청 본문(body)을 파싱합니다.
    - 필수 필드 (apiKey, eventName)의 존재 여부를 검증합니다.
    - CORS 처리를 위한 헤더를 포함하여 응답을 반환합니다.
    """
    print(f"Received event: {json.dumps(event)}")

    # CORS preflight 요청(OPTIONS)에 대한 처리
    if event.get('requestContext', {}).get('http', {}).get('method') == 'OPTIONS':
        return {
            'statusCode': 204,
            'headers': {
                'Access-Control-Allow-Origin': '*', # 실제 프로덕션에서는 허용된 도메인으로 제한해야 합니다.
                'Access-Control-Allow-Methods': 'POST, OPTIONS',
                'Access-Control-Allow-Headers': 'Content-Type'
            }
        }

    try:
        # 요청 본문 파싱
        body = json.loads(event.get('body', '{}'))

        api_key = body.get('apiKey')
        event_name = body.get('eventName')

        # --- 기본 유효성 검사 ---
        # 보안 강화: 실제로는 DB와 연동하여 유효한 API 키인지 검증해야 합니다.
        if not api_key:
            return {
                'statusCode': 401,
                'body': json.dumps({'message': 'Unauthorized: API Key is missing.'})
            }
        
        if not event_name:
             return {
                'statusCode': 400,
                'body': json.dumps({'message': 'Bad Request: eventName is missing.'})
            }

        # TODO: Phase 1.3에서 이 데이터를 Kinesis Stream으로 전송하는 로직 추가 예정
        print(f"Successfully processed event '{event_name}' for API Key '{api_key[:5]}...'")


        # 성공 응답 반환
        return {
            'statusCode': 202, # Accepted: 요청이 성공적으로 접수되었음을 의미
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*' # 프로덕션에서는 특정 도메인으로 제한
            },
            'body': json.dumps({'message': 'Event received successfully.'})
        }

    except json.JSONDecodeError:
        return {
            'statusCode': 400,
            'body': json.dumps({'message': 'Bad Request: Invalid JSON format.'})
        }
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return {
            'statusCode': 500,
            'body': json.dumps({'message': 'Internal Server Error.'})
        }
