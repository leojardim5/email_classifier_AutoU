"use client";

import { ResultDisplayProps } from "@/types";

export default function ResultDisplay({ result }: ResultDisplayProps) {
  const isProductive = result.label === "Produtivo";
  const confidencePercent = Math.round(result.confidence * 100);

  return (
    <div className="bg-white rounded-xl shadow-autou border border-gray-100 p-8 space-y-6">
      <div className="flex items-center space-x-3 mb-6">
        <div className="w-12 h-12 bg-gradient-to-br from-blue-600 to-purple-600 rounded-xl flex items-center justify-center">
          <span className="text-white text-2xl">📊</span>
        </div>
        <h2 className="text-3xl font-bold text-gray-900">
          Resultado da Classificação
        </h2>
      </div>

      {/* Classification Badge */}
      <div className={`flex items-center justify-between p-6 rounded-xl border-2 ${
        isProductive 
          ? "bg-gradient-to-r from-green-50 to-emerald-50 border-green-200" 
          : "bg-gradient-to-r from-orange-50 to-amber-50 border-orange-200"
      }`}>
        <div className="flex items-center space-x-4">
          <div className={`w-16 h-16 rounded-xl flex items-center justify-center ${
            isProductive 
              ? "bg-gradient-to-br from-green-500 to-emerald-600" 
              : "bg-gradient-to-br from-orange-500 to-amber-600"
          } shadow-lg`}>
            <span className="text-3xl">{isProductive ? "📋" : "💬"}</span>
          </div>
          <div>
            <div className="text-xs font-semibold text-gray-600 uppercase tracking-wide mb-1">Categoria</div>
            <div className={`text-3xl font-bold ${
              isProductive ? "text-green-700" : "text-orange-700"
            }`}>
              {result.label}
            </div>
          </div>
        </div>
        <div className="text-right">
          <div className="text-xs font-semibold text-gray-600 uppercase tracking-wide mb-1">Confiança</div>
          <div className="text-3xl font-bold text-autou-gradient">
            {confidencePercent}%
          </div>
        </div>
      </div>

      {/* Confidence Bar */}
      <div className="bg-gray-50 rounded-xl p-4">
        <div className="flex justify-between text-sm font-semibold text-gray-700 mb-2">
          <span>Nível de confiança da IA</span>
          <span className="text-autou-gradient">{confidencePercent}%</span>
        </div>
        <div className="w-full bg-gray-200 rounded-full h-4 overflow-hidden">
          <div
            className={`h-4 rounded-full transition-all duration-500 ${
              confidencePercent >= 80
                ? "bg-gradient-to-r from-green-500 to-emerald-600"
                : confidencePercent >= 60
                ? "bg-gradient-to-r from-yellow-500 to-orange-500"
                : "bg-gradient-to-r from-orange-500 to-red-500"
            } shadow-sm`}
            style={{ width: `${confidencePercent}%` }}
          ></div>
        </div>
      </div>

      {/* Suggested Reply */}
      <div className="border-t border-gray-200 pt-6">
        <div className="flex items-center space-x-3 mb-4">
          <div className="w-10 h-10 bg-gradient-to-br from-blue-600 to-purple-600 rounded-lg flex items-center justify-center">
            <span className="text-white text-xl">💡</span>
          </div>
          <h3 className="text-xl font-bold text-gray-900">
            Resposta Sugerida pela IA
          </h3>
        </div>
        <div className="bg-gradient-to-br from-blue-50 via-indigo-50 to-purple-50 border-2 border-blue-200 rounded-xl p-6">
          <pre className="whitespace-pre-wrap text-gray-800 font-sans text-base leading-relaxed">
            {result.suggested_reply}
          </pre>
        </div>
        <button
          onClick={() => {
            navigator.clipboard.writeText(result.suggested_reply);
            alert("Resposta copiada para a área de transferência!");
          }}
          className="mt-4 px-6 py-3 bg-gradient-to-r from-blue-600 to-purple-600 text-white rounded-xl hover:shadow-lg transform hover:scale-105 transition-all font-semibold text-sm flex items-center space-x-2"
        >
          <span>📋</span>
          <span>Copiar Resposta</span>
        </button>
      </div>
    </div>
  );
}
