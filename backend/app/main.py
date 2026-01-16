"""
API para Classificação Automática de Emails
Estrutura MVC simples e organizada
"""
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from app.controllers.email_controller import router as email_router
from app.config.configuracao import CHAVE_API_GEMINI

app = FastAPI(
    title="Email Classifier API",
    description="API para classificação automática de emails usando Inteligência Artificial",
)

# Handler para erros de validação (422)
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    errors = []
    for error in exc.errors():
        if error["type"] == "json_invalid":
            errors.append({
                "campo": "body",
                "erro": "JSON inválido. O texto pode conter caracteres especiais ou quebras de linha que precisam ser escapadas.",
                "detalhe": error.get("ctx", {}).get("error", "Erro ao decodificar JSON"),
                "solucao": "Escape quebras de linha com \\n no JSON ou teste pelo Swagger (/docs)."
            })
        else:
            errors.append({
                "campo": " -> ".join(str(x) for x in error.get("loc", [])),
                "erro": error.get("msg", "Erro de validação"),
                "valor_recebido": error.get("input"),
            })

    return JSONResponse(
        status_code=422,
        content={
            "erro": "Erro de validação",
            "detalhes": errors,
            "dica": "Use o Swagger UI (/docs) para testar mais facilmente.",
        },
    )

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Em produção, restrinja
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Rotas principais (API)
app.include_router(email_router)

def _health_payload():
    return {"status": "ok", "message": "API rodando com sucesso"}

# ✅ Health check do Render costuma bater aqui
@app.get("/healthz")
def healthz_get():
    return _health_payload()

# ✅ Alguns checks usam HEAD; evita 405 no log e evita restart por falha
@app.head("/healthz")
def healthz_head():
    return None

# Mantém /health também (pra você testar)
@app.get("/health")
def health_get():
    return _health_payload()

@app.head("/health")
def health_head():
    return None

@app.get("/")
def root():
    api_key_configurada = "✅ Configurada" if CHAVE_API_GEMINI else "❌ Não configurada"
    return {
        "message": "Bem-vindo à Email Classifier API",
        "docs": "/docs",
        "health": "/health",
        "healthz": "/healthz",
        "api_key_status": api_key_configurada,
    }
