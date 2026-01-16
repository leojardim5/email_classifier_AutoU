/**
 * Interfaces relacionadas à API de classificação de emails
 * Arquivo independente - não depende de outros tipos
 */

import { BaseApiRequest, BaseApiResponse } from "./base";

/**
 * Categorias possíveis de classificação de email
 */
export type EmailCategory = "Produtivo" | "Improdutivo";

/**
 * Interface para requisição de classificação por texto
 */
export interface ClassificationRequest extends BaseApiRequest {
  texto: string;
}

/**
 * Interface para requisição de classificação por arquivo
 * (Usado internamente, não enviado diretamente)
 */
export interface ClassificationFileRequest {
  file: File;
}

/**
 * Interface para resposta de classificação da API
 */
export interface ClassificationResult extends BaseApiResponse {
  label: EmailCategory;
  confidence: number;
  suggested_reply: string;
  all_scores?: Record<string, number> | null;
}

/**
 * Interface para resposta de teste do Gemini
 */
export interface GeminiTestResponse extends BaseApiResponse {
  response: string;
  model: string;
  tokens_used?: number;
}

/**
 * Interface para erro de validação da API
 */
export interface ValidationError {
  campo: string;
  erro: string;
  detalhe?: string;
  valor_recebido?: unknown;
}

/**
 * Interface para resposta de erro da API
 */
export interface ApiErrorResponse {
  erro: string;
  detalhes?: ValidationError[];
  dica?: string;
}
