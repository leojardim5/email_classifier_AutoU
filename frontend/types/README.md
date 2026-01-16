# 📁 Estrutura de Tipos

Estrutura organizada e independente de tipos TypeScript para o projeto.

## 📂 Arquivos

### `base.ts`
**Interfaces e tipos fundamentais do sistema**
- `BaseModel` - Interface base para modelos com ID
- `BaseApiResponse` - Interface base para respostas da API
- `BaseApiRequest` - Interface base para requisições
- `OperationStatus` - Status de operação
- `ApiError` - Erros padronizados
- `Result<T>` - Resultado genérico

**Dependências:** Nenhuma (arquivo base)

---

### `api.ts`
**Interfaces relacionadas à API de classificação**
- `EmailCategory` - Tipo para categorias de email
- `ClassificationRequest` - Requisição de classificação
- `ClassificationResult` - Resposta de classificação
- `GeminiTestResponse` - Resposta de teste do Gemini
- `ValidationError` - Erro de validação
- `ApiErrorResponse` - Resposta de erro da API

**Dependências:** `base.ts`

---

### `history.ts`
**Interfaces relacionadas ao histórico**
- `HistoryItem` - Item do histórico (estende `BaseModel`)
- `HistoryListProps` - Props do componente HistoryList
- `HistoryStats` - Estatísticas do histórico
- `HistoryFilters` - Filtros do histórico

**Dependências:** `base.ts`, `api.ts`

---

### `components.ts`
**Interfaces para props de componentes**
- `UploadFormProps` - Props do UploadForm
- `ResultDisplayProps` - Props do ResultDisplay
- `EmailClassifierProps` - Props do EmailClassifier
- `EmailClassifierState` - Estado interno do EmailClassifier

**Dependências:** `api.ts`, `history.ts`

---

### `index.ts`
**Exportações centralizadas**
- Exporta todos os tipos de forma centralizada
- Facilita imports: `import { Type } from "@/types"`

**Dependências:** Todos os outros arquivos

---

## 🎯 Como Usar

### Importação Individual
```typescript
import { ClassificationResult } from "@/types/api";
import { HistoryItem } from "@/types/history";
import { BaseModel } from "@/types/base";
```

### Importação Centralizada (Recomendado)
```typescript
import { 
  ClassificationResult, 
  HistoryItem, 
  BaseModel 
} from "@/types";
```

---

## ✅ Princípios

1. **Independência**: Cada arquivo pode ser usado independentemente
2. **BaseModel**: Interfaces principais estendem `BaseModel`
3. **Tipagem Forte**: Todos os tipos são explícitos
4. **Reutilização**: Tipos compartilhados em `base.ts`
5. **Organização**: Separação por responsabilidade

---

## 📝 Exemplo de Uso

```typescript
import { HistoryItem, ClassificationResult } from "@/types";

// Criar item do histórico
const item: HistoryItem = {
  id: "123",
  timestamp: new Date(),
  input: "Texto do email",
  result: {
    label: "Produtivo",
    confidence: 0.95,
    suggested_reply: "Resposta...",
    success: true
  }
};
```
