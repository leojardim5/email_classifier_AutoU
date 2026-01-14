"use client";

import { ClassificationResult } from "@/types/api";

interface HistoryItem {
  id: string;
  timestamp: Date;
  input: string;
  result: ClassificationResult;
}

interface HistoryListProps {
  history: HistoryItem[];
}

export default function HistoryList({ history }: HistoryListProps) {
  if (history.length === 0) {
    return null;
  }

  return (
    <div className="bg-white rounded-lg shadow-lg p-6 mt-6">
      <div className="flex items-center justify-between mb-4">
        <h2 className="text-2xl font-bold text-gray-900">
          📋 Histórico de Classificações
        </h2>
        <span className="text-sm text-gray-500">
          {history.length} {history.length === 1 ? "classificação" : "classificações"}
        </span>
      </div>
      <div className="space-y-4">
        {history.map((item) => (
          <div
            key={item.id}
            className="border border-gray-200 rounded-lg p-4 hover:shadow-md transition-shadow bg-gray-50"
          >
            {/* Header com label e hora */}
            <div className="flex items-center justify-between mb-3 pb-3 border-b border-gray-200">
              <div className="flex items-center space-x-3">
                <span className="text-xl">
                  {item.result.label === "Produtivo" ? "📋" : "💬"}
                </span>
                <div>
                  <span
                    className={`font-bold text-lg ${
                      item.result.label === "Produtivo" ? "text-green-600" : "text-orange-600"
                    }`}
                  >
                    {item.result.label}
                  </span>
                  <div className="text-xs text-gray-500">
                    {Math.round(item.result.confidence * 100)}% de confiança
                  </div>
                </div>
              </div>
              <div className="text-right">
                <div className="text-sm font-semibold text-gray-700">
                  🕒 {new Date(item.timestamp).toLocaleTimeString("pt-BR", { 
                    hour: "2-digit", 
                    minute: "2-digit" 
                  })}
                </div>
                <div className="text-xs text-gray-500">
                  {new Date(item.timestamp).toLocaleDateString("pt-BR")}
                </div>
              </div>
            </div>

            {/* Input Preview */}
            <div className="mb-3">
              <div className="text-xs font-semibold text-gray-600 mb-1">📝 ENTRADA:</div>
              <div className="text-sm text-gray-800 bg-white rounded p-2 border border-gray-200 line-clamp-2">
                {item.input.length > 150 ? `${item.input.substring(0, 150)}...` : item.input}
              </div>
            </div>

            {/* Resposta Sugerida Preview */}
            <div className="mb-3">
              <div className="text-xs font-semibold text-gray-600 mb-1">💡 RESPOSTA SUGERIDA:</div>
              <div className="text-sm text-gray-800 bg-white rounded p-2 border border-gray-200 line-clamp-2">
                {item.result.suggested_reply.length > 150 
                  ? `${item.result.suggested_reply.substring(0, 150)}...` 
                  : item.result.suggested_reply}
              </div>
            </div>

            {/* Actions */}
            <div className="flex justify-end space-x-2 pt-2 border-t border-gray-200">
              <button
                onClick={() => {
                  navigator.clipboard.writeText(item.result.suggested_reply);
                  alert("Resposta copiada para a área de transferência!");
                }}
                className="px-3 py-1 bg-blue-600 text-white text-xs rounded hover:bg-blue-700 transition-colors"
              >
                📋 Copiar Resposta
              </button>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
