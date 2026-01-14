"use client";

import { ClassificationResult } from "@/types/api";

interface ResultDisplayProps {
  result: ClassificationResult;
}

export default function ResultDisplay({ result }: ResultDisplayProps) {
  const isProductive = result.label === "Produtivo";
  const confidencePercent = Math.round(result.confidence * 100);

  return (
    <div className="bg-white rounded-lg shadow-lg p-6 space-y-6">
      <h2 className="text-2xl font-bold text-gray-900 mb-4">
        📊 Resultado da Classificação
      </h2>

      {/* Classification Badge */}
      <div className="flex items-center justify-between p-4 rounded-lg bg-gray-50">
        <div className="flex items-center space-x-3">
          <span className={`text-3xl ${isProductive ? "📋" : "💬"}`}>
            {isProductive ? "📋" : "💬"}
          </span>
          <div>
            <div className="text-sm text-gray-600">Categoria:</div>
            <div className={`text-2xl font-bold ${
              isProductive ? "text-green-600" : "text-orange-600"
            }`}>
              {result.label}
            </div>
          </div>
        </div>
        <div className="text-right">
          <div className="text-sm text-gray-600">Confiança:</div>
          <div className="text-2xl font-bold text-blue-600">
            {confidencePercent}%
          </div>
        </div>
      </div>

      {/* Confidence Bar */}
      <div>
        <div className="flex justify-between text-sm text-gray-600 mb-1">
          <span>Nível de confiança</span>
          <span>{confidencePercent}%</span>
        </div>
        <div className="w-full bg-gray-200 rounded-full h-3">
          <div
            className={`h-3 rounded-full transition-all ${
              confidencePercent >= 80
                ? "bg-green-500"
                : confidencePercent >= 60
                ? "bg-yellow-500"
                : "bg-orange-500"
            }`}
            style={{ width: `${confidencePercent}%` }}
          ></div>
        </div>
      </div>

      {/* Suggested Reply */}
      <div className="border-t pt-6">
        <h3 className="text-lg font-semibold text-gray-900 mb-3">
          💡 Resposta Sugerida
        </h3>
        <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
          <pre className="whitespace-pre-wrap text-gray-800 font-sans text-sm leading-relaxed">
            {result.suggested_reply}
          </pre>
        </div>
        <button
          onClick={() => {
            navigator.clipboard.writeText(result.suggested_reply);
            alert("Resposta copiada para a área de transferência!");
          }}
          className="mt-3 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors text-sm"
        >
          📋 Copiar Resposta
        </button>
      </div>
    </div>
  );
}
