import json
import os
import google.generativeai as genai

# Gemini API 키 설정
GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

def handler(event, context):
    """
    DynamoDB 스트림으로부터 받은 레코드를 처리하여 잠재 광고주를 식별하고
    영업 전략 생성을 시작합니다.
    """
    print(f"Processing {len(event['Records'])} records from DynamoDB Stream.")

    for record in event['Records']:
        try:
            # 이벤트 타입이 INSERT(새로운 데이터 추가)일 때만 처리
            if record.get('eventName') == 'INSERT':
                # DynamoDB 스트림 레코드에서 새로운 데이터(NewImage)를 추출
                new_image = record['dynamodb']['NewImage']
                
                # 데이터 타입에 맞게 파싱 (DynamoDB는 타입을 명시함)
                intent = new_image.get('intent', {}).get('S')
                question = new_image.get('originalQuestion', {}).get('S')
                customer_id = new_image.get('customerId', {}).get('S')
                event_name = new_image.get('eventName', {}).get('S')
                
                print(f"New record received: Customer='{customer_id}', Event='{event_name}', Intent='{intent}', Question='{question}'")

                # 1. 잠재 광고주 발굴 조건 확인
                # 예: 의도가 '구매 고려'이고, 질문에 특정 제품/서비스가 언급될 때
                if intent == '구매 고려':
                    print(f"Found potential lead with '구매 고려' intent. Starting scouting process...")
                    
                    # 2. 잠재 광고주 정보 추출 (Gemini API 활용)
                    # TODO: Gemini를 호출하여 질문에서 회사/제품/서비스 이름 추출
                    potential_advertiser = extract_advertiser_from_question(question)
                    
                    if potential_advertiser:
                        print(f"Identified potential advertiser: {potential_advertiser}")
                        # 3. 광고주 정보 검색 및 영업 전략 생성
                        # TODO: Gemini (with Search)를 호출하여 회사 정보, 연락처 등 검색
                        # TODO: 검색된 정보를 바탕으로 맞춤형 이메일, 랜딩페이지 컨셉 생성
                        # TODO: 생성된 결과를 S3에 저장하고 영업팀에 SES로 알림 전송
                        
                        # 현재는 로그로만 출력 (실제 구현 시 S3, SES 연동)
                        scouting_result = {
                            'customer_id': customer_id,
                            'potential_advertiser': potential_advertiser,
                            'original_question': question,
                            'scouting_timestamp': context.aws_request_id,
                            'status': 'identified'
                        }
                        print(f"Scouting result: {json.dumps(scouting_result, ensure_ascii=False)}")
                    else:
                        print("Could not identify specific advertiser from question. Skipping.")
                else:
                    print("Record does not meet scouting criteria. Skipping.")

        except Exception as e:
            print(f"Error processing record: {e}")
            continue
            
    return {
        'statusCode': 200,
        'body': json.dumps(f"Successfully processed {len(event['Records'])} records.")
    }

def extract_advertiser_from_question(question):
    """
    Gemini API를 사용하여 질문에서 잠재 광고주 이름(회사/제품)을 추출합니다.
    """
    if not GEMINI_API_KEY:
        print("GEMINI_API_KEY is not configured. Skipping advertiser extraction.")
        return None
        
    try:
        model = genai.GenerativeModel('gemini-pro')
        prompt = f"""
        다음 문장에서 언급된 가장 핵심적인 회사 또는 제품 이름을 하나만 정확히 추출해줘. 다른 설명 없이 이름만 말해줘. 만약 없다면 '없음'이라고 답해줘.
        문장: "{question}"
        회사/제품 이름:
        """
        response = model.generate_content(prompt)
        result = response.text.strip()
        return result if result != "없음" else None
    except Exception as e:
        print(f"Error calling Gemini API for extraction: {e}")
        return None
