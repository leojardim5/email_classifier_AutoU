/**
 * Interfaces e tipos base do sistema
 * Arquivo independente com definições fundamentais
 */

/**
 * Interface base para modelos com identificador único
 */
export interface BaseModel {
  id: string;
  createdAt?: Date;
  updatedAt?: Date;
}

/**
 * Interface base para respostas da API
 */
export interface BaseApiResponse {
  success: boolean;
  message?: string;
  timestamp?: string;
}

/**
 * Interface base para requisições da API
 */
export interface BaseApiRequest {
  [key: string]: unknown;
}

/**
 * Tipo para status de operação
 */
export type OperationStatus = "idle" | "loading" | "success" | "error";

/**
 * Interface para erros padronizados
 */
export interface ApiError {
  code: string;
  message: string;
  details?: Record<string, unknown>;
}

/**
 * Tipo genérico para resultados com dados opcionais
 */
export interface Result<T> {
  data?: T;
  error?: ApiError;
}
