"use client";

import { useState, useEffect } from "react";
import UploadForm from "./UploadForm";
import ResultDisplay from "./ResultDisplay";
import HistoryList from "./HistoryList";
import { ClassificationResult } from "@/types/api";

interface HistoryItem {
  id: string;
  timestamp: Date;
  input: string;
  result: ClassificationResult;
}

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
    <div className="max-w-4xl mx-auto">
      {/* Header */}
      <div className="text-center mb-8">
        <h1 className="text-4xl font-bold text-gray-900 mb-2">
          📧 Classificador de Emails
        </h1>
        <p className="text-gray-600">
          Classificação automática usando Inteligência Artificial
        </p>
      </div>

      {/* Upload Form */}
      <div className="bg-white rounded-lg shadow-lg p-6 mb-6">
        <UploadForm 
          onClassify={handleClassification} 
          loading={loading}
        />
      </div>

      {/* Error Display */}
      {error && (
        <div className="bg-red-50 border border-red-200 rounded-lg p-4 mb-6">
          <div className="flex items-center">
            <span className="text-red-600 font-semibold">❌ Erro:</span>
            <span className="text-red-700 ml-2">{error}</span>
          </div>
        </div>
      )}

      {/* Result Display */}
      {result && <ResultDisplay result={result} />}

      {/* History List */}
      <HistoryList history={history} />

      {/* Info Section */}
      <div className="mt-8 bg-blue-50 rounded-lg p-6">
        <h3 className="text-lg font-semibold text-blue-900 mb-3">
          ℹ️ Como funciona?
        </h3>
        <ul className="space-y-2 text-blue-800">
          <li>• <strong>Produtivo:</strong> Emails que requerem ação ou resposta específica</li>
          <li>• <strong>Improdutivo:</strong> Emails que não necessitam ação imediata</li>
          <li>• A IA analisa o conteúdo e sugere uma resposta personalizada</li>
        </ul>
      </div>
    </div>
  );
}
