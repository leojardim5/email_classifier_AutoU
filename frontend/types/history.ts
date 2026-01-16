/**
 * Interfaces relacionadas ao histórico de classificações
 * Arquivo independente - não depende de outros tipos
 */

import { BaseModel } from "./base";
import { ClassificationResult } from "./api";

/**
 * Interface para item do histórico de classificações
 */
export interface HistoryItem extends BaseModel {
  timestamp: Date;
  input: string;
  result: ClassificationResult;
}

/**
 * Interface para props do componente HistoryList
 */
export interface HistoryListProps {
  history: HistoryItem[];
  onClearHistory?: () => void;
  maxItems?: number;
}

/**
 * Interface para estatísticas do histórico
 */
export interface HistoryStats {
  total: number;
  productive: number;
  unproductive: number;
  averageConfidence: number;
}

/**
 * Interface para filtros do histórico
 */
export interface HistoryFilters {
  category?: "Produtivo" | "Improdutivo" | "all";
  dateFrom?: Date;
  dateTo?: Date;
  minConfidence?: number;
}
