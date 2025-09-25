import json
import os
import math
# import psycopg2
# import google.generativeai as genai

# genai.configure(api_key="YOUR_GEMINI_API_KEY")

# --- DB 연결 정보 ---
# DB_HOST = os.environ.get('DB_HOST')
# DB_NAME = os.environ.get('DB_NAME')
# DB_USER = os.environ.get('DB_USER')
# DB_PASSWORD = os.environ.get('DB_PASSWORD')

def cosine_similarity(vec_a, vec_b):
    """
    두 벡터 간의 코사인 유사도를 계산합니다.
    """
    if len(vec_a) != len(vec_b):
        return 0.0
    
    dot_product = sum(a * b for a, b in zip(vec_a, vec_b))
    magnitude_a = math.sqrt(sum(a * a for a in vec_a))
    magnitude_b = math.sqrt(sum(b * b for b in vec_b))
    
    if magnitude_a == 0 or magnitude_b == 0:
        return 0.0
    
    return dot_product / (magnitude_a * magnitude_b)

def get_text_embedding(text):
    """
    Gemini Embedding API를 호출하여 텍스트를 벡터로 변환합니다.
    """
    # result = genai.embed_content(
    #     model="models/embedding-001",
    #     content=text,
    #     task_type="RETRIEVAL_QUERY" # 사용자 질문이므로 'RETRIEVAL_QUERY' 사용
    # )
    # return result['embedding']
    
    # --- 임시 모의(Mock) 벡터 ---
    return [0.1] * 768

def find_best_matching_advertiser(user_query_vector):
    """
    사용자 질문 벡터와 가장 유사한 광고주를 찾습니다.
    """
    # 실제 구현에서는 DB에서 모든 광고주의 벡터를 가져와 비교
    # 현재는 Mock 데이터로 테스트
    
    mock_advertisers = [
        {
            'id': 1,
            'name': 'Microsoft',
            'description': 'Microsoft AI and cloud services for enterprise solutions',
            'embedding': [0.2] * 768,
            'ad_template': 'Microsoft의 AI 솔루션으로 비즈니스를 혁신하세요! 무료 체험 신청'
        },
        {
            'id': 2,
            'name': 'Google',
            'description': 'Google Cloud Platform and AI services for businesses',
            'embedding': [0.3] * 768,
            'ad_template': 'Google Cloud로 스케일링하세요! 지금 시작하면 크레딧 제공'
        },
        {
            'id': 3,
            'name': 'Amazon',
            'description': 'Amazon Web Services cloud computing platform',
            'embedding': [0.15] * 768,
            'ad_template': 'AWS로 클라우드 여정을 시작하세요! 신규 고객 특별 혜택'
        }
    ]
    
    best_match = None
    best_similarity = 0.0
    
    for advertiser in mock_advertisers:
        similarity = cosine_similarity(user_query_vector, advertiser['embedding'])
        if similarity > best_similarity:
            best_similarity = similarity
            best_match = advertiser
    
    return best_match, best_similarity

def generate_personalized_ad(advertiser, user_query):
    """
    Gemini API를 사용하여 사용자 질문에 맞춤화된 광고를 생성합니다.
    """
    # --- 실제 Gemini API 호출 예시 ---
    # model = genai.GenerativeModel('gemini-pro')
    # prompt = f"""
    # 다음 정보를 바탕으로 사용자 질문에 맞는 맞춤형 광고를 생성해주세요:
    # 
    # 광고주: {advertiser['name']}
    # 광고주 설명: {advertiser['description']}
    # 사용자 질문: {user_query}
    # 기본 템플릿: {advertiser['ad_template']}
    # 
    # 요구사항:
    # - 사용자의 질문 맥락을 반영
    # - 자연스럽고 매력적인 문구
    # - 한국어로 작성
    # - 50자 이내로 간결하게
    # """
    # response = model.generate_content(prompt)
    # return response.text.strip()
    
    # --- 임시 Mock 응답 ---
    return f"{advertiser['name']}의 솔루션이 궁금하시군요! {advertiser['ad_template']}"

def handler(event, context):
    """
    사용자 질문을 받아 가장 적합한 광고를 생성하고 반환합니다.
    """
    print(f"Received ad generation request: {json.dumps(event)}")
    
    try:
        # CORS preflight 요청 처리
        if event.get('requestContext', {}).get('http', {}).get('method') == 'OPTIONS':
            return {
                'statusCode': 204,
                'headers': {
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Methods': 'POST, OPTIONS',
                    'Access-Control-Allow-Headers': 'Content-Type'
                }
            }
        
        # 요청 본문 파싱
        body = json.loads(event.get('body', '{}'))
        user_query = body.get('query', '')
        
        if not user_query:
            return {
                'statusCode': 400,
                'headers': {'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*'},
                'body': json.dumps({'error': 'Query parameter is required'})
            }
        
        # 1. 사용자 질문을 벡터로 변환
        user_query_vector = get_text_embedding(user_query)
        
        # 2. 가장 유사한 광고주 찾기
        best_advertiser, similarity_score = find_best_matching_advertiser(user_query_vector)
        
        if not best_advertiser:
            return {
                'statusCode': 404,
                'headers': {'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*'},
                'body': json.dumps({'error': 'No matching advertiser found'})
            }
        
        # 3. 맞춤형 광고 생성
        personalized_ad = generate_personalized_ad(best_advertiser, user_query)
        
        # 4. 응답 구성
        response = {
            'advertiser': {
                'id': best_advertiser['id'],
                'name': best_advertiser['name'],
                'description': best_advertiser['description']
            },
            'ad_content': personalized_ad,
            'similarity_score': similarity_score,
            'user_query': user_query
        }
        
        print(f"Generated ad for {best_advertiser['name']} with similarity {similarity_score:.3f}")
        
        return {
            'statusCode': 200,
            'headers': {'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*'},
            'body': json.dumps(response, ensure_ascii=False)
        }
        
    except json.JSONDecodeError:
        return {
            'statusCode': 400,
            'headers': {'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*'},
            'body': json.dumps({'error': 'Invalid JSON format'})
        }
    except Exception as e:
        print(f"Error generating ad: {e}")
        return {
            'statusCode': 500,
            'headers': {'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*'},
            'body': json.dumps({'error': 'Internal server error'})
        }
