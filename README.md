# 📧 Email Classifier - Sistema de Classificação Automática de Emails

Sistema completo de classificação automática de emails usando Inteligência Artificial, desenvolvido para uma empresa do setor financeiro. A solução classifica emails em "Produtivo" ou "Improdutivo" e gera respostas personalizadas usando a API Google Gemini AI.

## 📋 Índice

- [Visão Geral](#visão-geral)
- [Funcionalidades](#funcionalidades)
- [Tecnologias Utilizadas](#tecnologias-utilizadas)
- [Estrutura do Projeto](#estrutura-do-projeto)
- [Instalação e Configuração](#instalação-e-configuração)
- [Como Usar](#como-usar)
- [Arquitetura do Sistema](#arquitetura-do-sistema)
- [Como Funciona o localStorage](#como-funciona-o-localstorage)
- [API Endpoints](#api-endpoints)
- [Deploy](#deploy)
- [Requisitos do Desafio](#requisitos-do-desafio)

## 🎯 Visão Geral

Este projeto foi desenvolvido para resolver um problema real: empresas do setor financeiro recebem um alto volume de emails diariamente, muitos dos quais não requerem ação imediata. O sistema automatiza a classificação desses emails e sugere respostas personalizadas, liberando tempo da equipe.

### Categorias de Classificação

- **📋 Produtivo:** Emails que requerem ação ou resposta específica (solicitações de suporte, atualizações sobre casos, dúvidas sobre o sistema, etc.)
- **💬 Improdutivo:** Emails que não necessitam ação imediata (felicitações, agradecimentos, mensagens sociais)

## ✨ Funcionalidades

### Backend (Python/FastAPI)
- ✅ Classificação de emails usando Google Gemini AI
- ✅ Pré-processamento NLP (remoção de stop words, stemming)
- ✅ Geração de respostas personalizadas com IA
- ✅ Suporte a arquivos .txt e .pdf
- ✅ API REST completa com documentação (Swagger)
- ✅ Tratamento robusto de erros
- ✅ Estrutura MVC organizada e didática

### Frontend (Next.js/React)
- ✅ Interface moderna e responsiva com Tailwind CSS
- ✅ Upload de arquivos (.txt, .pdf)
- ✅ Inserção direta de texto
- ✅ Exibição de resultados com nível de confiança
- ✅ **Histórico de classificações** (localStorage)
- ✅ Design profissional e intuitivo
- ✅ TypeScript para type safety

## 🛠 Tecnologias Utilizadas

### Backend
- **Python 3.11+**
- **FastAPI** - Framework web moderno e rápido
- **Google Gemini AI** - API de IA para classificação e geração de respostas
- **pdfplumber** - Extração de texto de arquivos PDF
- **python-dotenv** - Gerenciamento de variáveis de ambiente
- **Pydantic** - Validação de dados
- **Uvicorn** - Servidor ASGI

### Frontend
- **Next.js 14** - Framework React com App Router
- **React 18** - Biblioteca para interfaces
- **TypeScript** - Tipagem estática
- **Tailwind CSS** - Framework CSS utilitário
- **localStorage API** - Armazenamento local do histórico

## 📁 Estrutura do Projeto

```
Projeto_AutoI/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py                    # Aplicação FastAPI principal
│   │   ├── config/
│   │   │   └── configuracao.py       # Configurações (API keys, etc)
│   │   ├── models/
│   │   │   └── schemas.py            # Schemas Pydantic (validação)
│   │   ├── services/
│   │   │   ├── extrator_servico.py   # Extração de texto (.txt, .pdf)
│   │   │   ├── preprocessador_nlp.py # NLP (stop words, stemming)
│   │   │   ├── classificador_servico.py # Classificação com Gemini AI
│   │   │   └── resposta_servico.py   # Geração de respostas com IA
│   │   └── controllers/
│   │       └── email_controller.py  # Endpoints REST API
│   ├── .env                          # Variáveis de ambiente (não versionado)
│   ├── requirements.txt              # Dependências Python
│   └── README.md                     # Documentação do backend
│
└── frontend/
    ├── app/
    │   ├── layout.tsx                # Layout principal
    │   ├── page.tsx                  # Página inicial
    │   └── globals.css               # Estilos globais
    ├── components/
    │   ├── EmailClassifier.tsx      # Componente principal
    │   ├── UploadForm.tsx           # Formulário de upload
    │   ├── ResultDisplay.tsx        # Exibição de resultados
    │   └── HistoryList.tsx          # Lista de histórico
    ├── types/
    │   └── api.ts                    # Tipos TypeScript
    ├── next.config.js               # Configuração Next.js
    ├── package.json                 # Dependências Node.js
    └── tsconfig.json                # Configuração TypeScript
```

## 🚀 Instalação e Configuração

### Pré-requisitos

- Python 3.11 ou superior
- Node.js 18+ e npm
- Conta Google Cloud com API Key do Gemini AI

### 1. Backend

```bash
# Navegue até a pasta do backend
cd backend

# Crie um ambiente virtual
python -m venv venv

# Ative o ambiente virtual
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Instale as dependências
pip install -r requirements.txt

# Crie o arquivo .env na pasta backend/
# Copie o exemplo abaixo e adicione sua API Key
echo GEMINI_API_KEY=sua_chave_aqui > .env

# Execute o servidor
uvicorn app.main:app --reload
```

O backend estará disponível em `http://127.0.0.1:8000`

**Documentação da API:** `http://127.0.0.1:8000/docs`

### 2. Frontend

```bash
# Navegue até a pasta do frontend
cd frontend

# Instale as dependências
npm install

# Execute o servidor de desenvolvimento
npm run dev
```

O frontend estará disponível em `http://localhost:3000`

### 3. Configuração da API Key do Gemini

1. Acesse [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Crie uma API Key
3. Adicione no arquivo `backend/.env`:
   ```
   GEMINI_API_KEY=sua_chave_aqui
   ```

## 📖 Como Usar

### Interface Web

1. **Acesse a aplicação** em `http://localhost:3000`
2. **Escolha a forma de entrada:**
   - **Texto:** Digite ou cole o texto do email diretamente
   - **Arquivo:** Faça upload de um arquivo .txt ou .pdf
3. **Clique em "Classificar Email"**
4. **Visualize o resultado:**
   - Categoria (Produtivo/Improdutivo)
   - Nível de confiança
   - Resposta sugerida personalizada
5. **Acesse o histórico** abaixo para ver classificações anteriores

### API REST (Swagger)

1. Acesse `http://127.0.0.1:8000/docs`
2. Teste os endpoints diretamente pela interface Swagger
3. Principais endpoints:
   - `POST /api/emails/classify-text` - Classificar texto
   - `POST /api/emails/classify-file` - Classificar arquivo
   - `POST /api/emails/teste-gemini` - Testar Gemini diretamente

## 🏗 Arquitetura do Sistema

### Fluxo de Processamento

```
1. Usuário envia texto/arquivo
   ↓
2. Frontend → Backend (API REST)
   ↓
3. Backend extrai texto (se arquivo)
   ↓
4. Pré-processamento NLP (stop words, stemming)
   ↓
5. Classificação com Gemini AI → "Produtivo" ou "Improdutivo"
   ↓
6. Geração de resposta personalizada com Gemini AI
   ↓
7. Retorno para Frontend
   ↓
8. Exibição de resultado + salvamento no histórico
```

### Estrutura MVC

O backend segue o padrão **MVC (Model-View-Controller)**:

- **Models (schemas.py):** Define a estrutura dos dados (entrada/saída)
- **Views (controllers):** Endpoints da API que recebem requisições
- **Controllers (services):** Lógica de negócio (classificação, NLP, etc.)

## 💾 Como Funciona o localStorage

### O que é localStorage?

O `localStorage` é uma API do navegador que permite armazenar dados no computador do usuário de forma persistente. Os dados permanecem salvos mesmo após fechar o navegador.

### Como é usado no projeto?

O histórico de classificações é salvo no `localStorage` para manter um registro das requisições anteriores.

#### 1. Salvando no Histórico

```typescript
// Após receber a resposta da API
const saveToHistory = (input: string, result: ClassificationResult) => {
  const newItem = {
    id: Date.now().toString(),           // ID único (timestamp)
    timestamp: new Date(),                // Data/hora da classificação
    input: input,                         // Texto ou nome do arquivo
    result: result                        // Resultado completo (label, confidence, suggested_reply)
  };

  // Adiciona no início do array e mantém apenas os últimos 20
  const updatedHistory = [newItem, ...history].slice(0, 20);
  
  // Salva no localStorage (como JSON string)
  localStorage.setItem("email-classifier-history", JSON.stringify(updatedHistory));
};
```

#### 2. Carregando do Histórico

```typescript
// Ao carregar a página
useEffect(() => {
  const savedHistory = localStorage.getItem("email-classifier-history");
  if (savedHistory) {
    try {
      // Converte de JSON string para objeto JavaScript
      const parsed = JSON.parse(savedHistory);
      
      // Converte timestamps de string para Date
      const historyWithDates = parsed.map((item: any) => ({
        ...item,
        timestamp: new Date(item.timestamp),
      }));
      
      setHistory(historyWithDates);
    } catch (e) {
      console.error("Erro ao carregar histórico:", e);
    }
  }
}, []);
```

#### 3. Características Importantes

- ✅ **Persistência:** Dados permanecem após fechar o navegador
- ✅ **Escopo:** Dados são específicos do domínio (localhost vs produção)
- ✅ **Limite:** Aproximadamente 5-10MB por domínio
- ✅ **Formato:** Apenas strings (JSON.stringify/parse necessário)
- ✅ **Acesso:** Apenas via JavaScript no mesmo domínio

#### 4. Limitações e Considerações

- ⚠️ **Não é seguro para dados sensíveis** (armazena no navegador do usuário)
- ⚠️ **Limitado ao navegador/dispositivo** (não sincroniza entre dispositivos)
- ⚠️ **Pode ser limpo pelo usuário** (limpar dados do navegador)
- ⚠️ **Não funciona em modo privado/incógnito** em alguns navegadores

#### 5. Estrutura dos Dados Salvos

```json
[
  {
    "id": "1704123456789",
    "timestamp": "2024-01-01T10:30:00.000Z",
    "input": "Olá, gostaria de saber o status da minha requisição #12345.",
    "result": {
      "label": "Produtivo",
      "confidence": 0.95,
      "suggested_reply": "Olá! Obrigado pelo contato..."
    }
  },
  ...
]
```

## 🔌 API Endpoints

### Classificar Texto
```http
POST /api/emails/classify-text
Content-Type: application/json

{
  "texto": "Olá, gostaria de saber o status da minha requisição"
}
```

**Resposta:**
```json
{
  "label": "Produtivo",
  "confidence": 0.95,
  "suggested_reply": "Olá! Obrigado pelo contato...",
  "all_scores": null
}
```

### Classificar Arquivo
```http
POST /api/emails/classify-file
Content-Type: multipart/form-data

file: [arquivo.txt ou arquivo.pdf]
```

### Teste Gemini
```http
POST /api/emails/teste-gemini
Content-Type: application/json

{
  "texto": "Texto para testar"
}
```

### Health Check
```http
GET /health
```

## 🌐 Deploy

### Backend (Render/Railway/Heroku)

1. Crie uma conta na plataforma escolhida
2. Conecte seu repositório GitHub
3. Configure as variáveis de ambiente:
   - `GEMINI_API_KEY`
4. Configure o comando de start:
   - `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

### Frontend (Vercel - Recomendado)

1. Conecte o repositório no [Vercel](https://vercel.com)
2. Configure as variáveis de ambiente:
   - Não é necessário (usa proxy via next.config.js)
3. Ajuste o `next.config.js` para apontar para o backend em produção:
   ```javascript
   async rewrites() {
     return [
       {
         source: '/api/:path*',
         destination: 'https://seu-backend.onrender.com/api/:path*',
       },
     ];
   },
   ```

## 📋 Checklist de Requisitos do Desafio

Verifique o arquivo [CHECKLIST_REQUISITOS.md](./CHECKLIST_REQUISITOS.md) para uma análise completa de todos os requisitos.

## 📝 Licença

Este projeto foi desenvolvido para fins educacionais e de avaliação técnica.

## 👤 Autor

Desenvolvido como parte do processo seletivo AutoU.

## 🙏 Agradecimentos

- Google Gemini AI pela API de inteligência artificial
- Comunidade open source pelas bibliotecas utilizadas
