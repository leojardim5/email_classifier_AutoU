"use client";

import { useState } from "react";
import { UploadFormProps } from "@/types";

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
    <form onSubmit={handleSubmit} className="space-y-6">
      {/* Tabs */}
      <div className="flex space-x-2 bg-gray-50 p-1 rounded-lg border border-gray-200">
        <button
          type="button"
          onClick={() => setActiveTab("text")}
          className={`flex-1 px-6 py-3 font-semibold text-sm rounded-md transition-all ${
            activeTab === "text"
              ? "bg-gradient-to-r from-blue-600 to-purple-600 text-white shadow-md"
              : "text-gray-600 hover:text-gray-900 hover:bg-white"
          }`}
        >
          <span className="mr-2">📝</span>
          Inserir Texto
        </button>
        <button
          type="button"
          onClick={() => setActiveTab("file")}
          className={`flex-1 px-6 py-3 font-semibold text-sm rounded-md transition-all ${
            activeTab === "file"
              ? "bg-gradient-to-r from-blue-600 to-purple-600 text-white shadow-md"
              : "text-gray-600 hover:text-gray-900 hover:bg-white"
          }`}
        >
          <span className="mr-2">📎</span>
          Upload Arquivo
        </button>
      </div>

      {/* Text Input */}
      {activeTab === "text" && (
        <div>
          <label htmlFor="email-text" className="block text-sm font-semibold text-gray-700 mb-3">
            Cole o texto do email aqui:
          </label>
          <textarea
            id="email-text"
            value={text}
            onChange={(e) => setText(e.target.value)}
            placeholder="Cole aqui o conteúdo do email que deseja classificar..."
            className="w-full h-56 px-4 py-4 border-2 border-gray-200 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-blue-500 resize-none transition-all shadow-sm hover:shadow-md"
            required
            disabled={loading}
          />
        </div>
      )}

      {/* File Input */}
      {activeTab === "file" && (
        <div>
          <label htmlFor="email-file" className="block text-sm font-semibold text-gray-700 mb-3">
            Selecione um arquivo (.txt ou .pdf):
          </label>
          <div className="relative">
            <input
              type="file"
              id="email-file"
              accept=".txt,.pdf"
              onChange={handleFileChange}
              className="block w-full text-sm text-gray-500 
                file:mr-4 file:py-3 file:px-6 
                file:rounded-xl file:border-0 
                file:text-sm file:font-semibold 
                file:bg-gradient-to-r file:from-blue-600 file:to-purple-600 
                file:text-white 
                hover:file:opacity-90 
                file:cursor-pointer
                file:shadow-md
                file:transition-all
                cursor-pointer"
              required={activeTab === "file"}
              disabled={loading}
            />
          </div>
          {file && (
            <div className="mt-4 p-4 bg-gradient-to-r from-blue-50 to-purple-50 rounded-xl border border-blue-200">
              <div className="flex items-center space-x-3">
                <div className="w-10 h-10 bg-gradient-to-br from-blue-600 to-purple-600 rounded-lg flex items-center justify-center">
                  <span className="text-white text-lg">📄</span>
                </div>
                <div className="flex-1">
                  <div className="font-semibold text-gray-900">{file.name}</div>
                  <div className="text-sm text-gray-600">{(file.size / 1024).toFixed(2)} KB</div>
                </div>
              </div>
            </div>
          )}
        </div>
      )}

      {/* Submit Button */}
      <button
        type="submit"
        disabled={loading || (activeTab === "text" && !text.trim()) || (activeTab === "file" && !file)}
        className="w-full bg-gradient-to-r from-blue-600 via-purple-600 to-indigo-600 text-white py-4 px-6 rounded-xl font-bold text-lg shadow-lg hover:shadow-xl transform hover:scale-[1.02] transition-all disabled:opacity-50 disabled:cursor-not-allowed disabled:transform-none flex items-center justify-center space-x-2"
      >
        {loading ? (
          <>
            <svg className="animate-spin h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
              <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
              <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
            </svg>
            <span>Processando com IA...</span>
          </>
        ) : (
          <>
            <span>🚀</span>
            <span>Classificar Email</span>
          </>
        )}
      </button>
    </form>
  );
}
