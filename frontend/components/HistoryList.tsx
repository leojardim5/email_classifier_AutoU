"use client";

import { HistoryItem, HistoryListProps } from "@/types";

export default function HistoryList({ history }: HistoryListProps) {
  if (history.length === 0) {
    return null;
  }

  return (
    <div className="bg-white rounded-xl shadow-autou border border-gray-100 p-8 mt-8">
      <div className="flex items-center justify-between mb-6">
        <div className="flex items-center space-x-3">
          <div className="w-12 h-12 bg-gradient-to-br from-blue-600 to-purple-600 rounded-xl flex items-center justify-center">
            <span className="text-white text-2xl">📋</span>
          </div>
          <div>
            <h2 className="text-2xl font-bold text-gray-900">
              Histórico de Classificações
            </h2>
            <p className="text-sm text-gray-500 mt-1">Últimas análises realizadas</p>
          </div>
        </div>
        <div className="px-4 py-2 bg-gradient-to-r from-blue-50 to-purple-50 rounded-full border border-blue-200">
          <span className="text-sm font-semibold text-gray-700">
            {history.length} {history.length === 1 ? "classificação" : "classificações"}
          </span>
        </div>
      </div>
      <div className="space-y-4">
        {history.map((item) => (
          <div
            key={item.id}
            className="border-2 border-gray-200 rounded-xl p-5 hover:shadow-lg hover:border-blue-300 transition-all bg-gradient-to-br from-gray-50 to-white"
          >
            {/* Header com label e hora */}
            <div className="flex items-center justify-between mb-4 pb-4 border-b-2 border-gray-200">
              <div className="flex items-center space-x-4">
                <div className={`w-12 h-12 rounded-xl flex items-center justify-center ${
                  item.result.label === "Produtivo" 
                    ? "bg-gradient-to-br from-green-500 to-emerald-600" 
                    : "bg-gradient-to-br from-orange-500 to-amber-600"
                } shadow-md`}>
                  <span className="text-2xl">
                    {item.result.label === "Produtivo" ? "📋" : "💬"}
                  </span>
                </div>
                <div>
                  <span
                    className={`font-bold text-xl ${
                      item.result.label === "Produtivo" ? "text-green-700" : "text-orange-700"
                    }`}
                  >
                    {item.result.label}
                  </span>
                  <div className="text-xs font-semibold text-gray-600 mt-1">
                    {Math.round(item.result.confidence * 100)}% de confiança
                  </div>
                </div>
              </div>
              <div className="text-right px-4 py-2 bg-gray-100 rounded-lg">
                <div className="text-sm font-bold text-gray-800">
                  {new Date(item.timestamp).toLocaleTimeString("pt-BR", { 
                    hour: "2-digit", 
                    minute: "2-digit" 
                  })}
                </div>
                <div className="text-xs text-gray-600">
                  {new Date(item.timestamp).toLocaleDateString("pt-BR")}
                </div>
              </div>
            </div>

            {/* Input Preview */}
            <div className="mb-4">
              <div className="text-xs font-bold text-gray-700 mb-2 uppercase tracking-wide flex items-center space-x-2">
                <span>📝</span>
                <span>ENTRADA</span>
              </div>
              <div className="text-sm text-gray-800 bg-white rounded-lg p-3 border-2 border-gray-200 line-clamp-2 shadow-sm">
                {item.input.length > 150 ? `${item.input.substring(0, 150)}...` : item.input}
              </div>
            </div>

            {/* Resposta Sugerida Preview */}
            <div className="mb-4">
              <div className="text-xs font-bold text-gray-700 mb-2 uppercase tracking-wide flex items-center space-x-2">
                <span>💡</span>
                <span>RESPOSTA SUGERIDA</span>
              </div>
              <div className="text-sm text-gray-800 bg-gradient-to-br from-blue-50 to-purple-50 rounded-lg p-3 border-2 border-blue-200 line-clamp-2 shadow-sm">
                {item.result.suggested_reply.length > 150 
                  ? `${item.result.suggested_reply.substring(0, 150)}...` 
                  : item.result.suggested_reply}
              </div>
            </div>

            {/* Actions */}
            <div className="flex justify-end space-x-2 pt-3 border-t-2 border-gray-200">
              <button
                onClick={() => {
                  navigator.clipboard.writeText(item.result.suggested_reply);
                  alert("Resposta copiada para a área de transferência!");
                }}
                className="px-4 py-2 bg-gradient-to-r from-blue-600 to-purple-600 text-white text-sm font-semibold rounded-lg hover:shadow-md transform hover:scale-105 transition-all flex items-center space-x-2"
              >
                <span>📋</span>
                <span>Copiar Resposta</span>
              </button>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
