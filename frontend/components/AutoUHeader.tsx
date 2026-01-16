"use client";

import AutoULogo from "./AutoULogo";

export default function AutoUHeader() {
  return (
    <header className="w-full bg-white border-b border-gray-100 shadow-sm">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
        <div className="flex items-center justify-between">
          {/* Logo AutoU */}
          <div className="flex items-center space-x-4">
            <div className="flex items-center">
              <AutoULogo width={165} height={55} className="transition-transform hover:scale-105" />
            </div>
            <div className="hidden sm:block">
              <p className="text-xs text-gray-500 font-medium">Intelligence Platform</p>
            </div>
          </div>

          {/* Badge de Status */}
          <div className="hidden sm:flex items-center space-x-2 px-4 py-2 bg-gradient-to-r from-green-50 to-emerald-50 rounded-full border border-green-200">
            <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse"></div>
            <span className="text-sm font-semibold text-green-700">Sistema Ativo</span>
          </div>
        </div>
      </div>
    </header>
  );
}
