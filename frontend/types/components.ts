/**
 * Interfaces para props de componentes
 * Arquivo independente - não depende de outros tipos
 */

import { ClassificationResult } from "./api";
import { HistoryItem } from "./history";

/**
 * Props do componente UploadForm
 */
export interface UploadFormProps {
  onClassify: (text: string, file?: File) => void;
  loading: boolean;
  disabled?: boolean;
}

/**
 * Props do componente ResultDisplay
 */
export interface ResultDisplayProps {
  result: ClassificationResult;
  onCopyReply?: (reply: string) => void;
}

/**
 * Props do componente EmailClassifier
 */
export interface EmailClassifierProps {
  initialHistory?: HistoryItem[];
  maxHistoryItems?: number;
}

/**
 * Estado interno do EmailClassifier
 */
export interface EmailClassifierState {
  result: ClassificationResult | null;
  loading: boolean;
  error: string | null;
  history: HistoryItem[];
}
