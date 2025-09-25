#!/usr/bin/env python3
"""
간단한 Mock API 서버
로컬 테스트를 위한 Flask 기반 서버
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import threading
import time
from datetime import datetime

app = Flask(__name__)
CORS(app)

# 메모리 내 데이터 저장소
events_queue = []
processed_events = []

@app.route('/ingest', methods=['POST', 'OPTIONS'])
def ingest():
    """SDK에서 오는 데이터를 받는 엔드포인트"""
    if request.method == 'OPTIONS':
        return '', 204
    
    try:
        data = request.json
        print(f"📥 Received event: {data}")
        
        # 이벤트를 큐에 추가
        events_queue.append({
            **data,
            'received_at': datetime.now().isoformat()
        })
        
        # 백그라운드에서 처리 시뮬레이션
        threading.Thread(target=process_event, args=(data,)).start()
        
        return jsonify({
            'message': 'Event received successfully.',
            'status': 'success'
        }), 202
        
    except Exception as e:
        print(f"❌ Error processing request: {e}")
        return jsonify({'error': str(e)}), 500

def process_event(event_data):
    """이벤트 처리 시뮬레이션"""
    try:
        print(f"🔄 Processing event: {event_data.get('eventName', 'unknown')}")
        
        # 처리 시간 시뮬레이션
        time.sleep(1)
        
        # 처리된 이벤트 저장
        processed_event = {
            **event_data,
            'processed_at': datetime.now().isoformat(),
            'intent': '구매 고려',  # Mock 의도 분석
            'advertiser': 'Microsoft'  # Mock 광고주 추출
        }
        
        processed_events.append(processed_event)
        print(f"✅ Event processed: {processed_event}")
        
    except Exception as e:
        print(f"❌ Error processing event: {e}")

@app.route('/ads', methods=['POST', 'OPTIONS'])
def generate_ad():
    """광고 생성 엔드포인트"""
    if request.method == 'OPTIONS':
        return '', 204
    
    try:
        query = request.json.get('query', '')
        print(f"🎯 Generating ad for query: {query}")
        
        # Mock 광고 생성
        ad_response = {
            'advertiser': {
                'name': 'Microsoft',
                'description': 'AI 솔루션 제공업체'
            },
            'ad_content': f'"{query}"에 대한 Microsoft AI 솔루션을 확인해보세요!',
            'similarity_score': 0.85,
            'user_query': query,
            'generated_at': datetime.now().isoformat()
        }
        
        print(f"📢 Generated ad: {ad_response}")
        return jsonify(ad_response)
        
    except Exception as e:
        print(f"❌ Error generating ad: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/stats', methods=['GET'])
def get_stats():
    """통계 조회 엔드포인트"""
    try:
        stats = {
            'total_events': len(events_queue),
            'processed_events': len(processed_events),
            'pending_events': len(events_queue) - len(processed_events),
            'last_event': events_queue[-1] if events_queue else None,
            'last_processed': processed_events[-1] if processed_events else None
        }
        
        return jsonify(stats)
        
    except Exception as e:
        print(f"❌ Error getting stats: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/health', methods=['GET'])
def health():
    """헬스 체크 엔드포인트"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'events_received': len(events_queue),
        'events_processed': len(processed_events)
    })

if __name__ == '__main__':
    print("🚀 Starting Mock API Server...")
    print("📡 Endpoints:")
    print("  - POST /ingest - SDK 이벤트 수신")
    print("  - POST /ads - 광고 생성")
    print("  - GET /stats - 통계 조회")
    print("  - GET /health - 헬스 체크")
    print("=" * 50)
    
    app.run(host='0.0.0.0', port=8080, debug=True)
