"use client";

import { useState } from "react";

interface UploadFormProps {
  onClassify: (text: string, file?: File) => void;
  loading: boolean;
}

export default function UploadForm({ onClassify, loading }: UploadFormProps) {
  const [text, setText] = useState("");
  const [file, setFile] = useState<File | null>(null);
  const [activeTab, setActiveTab] = useState<"text" | "file">("text");

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    
    if (activeTab === "text" && text.trim()) {
      onClassify(text);
    } else if (activeTab === "file" && file) {
      onClassify("", file);
    }
  };

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      const selectedFile = e.target.files[0];
      const extension = selectedFile.name.split('.').pop()?.toLowerCase();
      
      if (extension !== "txt" && extension !== "pdf") {
        alert("Por favor, selecione um arquivo .txt ou .pdf");
        return;
      }
      
      setFile(selectedFile);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      {/* Tabs */}
      <div className="flex border-b border-gray-200">
        <button
          type="button"
          onClick={() => setActiveTab("text")}
          className={`px-6 py-3 font-medium transition-colors ${
            activeTab === "text"
              ? "border-b-2 border-blue-600 text-blue-600"
              : "text-gray-500 hover:text-gray-700"
          }`}
        >
          📝 Inserir Texto
        </button>
        <button
          type="button"
          onClick={() => setActiveTab("file")}
          className={`px-6 py-3 font-medium transition-colors ${
            activeTab === "file"
              ? "border-b-2 border-blue-600 text-blue-600"
              : "text-gray-500 hover:text-gray-700"
          }`}
        >
          📎 Upload Arquivo
        </button>
      </div>

      {/* Text Input */}
      {activeTab === "text" && (
        <div>
          <label htmlFor="email-text" className="block text-sm font-medium text-gray-700 mb-2">
            Cole o texto do email aqui:
          </label>
          <textarea
            id="email-text"
            value={text}
            onChange={(e) => setText(e.target.value)}
            placeholder="Cole aqui o conteúdo do email que deseja classificar..."
            className="w-full h-48 px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent resize-none"
            required
            disabled={loading}
          />
        </div>
      )}

      {/* File Input */}
      {activeTab === "file" && (
        <div>
          <label htmlFor="email-file" className="block text-sm font-medium text-gray-700 mb-2">
            Selecione um arquivo (.txt ou .pdf):
          </label>
          <div className="flex items-center space-x-4">
            <input
              type="file"
              id="email-file"
              accept=".txt,.pdf"
              onChange={handleFileChange}
              className="block w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-lg file:border-0 file:text-sm file:font-semibold file:bg-blue-50 file:text-blue-700 hover:file:bg-blue-100"
              required={activeTab === "file"}
              disabled={loading}
            />
          </div>
          {file && (
            <div className="mt-2 text-sm text-gray-600">
              📄 Arquivo selecionado: <strong>{file.name}</strong> ({(file.size / 1024).toFixed(2)} KB)
            </div>
          )}
        </div>
      )}

      {/* Submit Button */}
      <button
        type="submit"
        disabled={loading || (activeTab === "text" && !text.trim()) || (activeTab === "file" && !file)}
        className="w-full bg-blue-600 text-white py-3 px-6 rounded-lg font-semibold hover:bg-blue-700 transition-colors disabled:bg-gray-400 disabled:cursor-not-allowed flex items-center justify-center"
      >
        {loading ? (
          <>
            <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
              <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
              <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
            </svg>
            Processando...
          </>
        ) : (
          "🚀 Classificar Email"
        )}
      </button>
    </form>
  );
}
