import Link from 'next/link';

export default function HomePage() {
  return (
    <main className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      {/* Navigation */}
      <nav className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between h-16">
            <div className="flex items-center">
              <h1 className="text-2xl font-bold text-gray-900">Ad-Scouter AI</h1>
            </div>
            <div className="flex items-center space-x-4">
              <Link href="/login" className="text-gray-700 hover:text-gray-900">
                로그인
              </Link>
              <Link 
                href="/signup" 
                className="bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-blue-700"
              >
                무료 시작하기
              </Link>
            </div>
          </div>
        </div>
      </nav>

      {/* Hero Section */}
      <section className="py-20">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <h1 className="text-5xl font-bold text-gray-900 mb-6">
            AI로 잠재 광고주를<br />
            <span className="text-blue-600">자동으로 발굴</span>하세요
          </h1>
          <p className="text-xl text-gray-600 mb-8 max-w-3xl mx-auto">
            사용자의 질문을 분석하여 구매 의도가 높은 잠재 고객을 자동으로 식별하고, 
            맞춤형 광고를 실시간으로 제공하는 혁신적인 AI 플랫폼입니다.
          </p>
          <div className="flex justify-center space-x-4">
            <Link 
              href="/signup" 
              className="bg-blue-600 text-white px-8 py-3 rounded-lg text-lg font-semibold hover:bg-blue-700"
            >
              무료로 시작하기
            </Link>
            <Link 
              href="#features" 
              className="bg-white text-blue-600 px-8 py-3 rounded-lg text-lg font-semibold border-2 border-blue-600 hover:bg-blue-50"
            >
              더 알아보기
            </Link>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section id="features" className="py-20 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-4xl font-bold text-gray-900 mb-4">
              강력한 기능들
            </h2>
            <p className="text-xl text-gray-600">
              비즈니스 성장을 위한 모든 도구를 한 곳에서
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            <div className="text-center p-6">
              <div className="bg-blue-100 w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4">
                <span className="text-2xl">🧠</span>
              </div>
              <h3 className="text-xl font-semibold text-gray-900 mb-2">AI 의도 분석</h3>
              <p className="text-gray-600">
                Gemini AI를 활용하여 사용자의 질문에서 구매 의도를 정확하게 분석합니다.
              </p>
            </div>

            <div className="text-center p-6">
              <div className="bg-green-100 w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4">
                <span className="text-2xl">🎯</span>
              </div>
              <h3 className="text-xl font-semibold text-gray-900 mb-2">자동 고객 발굴</h3>
              <p className="text-gray-600">
                잠재 광고주를 자동으로 식별하고 영업팀에 실시간으로 알림을 보냅니다.
              </p>
            </div>

            <div className="text-center p-6">
              <div className="bg-purple-100 w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4">
                <span className="text-2xl">📊</span>
              </div>
              <h3 className="text-xl font-semibold text-gray-900 mb-2">실시간 대시보드</h3>
              <p className="text-gray-600">
                모든 데이터와 성과를 한눈에 확인할 수 있는 직관적인 대시보드를 제공합니다.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* How it Works Section */}
      <section className="py-20 bg-gray-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-4xl font-bold text-gray-900 mb-4">
              작동 원리
            </h2>
            <p className="text-xl text-gray-600">
              3단계로 간단하게 시작하세요
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            <div className="text-center">
              <div className="bg-blue-600 text-white w-12 h-12 rounded-full flex items-center justify-center mx-auto mb-4 text-xl font-bold">
                1
              </div>
              <h3 className="text-xl font-semibold text-gray-900 mb-2">SDK 설치</h3>
              <p className="text-gray-600">
                웹사이트에 간단한 스크립트 태그만 추가하면 됩니다.
              </p>
            </div>

            <div className="text-center">
              <div className="bg-blue-600 text-white w-12 h-12 rounded-full flex items-center justify-center mx-auto mb-4 text-xl font-bold">
                2
              </div>
              <h3 className="text-xl font-semibold text-gray-900 mb-2">데이터 수집</h3>
              <p className="text-gray-600">
                사용자의 질문과 상호작용이 자동으로 분석됩니다.
              </p>
            </div>

            <div className="text-center">
              <div className="bg-blue-600 text-white w-12 h-12 rounded-full flex items-center justify-center mx-auto mb-4 text-xl font-bold">
                3
              </div>
              <h3 className="text-xl font-semibold text-gray-900 mb-2">수익 창출</h3>
              <p className="text-gray-600">
                잠재 고객 발굴과 맞춤형 광고로 비즈니스가 성장합니다.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20 bg-blue-600">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <h2 className="text-4xl font-bold text-white mb-4">
            지금 시작하세요
          </h2>
          <p className="text-xl text-blue-100 mb-8">
            무료 체험으로 Ad-Scouter AI의 강력함을 경험해보세요
          </p>
          <Link 
            href="/signup" 
            className="bg-white text-blue-600 px-8 py-3 rounded-lg text-lg font-semibold hover:bg-gray-100"
          >
            무료로 시작하기
          </Link>
        </div>
      </section>

      {/* Footer */}
      <footer className="bg-gray-900 text-white py-12">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center">
            <h3 className="text-2xl font-bold mb-4">Ad-Scouter AI</h3>
            <p className="text-gray-400 mb-4">
              AI로 비즈니스를 혁신하는 플랫폼
            </p>
            <p className="text-sm text-gray-500">
              © 2024 Ad-Scouter AI. All rights reserved.
            </p>
          </div>
        </div>
      </footer>
    </main>
  );
}