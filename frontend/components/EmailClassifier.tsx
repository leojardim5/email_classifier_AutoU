"use client";

import { useState, useEffect } from "react";
import UploadForm from "./UploadForm";
import ResultDisplay from "./ResultDisplay";
import HistoryList from "./HistoryList";
import { ClassificationResult, HistoryItem } from "@/types";

export default function EmailClassifier() {
  const [result, setResult] = useState<ClassificationResult | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [history, setHistory] = useState<HistoryItem[]>([]);

  // Carrega histórico do localStorage ao montar
  useEffect(() => {
    const savedHistory = localStorage.getItem("email-classifier-history");
    if (savedHistory) {
      try {
        const parsed = JSON.parse(savedHistory);
        // Converte timestamps para Date
        const historyWithDates = parsed.map((item: any) => ({
          ...item,
          timestamp: new Date(item.timestamp),
        }));
        setHistory(historyWithDates);
      } catch (e) {
        console.error("Erro ao carregar histórico:", e);
      }
    }
  }, []);

  // Salva histórico no localStorage
  const saveToHistory = (input: string, result: ClassificationResult) => {
    const newItem: HistoryItem = {
      id: Date.now().toString(),
      timestamp: new Date(),
      input: input,
      result: result,
    };

    const updatedHistory = [newItem, ...history].slice(0, 20); // Mantém apenas os últimos 20
    setHistory(updatedHistory);
    localStorage.setItem("email-classifier-history", JSON.stringify(updatedHistory));
  };

  const handleClassification = async (text: string, file?: File) => {
    setLoading(true);
    setError(null);
    setResult(null);

    try {
      let response;
      
      if (file) {
        // Upload de arquivo
        const formData = new FormData();
        formData.append("file", file);
        
        response = await fetch("/api/emails/classify-file", {
          method: "POST",
          body: formData,
        });
      } else {
        // Envio de texto
        response = await fetch("/api/emails/classify-text", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({ texto: text }),
        });
      }

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || "Erro ao processar email");
      }

      const data: ClassificationResult = await response.json();
      setResult(data);
      
      // Salva no histórico
      const inputText = file ? `Arquivo: ${file.name}` : text;
      saveToHistory(inputText, data);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Erro desconhecido");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-5xl mx-auto">
      {/* Hero Section */}
      <div className="text-center mb-12">
        <div className="inline-flex items-center justify-center w-20 h-20 bg-gradient-to-br from-blue-600 via-purple-600 to-indigo-600 rounded-2xl mb-6 shadow-autou transform hover:scale-105 transition-transform">
          <span className="text-white text-4xl">📧</span>
        </div>
        <h1 className="text-5xl font-bold mb-4 text-autou-gradient">
        Triagem Inteligente de E-mails (Case AutoU)
        </h1>
        <p className="text-xl text-gray-600 max-w-2xl mx-auto leading-relaxed">
          Transforme a complexidade do gerenciamento de emails em vantagem competitiva com nossa plataforma de IA
        </p>
        <div className="mt-6 flex items-center justify-center space-x-6 text-sm text-gray-500">
          <div className="flex items-center space-x-2">
            <div className="w-2 h-2 bg-green-500 rounded-full"></div>
            <span>IA Avançada</span>
          </div>
          <div className="flex items-center space-x-2">
            <div className="w-2 h-2 bg-blue-500 rounded-full"></div>
            <span>Respostas Personalizadas</span>
          </div>
          <div className="flex items-center space-x-2">
            <div className="w-2 h-2 bg-purple-500 rounded-full"></div>
            <span>Análise em Tempo Real</span>
          </div>
        </div>
      </div>

      {/* Upload Form */}
      <div className="bg-white rounded-xl shadow-autou border border-gray-100 p-8 mb-8">
        <UploadForm 
          onClassify={handleClassification} 
          loading={loading}
        />
      </div>

      {/* Error Display */}
      {error && (
        <div className="bg-red-50 border-l-4 border-red-500 rounded-lg p-5 mb-6 shadow-sm">
          <div className="flex items-start">
            <div className="flex-shrink-0">
              <svg className="h-6 w-6 text-red-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            </div>
            <div className="ml-3">
              <h3 className="text-sm font-semibold text-red-800 mb-1">Erro ao processar</h3>
              <p className="text-sm text-red-700">{error}</p>
            </div>
          </div>
        </div>
      )}

      {/* Result Display */}
      {result && <ResultDisplay result={result} />}

      {/* History List */}
      <HistoryList history={history} />

      {/* Info Section */}
      <div className="mt-12 bg-gradient-to-br from-blue-50 via-indigo-50 to-purple-50 rounded-xl p-8 border border-blue-100">
        <div className="flex items-start space-x-4">
          <div className="flex-shrink-0">
            <div className="w-12 h-12 bg-gradient-to-br from-blue-600 to-purple-600 rounded-lg flex items-center justify-center">
              <svg className="w-6 h-6 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            </div>
          </div>
          <div className="flex-1">
            <h3 className="text-xl font-bold text-gray-900 mb-4">
              Como funciona?
            </h3>
            <div className="grid md:grid-cols-2 gap-4">
              <div className="bg-white/60 rounded-lg p-4 border border-blue-100">
                <div className="flex items-center space-x-2 mb-2">
                  <span className="text-2xl">📋</span>
                  <span className="font-bold text-green-700">Produtivo</span>
                </div>
                <p className="text-sm text-gray-700">
                  Emails que requerem ação ou resposta específica (ex: solicitações de suporte, atualizações sobre casos, dúvidas sobre o sistema)
                </p>
              </div>
              <div className="bg-white/60 rounded-lg p-4 border border-blue-100">
                <div className="flex items-center space-x-2 mb-2">
                  <span className="text-2xl">💬</span>
                  <span className="font-bold text-orange-700">Improdutivo</span>
                </div>
                <p className="text-sm text-gray-700">
                  Emails que não necessitam ação imediata (ex: mensagens de felicitações, agradecimentos, comunicações informativas)
                </p>
              </div>
            </div>
            <div className="mt-4 pt-4 border-t border-blue-200">
              <p className="text-sm text-gray-700">
                <strong className="text-gray-900">Nossa IA</strong> analisa o conteúdo do email usando processamento de linguagem natural e sugere uma resposta personalizada baseada no contexto e na categoria identificada.
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
