// TODO: 이 페이지는 인증된 사용자만 접근할 수 있도록 보호되어야 합니다. (Higher-Order Component 또는 Middleware 사용)

export default function DashboardPage() {
  return (
    <main className="flex min-h-screen flex-col items-center justify-center p-24 bg-gray-50">
      <div className="w-full max-w-5xl bg-white p-8 rounded-lg shadow-md">
        <h1 className="text-3xl font-bold text-gray-800 mb-4">
          Ad-Scouter AI Dashboard
        </h1>
        <p className="text-gray-600 mb-8">
          고객님의 비즈니스 성장을 위한 데이터 인사이트를 확인하세요.
        </p>

        {/* 여기에 다양한 통계 차트와 데이터 시각화 컴포넌트가 위치하게 됩니다. */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {/* 예시 카드 1: 총 호출 비용 */}
          <div className="p-6 bg-blue-50 rounded-lg">
            <h3 className="text-lg font-semibold text-blue-800">총 호출 비용</h3>
            <p className="text-3xl font-bold text-blue-900 mt-2">$1,234.56</p>
          </div>
          
          {/* 예시 카드 2: 사용자 의도 분포 */}
          <div className="p-6 bg-green-50 rounded-lg">
            <h3 className="text-lg font-semibold text-green-800">사용자 의도 분포</h3>
            <p className="text-sm text-green-700 mt-2">구매 고려: 45%</p>
          </div>

          {/* 예시 카드 3: 발굴된 잠재 광고주 */}
          <div className="p-6 bg-purple-50 rounded-lg">
            <h3 className="text-lg font-semibold text-purple-800">발굴된 잠재 광고주</h3>
            <p className="text-3xl font-bold text-purple-900 mt-2">12</p>
          </div>
        </div>

        {/* 추가 섹션: 최근 활동 */}
        <div className="mt-8">
          <h2 className="text-2xl font-bold text-gray-800 mb-4">최근 활동</h2>
          <div className="bg-gray-50 p-6 rounded-lg">
            <div className="space-y-4">
              <div className="flex justify-between items-center">
                <span className="text-gray-700">새로운 잠재 광고주 발굴</span>
                <span className="text-sm text-gray-500">2시간 전</span>
              </div>
              <div className="flex justify-between items-center">
                <span className="text-gray-700">사용자 질문 분석 완료</span>
                <span className="text-sm text-gray-500">5시간 전</span>
              </div>
              <div className="flex justify-between items-center">
                <span className="text-gray-700">광고 매칭 성공</span>
                <span className="text-sm text-gray-500">1일 전</span>
              </div>
            </div>
          </div>
        </div>

        {/* SDK 통합 가이드 */}
        <div className="mt-8">
          <h2 className="text-2xl font-bold text-gray-800 mb-4">SDK 통합 가이드</h2>
          <div className="bg-blue-50 p-6 rounded-lg">
            <h3 className="text-lg font-semibold text-blue-800 mb-2">웹사이트에 SDK 추가하기</h3>
            <div className="bg-gray-800 text-green-400 p-4 rounded font-mono text-sm">
              <div>&lt;script&gt;</div>
              <div>&nbsp;&nbsp;window.AD_SCOUTER_API_KEY = 'your-api-key-here';</div>
              <div>&lt;/script&gt;</div>
              <div>&lt;script src="https://cdn.your-domain.com/ad-scouter-sdk.js"&gt;&lt;/script&gt;</div>
            </div>
            <p className="text-blue-700 mt-2 text-sm">
              위 코드를 웹사이트의 &lt;head&gt; 태그 안에 추가하세요.
            </p>
          </div>
        </div>
      </div>
    </main>
  );
}
