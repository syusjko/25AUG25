/**
 * Ad-Scouter AI Analytics SDK v0.1
 * * 이 SDK는 고객사 웹사이트에 설치되어 사용자 상호작용 데이터를
 * Ad-Scouter AI 분석 서버로 안전하게 전송하는 역할을 합니다.
 */
(function(window) {
    // SDK가 이미 로드되었는지 확인하여 중복 실행을 방지합니다.
    if (window.adScouter) {
        return;
    }

    const AD_SCOUTER_API_ENDPOINT = 'https://api.your-domain.com/ingest'; // 최종 데이터 수집 API 엔드포인트

    /**
     * SDK의 핵심 기능을 담당하는 AdScouter 클래스
     */
    class AdScouter {
        constructor(apiKey) {
            if (!apiKey) {
                throw new Error('Ad-Scouter AI: API Key is required.');
            }
            this.apiKey = apiKey;
            this.initialized = false;
            console.log('Ad-Scouter AI SDK loaded.');
        }

        /**
         * SDK를 초기화하고, 필수 정보를 설정합니다.
         * @param {object} options - 초기화 옵션 객체
         */
        init(options = {}) {
            this.config = { ...options };
            this.initialized = true;
            console.log('Ad-Scouter AI SDK initialized with API Key:', this.apiKey);
            
            // 초기화 시 페이지 뷰 이벤트를 자동으로 전송할 수 있습니다.
            // this.track('pageview', { url: window.location.href });
        }

        /**
         * 추적할 이벤트를 서버로 전송합니다.
         * @param {string} eventName - 추적할 이벤트의 이름 (예: 'question_asked', 'answer_received')
         * @param {object} properties - 이벤트와 관련된 추가 데이터
         */
        track(eventName, properties = {}) {
            if (!this.initialized) {
                console.error('Ad-Scouter AI: Please call init() before tracking events.');
                return;
            }

            const payload = {
                apiKey: this.apiKey,
                eventName: eventName,
                properties: properties,
                timestamp: new Date().toISOString(),
                url: window.location.href,
                userAgent: navigator.userAgent,
            };

            console.log('Tracking event:', payload);

            // Fetch API를 사용하여 비동기적으로 데이터를 서버에 전송합니다.
            // navigator.sendBeacon을 사용하면 페이지 이탈 시에도 데이터 전송을 보장할 수 있습니다.
            if (navigator.sendBeacon) {
                const blob = new Blob([JSON.stringify(payload)], { type: 'application/json' });
                navigator.sendBeacon(AD_SCOUTER_API_ENDPOINT, blob);
            } else {
                fetch(AD_SCOUTER_API_ENDPOINT, {
                    method: 'POST',
                    body: JSON.stringify(payload),
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    keepalive: true // 페이지가 닫혀도 요청을 완료하도록 시도
                });
            }
        }
    }

    // 전역 adScouter 객체를 생성하여 외부에서 사용할 수 있도록 합니다.
    window.adScouter = new AdScouter(window.AD_SCOUTER_API_KEY);

})(window);
