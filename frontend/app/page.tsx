"use client";

import EmailClassifier from "@/components/EmailClassifier";
import AutoUHeader from "@/components/AutoUHeader";
import AutoULogo from "@/components/AutoULogo";

export default function Home() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50/30 to-indigo-50/30">
      <AutoUHeader />
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <EmailClassifier />
      </main>
      
      {/* Footer simples */}
      <footer className="mt-16 border-t border-gray-200 bg-white/50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <div className="flex flex-col sm:flex-row items-center justify-between text-sm text-gray-600">
            <div className="flex items-center space-x-2 mb-2 sm:mb-0">
              <AutoULogo width={120} height={40} />
              <span className="text-gray-400">•</span>
              <span>Intelligence Platform</span>
            </div>
            <div className="text-gray-500">
              Transformando complexidade em vantagem competitiva
            </div>
          </div>
        </div>
      </footer>
    </div>
  );
}
