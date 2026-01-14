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

# Cria a aplicação FastAPI
app = FastAPI(
    title="Email Classifier API",
    description="API para classificação automática de emails usando Inteligência Artificial"
)

# Handler para erros de validação (422) - DEVE VIR DEPOIS DE CRIAR O APP
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Trata erros de validação e mostra mensagens mais claras"""
    errors = []
    for error in exc.errors():
        if error["type"] == "json_invalid":
            errors.append({
                "campo": "body",
                "erro": "JSON inválido. O texto pode conter caracteres especiais ou quebras de linha que precisam ser escapadas.",
                "detalhe": error.get("ctx", {}).get("error", "Erro ao decodificar JSON"),
                "solucao": "Use o Swagger UI ou certifique-se de escapar quebras de linha com \\n no JSON"
            })
        else:
            errors.append({
                "campo": " -> ".join(str(x) for x in error.get("loc", [])),
                "erro": error.get("msg", "Erro de validação"),
                "valor_recebido": error.get("input")
            })
    
    return JSONResponse(
        status_code=422,
        content={
            "erro": "Erro de validação",
            "detalhes": errors,
            "dica": "Se estiver usando curl, certifique-se de que o JSON está bem formatado. Use o Swagger UI (/docs) para testar mais facilmente."
        }
    )

# Configura CORS para permitir requisições do frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Em produção, especifique os domínios permitidos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Registra os routers (endpoints)
app.include_router(email_router)


@app.get("/health")
def verificar_saude():
    """Endpoint para verificar se a API está funcionando"""
    return {
        "status": "ok", 
        "message": "API rodando com sucesso"
    }


@app.get("/")
def root():
    """Endpoint raiz"""
    api_key_configurada = "✅ Configurada" if CHAVE_API_GEMINI else "❌ Não configurada"
    return {
        "message": "Bem-vindo à Email Classifier API",
        "docs": "/docs",
        "health": "/health",
        "api_key_status": api_key_configurada
    }
