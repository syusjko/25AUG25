import base64
import json
import os
import boto3
import uuid
import google.generativeai as genai

# 로컬 테스트 환경을 위한 엔드포인트 설정
endpoint_url = os.environ.get('LOCALSTACK_ENDPOINT_URL')

# boto3 클라이언트 및 환경 변수 초기화
dynamodb = boto3.resource('dynamodb', endpoint_url=endpoint_url)
STATS_TABLE_NAME = os.environ.get('STATS_TABLE_NAME', 'ad-scouter-stats')
table = dynamodb.Table(STATS_TABLE_NAME)

# Gemini API 키 설정
GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY environment variable is not set.")
genai.configure(api_key=GEMINI_API_KEY)

def get_intent_from_gemini(text):
    """
    Gemini API를 호출하여 텍스트의 의도를 분석합니다.
    """
    try:
        model = genai.GenerativeModel('gemini-pro')
        prompt = f"""
        다음 텍스트를 분석하여 사용자의 의도를 '정보 탐색', '구매 고려', '기능 문의', '단순 대화', '기타' 중 하나로 정확하게 분류해줘. 다른 설명은 붙이지 말고 분류 결과만 말해줘.
        텍스트: "{text}"
        분류:
        """
        response = model.generate_content(prompt)
        # response.prompt_feedback는 부적절한 프롬프트가 있었는지 확인하는데 사용 가능
        return response.text.strip()
    except Exception as e:
        print(f"Error calling Gemini API: {e}")
        return "분석 실패" # 에러 발생 시 기본값 반환

def handler(event, context):
    """
    Kinesis로부터 받은 레코드를 처리하여 의도를 분석하고 DynamoDB에 저장합니다.
    """
    print(f"Processing {len(event['Records'])} records from Kinesis.")
    for record in event['Records']:
        try:
            # Kinesis 레코드는 base64로 인코딩되어 있으므로 디코딩합니다.
            payload_decoded = base64.b64decode(record['kinesis']['data']).decode('utf-8')
            data = json.loads(payload_decoded)
            print(f"Decoded data: {data}")

            # SDK에서 보낸 'properties' 객체에서 질문을 추출합니다.
            # 실제 데이터 구조에 따라 이 부분은 수정이 필요할 수 있습니다.
            question_text = data.get('properties', {}).get('question', '')

            if not question_text:
                print("No 'question' field in properties. Skipping record.")
                continue

            # 1. 비식별화 처리 (Placeholder)
            # TODO: Microsoft Presidio 등 라이브러리를 사용하여 개인정보를 마스킹하는 로직 추가
            anonymized_question = question_text # 현재는 원본 그대로 사용

            # 2. Gemini API로 의도 분석
            intent = get_intent_from_gemini(anonymized_question)
            print(f"Detected intent for question '{anonymized_question[:30]}...': {intent}")

            # 3. DynamoDB에 저장할 데이터 구성
            item_to_store = {
                'customerId': data.get('apiKey'), # apiKey를 고객사 ID로 사용
                'eventId': str(uuid.uuid4()), # 각 이벤트를 고유하게 식별
                'eventName': data.get('eventName'),
                'intent': intent,
                'originalQuestion': anonymized_question,
                'timestamp': data.get('timestamp'),
                # TODO: 잠재 광고주, 비용 통계 등 추가 필드 확장 예정
            }

            # 4. DynamoDB에 저장
            table.put_item(Item=item_to_store)
            print(f"Successfully stored stats for customer {item_to_store['customerId']}")

        except Exception as e:
            # 에러가 발생해도 다른 레코드 처리에 영향을 주지 않도록 로깅만 하고 넘어갑니다.
            print(f"Error processing record: {e}")
            print(f"Problematic record data: {record['kinesis']['data']}")
            continue

    return {
        'statusCode': 200,
        'body': json.dumps(f"Successfully processed {len(event['Records'])} records.")
    }