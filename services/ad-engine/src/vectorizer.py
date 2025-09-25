import json
import os
import google.generativeai as genai
# import psycopg2 # PostgreSQL 어댑터

# Gemini API 키 설정
GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

# --- DB 연결 정보 (환경 변수로 관리) ---
DB_HOST = os.environ.get('DB_HOST')
DB_NAME = os.environ.get('DB_NAME')
DB_USER = os.environ.get('DB_USER')
DB_PASSWORD = os.environ.get('DB_PASSWORD')

def get_text_embedding(text):
    """
    Gemini Embedding API를 호출하여 텍스트를 벡터로 변환합니다.
    """
    if not GEMINI_API_KEY:
        raise ValueError("GEMINI_API_KEY is not configured for vectorizer.")

    try:
        # 최신 임베딩 모델 사용
        result = genai.embed_content(
            model="models/text-embedding-004", # 또는 최신 모델
            content=text,
            task_type="RETRIEVAL_DOCUMENT"
        )
        return result['embedding']
    except Exception as e:
        print(f"Error calling Gemini Embedding API: {e}")
        return None

def handler(event, context):
    """
    (가상) DB 트리거로부터 받은 광고주 정보를 벡터로 변환하고,
    다시 DB에 업데이트합니다.
    """
    print(f"Processing vectorization request: {json.dumps(event)}")
    
    # 실제 구현에서는 DB 트리거 이벤트를 받아 처리
    # 현재는 테스트용으로 직접 광고주 정보를 받아 처리
    advertiser_info = event.get('advertiser_info', {})
    advertiser_id = advertiser_info.get('id')
    description = advertiser_info.get('description', '')
    
    if not advertiser_id or not description:
        return {
            'statusCode': 400,
            'body': json.dumps({'error': 'Missing advertiser_id or description'})
        }
    
    try:
        # 1. 광고주 정보 텍스트를 벡터로 변환
        embedding_vector = get_text_embedding(description)
        
        if embedding_vector is None:
            return {
                'statusCode': 500,
                'body': json.dumps({'error': 'Failed to generate embedding'})
            }
        
        # 2. DB에 연결하여 해당 광고주의 'embedding' 컬럼을 업데이트
        # conn = psycopg2.connect(host=DB_HOST, dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD)
        # cur = conn.cursor()
        # sql = "UPDATE advertisers SET embedding = %s WHERE id = %s"
        # cur.execute(sql, (embedding_vector, advertiser_id))
        # conn.commit()
        # cur.close()
        # conn.close()
        
        print(f"Successfully vectorized and updated advertiser ID: {advertiser_id}")
        
        return {
            'statusCode': 200,
            'body': json.dumps({
                'status': 'success',
                'advertiser_id': advertiser_id,
                'vector_dimension': len(embedding_vector)
            })
        }
        
    except Exception as e:
        print(f"Error processing vectorization: {e}")
        return {
            'statusCode': 500,
            'body': json.dumps({'error': 'Vectorization failed'})
        }