# 📧 Email Classifier - Sistema de Classificação Automática de Emails com IA

Solução web completa para classificar emails automaticamente usando Inteligência Artificial (Google Gemini), categorizando mensagens como **Produtivo** ou **Improdutivo** e gerando respostas automáticas personalizadas para cada email.

## 🎯 Objetivo

Automatizar a leitura e classificação de emails em grandes volumes, liberando tempo da equipe para atividades mais estratégicas. O sistema utiliza IA para identificar emails que requerem ação imediata (Produtivo) daqueles que são apenas felicitações ou agradecimentos (Improdutivo), e sugere respostas personalizadas automaticamente.

## ✨ Funcionalidades

### Classificação Automática
- **Produtivo**: Emails que requerem ação ou resposta específica (solicitações de suporte técnico, status de requisições, dúvidas sobre o sistema)
- **Improdutivo**: Emails que não necessitam ação imediata (mensagens de felicitações, agradecimentos)

### Entrada de Dados
- **Inserção direta de texto**: Cole o conteúdo do email diretamente na interface
- **Upload de arquivos**: Suporte para arquivos `.txt` ou `.pdf`

### Geração de Respostas
- Respostas personalizadas baseadas no conteúdo do email
- Contextualizadas para a categoria identificada
- Tom profissional adequado ao setor financeiro

### Interface Web
- Design moderno e intuitivo inspirado na AutoU
- Interface totalmente responsiva
- Histórico persistente de classificações (localStorage)
- Copiar resposta sugerida com um clique
- Estados de loading e tratamento de erros

## 🏗️ Arquitetura

O projeto segue uma arquitetura **MVC (Model-View-Controller)** com separação clara de responsabilidades:

```
Projeto_AutoI/
├── backend/          # API Python/FastAPI
│   ├── app/
│   │   ├── main.py                    # Aplicação FastAPI principal
│   │   ├── config/
│   │   │   └── configuracao.py        # Configurações (API keys, modelos)
│   │   ├── controllers/
│   │   │   └── email_controller.py    # Endpoints da API
│   │   ├── services/
│   │   │   ├── classificador_servico.py  # Classificação com Gemini AI
│   │   │   ├── resposta_servico.py       # Geração de respostas
│   │   │   ├── preprocessador_nlp.py     # Pré-processamento NLP
│   │   │   └── extrator_servico.py       # Extração de texto de PDFs
│   │   └── models/
│   │       └── schemas.py             # Modelos Pydantic (validação)
│   └── requirements.txt
└── frontend/         # Interface Next.js/React
    ├── app/
    │   ├── page.tsx                   # Página principal
    │   └── layout.tsx                 # Layout com fontes
    ├── components/
    │   ├── EmailClassifier.tsx        # Componente principal
    │   ├── UploadForm.tsx             # Formulário de upload
    │   ├── ResultDisplay.tsx          # Exibição de resultados
    │   ├── HistoryList.tsx            # Lista de histórico
    │   └── AutoULogo.tsx              # Logo da AutoU
    └── package.json
```

## 🛠️ Tecnologias

### Backend
- **Python 3.12+**: Linguagem principal
- **FastAPI**: Framework web moderno e rápido
- **Google Gemini AI** (`gemini-2.5-flash`): Classificação e geração de respostas
- **Pydantic**: Validação de dados e schemas
- **pdfplumber**: Extração de texto de arquivos PDF
- **Uvicorn**: Servidor ASGI
- **python-dotenv**: Gerenciamento de variáveis de ambiente

### Frontend
- **Next.js 14**: Framework React com Server-Side Rendering
- **React 18**: Biblioteca para interface de usuário
- **TypeScript**: Tipagem estática
- **Tailwind CSS**: Framework CSS utility-first
- **localStorage**: Persistência local do histórico

## 📋 Pré-requisitos

- **Python 3.12+** instalado
- **Node.js 18+** instalado
- **Conta Google AI Studio** com API key do Gemini
- **npm** ou **yarn** para gerenciar dependências do frontend

## 🚀 Instalação e Execução

### 1. Clone o repositório

```bash
git clone <url-do-repositorio>
cd Projeto_AutoI
```

### 2. Configurar Backend

```bash
# Entre na pasta do backend
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

# Configure a API key do Gemini
# Crie um arquivo .env na pasta backend/ com:
# GEMINI_API_KEY=sua_chave_api_aqui
# GEMINI_MODEL=gemini-2.5-flash
```

### 3. Executar Backend

```bash
# No diretório backend/
uvicorn app.main:app --reload
```

O backend estará disponível em: `http://127.0.0.1:8000`

**Documentação da API:** `http://127.0.0.1:8000/docs` (Swagger UI)

### 4. Configurar Frontend

