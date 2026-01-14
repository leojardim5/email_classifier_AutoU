export interface ClassificationResult {
  label: "Produtivo" | "Improdutivo";
  confidence: number;
  suggested_reply: string;
  all_scores?: Record<string, number> | null;
}

export interface ClassificationRequest {
  texto: string;
}
