"use client";

export default function AutoUHeader() {
  return (
    <header className="w-full bg-white border-b border-gray-100 shadow-sm">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
        <div className="flex items-center justify-between">
          {/* Logo AutoU */}
          <div className="flex items-center space-x-3">
            <div className="relative">
              {/* Símbolo AutoU - círculo com "A" estilizado */}
              <div className="w-12 h-12 bg-gradient-to-br from-blue-600 via-purple-600 to-indigo-600 rounded-xl flex items-center justify-center shadow-lg transform hover:scale-105 transition-transform">
                <span className="text-white font-bold text-xl">A</span>
              </div>
              {/* Efeito de brilho */}
              <div className="absolute inset-0 bg-gradient-to-br from-blue-400 to-purple-400 rounded-xl opacity-20 blur-sm"></div>
            </div>
            <div>
              <h1 className="text-2xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
                AutoU
              </h1>
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