```bash
# Entre na pasta do frontend (em outro terminal)
cd frontend

# Instale as dependências
npm install

# Configure a URL da API (opcional, se não estiver usando proxy)
# Crie um arquivo .env.local com:
# NEXT_PUBLIC_API_URL=http://127.0.0.1:8000
```

### 5. Executar Frontend

```bash
# No diretório frontend/
npm run dev
```

O frontend estará disponível em: `http://localhost:3000`

## 🔌 Endpoints da API

### Health Check
```
GET /health
```
Verifica se a API está funcionando.

### Classificar Texto
```
POST /api/emails/classify-text
Content-Type: application/json

{
  "texto": "Olá, preciso de ajuda com minha conta."
}
```

### Classificar Arquivo
```
POST /api/emails/classify-file
Content-Type: multipart/form-data

file: [arquivo .txt ou .pdf]
```

### Resposta de Exemplo
```json
{
  "label": "Produtivo",
  "confidence": 0.95,
  "suggested_reply": "Olá! Obrigado pelo contato...",
  "all_scores": null
}
```

## 🧪 Como Usar

### Via Interface Web

1. **Acesse a aplicação** em `http://localhost:3000`
2. **Escolha a forma de entrada:**
   - **Texto**: Cole o conteúdo do email diretamente
   - **Arquivo**: Faça upload de um arquivo `.txt` ou `.pdf`
3. **Clique em "Classificar Email"**
4. **Visualize o resultado:**
   - Categoria (Produtivo/Improdutivo)
   - Nível de confiança
   - Resposta sugerida personalizada
5. **Copie a resposta** com um clique
6. **Acesse o histórico** para ver classificações anteriores

### Via API (Swagger)

1. Acesse `http://127.0.0.1:8000/docs`
2. Selecione um endpoint
3. Clique em "Try it out"
4. Preencha os dados e clique em "Execute"

## 📝 Exemplos de Emails

### Email Produtivo
```
"Boa tarde! Preciso de ajuda urgente. Não consigo acessar minha conta 
há 2 dias e tenho uma demanda importante para hoje. Meu ID é 12345. 
Podem verificar o que está acontecendo?"
```

### Email Improdutivo
```
"Olá, pessoal! Só queria desejar um feliz natal e um próspero 
ano novo para toda a equipe! 🎄🎉"
```

## 🔧 Configuração Avançada

### Variáveis de Ambiente (Backend)

Crie um arquivo `.env` na pasta `backend/`:

```env
GEMINI_API_KEY=sua_chave_api_aqui
GEMINI_MODEL=gemini-2.5-flash
```

### Modelos Gemini Disponíveis

- `gemini-2.5-flash` (padrão) - Mais rápido, menor custo
- `gemini-1.5-flash` - Versão anterior do Flash
- `gemini-1.5-pro` - Mais potente, maior custo

Altere em `.env`: `GEMINI_MODEL=gemini-1.5-pro`

## 🌐 Deploy

### Backend (Render)

1. Conecte seu repositório no Render
2. Configure:
   - **Build Command**: `cd backend && pip install -r requirements.txt`
   - **Start Command**: `cd backend && uvicorn app.main:app --host 0.0.0.0 --port $PORT`
   - **Health Check Path**: `/health`
3. Configure variável de ambiente `GEMINI_API_KEY`

### Frontend (Vercel)

1. Conecte seu repositório no Vercel
2. Configure variável de ambiente `NEXT_PUBLIC_API_URL` com a URL do backend
3. Deploy automático a cada push

## 🎓 Conceitos e Práticas Aplicadas

- **MVC (Model-View-Controller)**: Separação clara de responsabilidades
- **Validação de Dados**: Pydantic para validação de entrada/saída
- **Processamento de Linguagem Natural (NLP)**: Pré-processamento de texto (remoção de stop words, normalização)
- **Inteligência Artificial**: Google Gemini AI para classificação e geração
- **API REST**: Endpoints RESTful bem estruturados
- **Tratamento de Erros**: Handlers globais e específicos
- **CORS**: Configuração para permitir requisições do frontend
- **Persistência Local**: localStorage para histórico de classificações
- **Responsive Design**: Interface adaptável a diferentes dispositivos

## 📚 Documentação Adicional

- **Backend**: Veja `backend/README.md` para detalhes da API
- **Frontend**: Veja `frontend/README.md` para detalhes da interface
- **API Docs**: Acesse `/docs` quando o backend estiver rodando (Swagger UI)

## 🤝 Como Contribuir

1. Faça fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📄 Licença

Este projeto foi desenvolvido como solução para um desafio técnico.

## 👤 Autor

Desenvolvido como solução para o desafio técnico da AutoU.

---

**Desenvolvido com ❤️ usando Python, FastAPI, Next.js e Google Gemini AI**
