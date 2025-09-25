import base64
import json
import os
import boto3
import uuid

# Google Gemini API 라이브러리 설치 필요
# (Lambda Layer 또는 배포 패키지에 포함시켜야 합니다)
# import google.generativeai as genai

# boto3 클라이언트 및 환경 변수 초기화
dynamodb = boto3.resource('dynamodb')
STATS_TABLE_NAME = os.environ.get('STATS_TABLE_NAME')
table = dynamodb.Table(STATS_TABLE_NAME)

# genai.configure(api_key="YOUR_GEMINI_API_KEY") # 실제 키로 교체 필요

def get_intent_from_gemini(text):
    """
    Gemini API를 호출하여 텍스트의 의도를 분석합니다.
    (실제 API 호출 부분은 주석 처리되어 있습니다. 로컬 테스트 및 키 설정 후 활성화하세요.)
    """
    # --- 실제 Gemini API 호출 예시 ---
    # model = genai.GenerativeModel('gemini-pro')
    # prompt = f"""
    # 다음 텍스트를 분석하여 사용자의 의도를 '정보 탐색', '구매 고려', '기능 문의', '단순 대화', '기타' 중 하나로 분류해줘.
    # 텍스트: "{text}"
    # 분류:
    # """
    # response = model.generate_content(prompt)
    # return response.text.strip()
    
    # --- 임시 모의(Mock) 응답 ---
    # 실제 API 연동 전 테스트를 위한 코드입니다.
    if "얼마" in text or "가격" in text:
        return "구매 고려"
    elif "어떻게" in text or "방법" in text:
        return "기능 문의"
    else:
        return "정보 탐색"


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
                'eventId': str(uuid.uuid4()),     # 각 이벤트를 고유하게 식별
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
