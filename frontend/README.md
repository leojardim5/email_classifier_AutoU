# Email Classifier - Frontend

Frontend em Next.js para classificação automática de emails usando IA.

## 🚀 Como Executar

### Pré-requisitos
- Node.js 18+ instalado
- Backend rodando em `http://127.0.0.1:8000`

### Instalação

```bash
# Instalar dependências
npm install

# Rodar em desenvolvimento
npm run dev
```

A aplicação estará disponível em: `http://localhost:3000`

## 📁 Estrutura

```
frontend/
├── app/
│   ├── layout.tsx          # Layout principal
│   ├── page.tsx            # Página inicial
│   └── globals.css         # Estilos globais
├── components/
│   ├── EmailClassifier.tsx # Componente principal
│   ├── UploadForm.tsx      # Formulário de upload
│   └── ResultDisplay.tsx   # Exibição de resultados
├── types/
│   └── api.ts              # Tipos TypeScript
└── package.json
```

## 🎨 Funcionalidades

- ✅ Upload de arquivos .txt ou .pdf
- ✅ Inserção direta de texto
- ✅ Classificação em tempo real
- ✅ Exibição de resultados com confiança
- ✅ Resposta sugerida personalizada
- ✅ Interface moderna e responsiva
- ✅ Copiar resposta para clipboard

## 🔌 Integração com Backend

O frontend se conecta automaticamente com o backend através do proxy configurado em `next.config.js`.

Endpoints utilizados:
- `POST /api/emails/classify-text` - Classificar texto
- `POST /api/emails/classify-file` - Classificar arquivo
