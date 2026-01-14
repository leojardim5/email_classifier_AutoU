# Email Classifier API

API para classificação automática de emails usando Inteligência Artificial (Google Gemini).

## 📁 Estrutura do Projeto (MVC)

```
backend/
├── app/
│   ├── main.py                    # Aplicação principal
│   ├── config/                     # Configurações
│   │   └── configuracao.py        # Configurações da API
│   ├── models/                     # Modelos de dados
│   │   └── schemas.py             # Schemas Pydantic
│   ├── services/                   # Lógica de negócio
│   │   ├── extrator_servico.py    # Extração de texto
│   │   ├── classificador_servico.py  # Classificação com IA
│   │   └── resposta_servico.py   # Geração de respostas
│   └── controllers/                # Controladores (Endpoints)
│       └── email_controller.py    # Endpoints de email
├── .env                            # Variáveis de ambiente
└── requirements.txt                # Dependências
```

## 🎯 Arquitetura MVC

### **Model (Modelo)**
- `models/schemas.py`: Define a estrutura dos dados (requisições e respostas)

### **View (Visualização)**
- Endpoints REST que retornam JSON
- Documentação automática em `/docs`

### **Controller (Controlador)**
- `controllers/email_controller.py`: Gerencia os endpoints da API
  - `classificar_texto()`: Classifica texto direto
  - `classificar_arquivo()`: Classifica arquivo

### **Service (Serviço)**
- `services/extrator_servico.py`: Extrai texto de .txt ou .pdf
- `services/classificador_servico.py`: Usa Gemini AI para classificar
- `services/resposta_servico.py`: Gera resposta automática

### **Config (Configuração)**
- `config/configuracao.py`: Centraliza todas as configurações

## 📋 Requisitos

- Python 3.12+
- pip
- Arquivo `.env` com `GEMINI_API_KEY`

## 🚀 Instalação

1. **Crie um ambiente virtual:**
```bash
python -m venv venv
```

2. **Ative o ambiente virtual:**
```bash
# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

3. **Instale as dependências:**
```bash
pip install -r requirements.txt
```

4. **Configure a API key:**
Crie um arquivo `.env` na pasta `backend/`:
```env
GEMINI_API_KEY=sua_chave_api_aqui
GEMINI_MODEL=gemini-2.5-flash
```

## 🏃 Como Executar

```bash
uvicorn app.main:app --reload
```

A API estará disponível em: `http://127.0.0.1:8000`

## 📚 Documentação

Após iniciar, acesse:
- **Swagger UI:** http://127.0.0.1:8000/docs
- **ReDoc:** http://127.0.0.1:8000/redoc

## 🔌 Endpoints

### 1. Health Check
```
GET /health
```
Verifica se a API está funcionando.

### 2. Classificar Texto
```
POST /api/emails/classify-text
Content-Type: application/json

{
  "texto": "Olá, gostaria de saber o status da minha requisição."
}
```

### 3. Classificar Arquivo
```
POST /api/emails/classify-file
Content-Type: multipart/form-data

file: [arquivo .txt ou .pdf]
```

## 📝 Exemplo de Resposta

```json
{
  "label": "Produtivo",
  "confidence": 0.95,
  "suggested_reply": "Olá! Obrigado pelo contato.\n\nRecebemos sua solicitação...",
  "all_scores": null
}
```

## 🧪 Testando

### Usando Swagger UI
1. Acesse http://127.0.0.1:8000/docs
2. Clique em um endpoint
3. Clique em "Try it out"
4. Preencha os dados e clique em "Execute"

### Usando curl
```bash
curl -X POST "http://127.0.0.1:8000/api/emails/classify-text" \
  -H "Content-Type: application/json" \
  -d '{"texto": "Olá, preciso de ajuda com minha conta."}'
```

## 📦 Dependências

- **FastAPI**: Framework web moderno e rápido
- **Uvicorn**: Servidor ASGI
- **google-genai**: Cliente para API Gemini
- **pdfplumber**: Extração de texto de PDFs
- **python-dotenv**: Gerenciamento de variáveis de ambiente

## 🎓 Conceitos Aplicados

1. **MVC (Model-View-Controller)**: Separação clara de responsabilidades
2. **Service Layer**: Lógica de negócio isolada
3. **REST API**: Endpoints padronizados
4. **Validação de Dados**: Usando Pydantic
5. **Tratamento de Erros**: Try/except com mensagens claras
6. **Documentação Automática**: Swagger/OpenAPI

## 💡 Explicação da Estrutura

- **Cada arquivo tem uma responsabilidade específica**
- **Código em português para facilitar aprendizado**
- **Comentários explicativos em cada função**
- **Estrutura simples mas organizada (nível júnior/médio)**
