/**
 * Exportações centralizadas de todos os tipos
 * Facilita imports: import { Type } from "@/types"
 */

// Base
export type {
  BaseModel,
  BaseApiResponse,
  BaseApiRequest,
  OperationStatus,
  ApiError,
  Result,
} from "./base";

// API
export type {
  EmailCategory,
  ClassificationRequest,
  ClassificationFileRequest,
  ClassificationResult,
  GeminiTestResponse,
  ValidationError,
  ApiErrorResponse,
} from "./api";

// History
export type {
  HistoryItem,
  HistoryListProps,
  HistoryStats,
  HistoryFilters,
} from "./history";

// Components
export type {
  UploadFormProps,
  ResultDisplayProps,
  EmailClassifierProps,
  EmailClassifierState,
} from "./components";
