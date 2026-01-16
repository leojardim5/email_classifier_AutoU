"""
API para Classificação Automática de Emails
Estrutura MVC simples e organizada
"""
import logging
import traceback
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from app.controllers.email_controller import router as email_router
from app.config.configuracao import CHAVE_API_GEMINI

# Configura logging detalhado
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Email Classifier API",
    description="API para classificação automática de emails usando Inteligência Artificial",
)

# Handler global para capturar TODAS as exceções não tratadas
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Captura TODAS as exceções não tratadas e loga detalhadamente"""
    logger.error("=" * 80)
    logger.error("ERRO NÃO TRATADO CAPTURADO!")
    logger.error(f"URL: {request.url}")
    logger.error(f"Método: {request.method}")
    logger.error(f"Tipo de exceção: {type(exc).__name__}")
    logger.error(f"Mensagem: {str(exc)}")
    logger.error("Traceback completo:")
    logger.error(traceback.format_exc())
    logger.error("=" * 80)
    
    return JSONResponse(
        status_code=500,
        content={
            "erro": "Erro interno do servidor",
            "tipo": type(exc).__name__,
            "detalhe": str(exc),
            "traceback": traceback.format_exc() if logger.level == logging.DEBUG else None
        }
    )

# Handler para erros de validação (422)
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    logger.warning(f"Erro de validação na requisição: {request.url}")
    logger.debug(f"Detalhes do erro: {exc.errors()}")
    
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

@app.on_event("startup")
async def startup_event():
    """Loga informações na inicialização"""
    logger.info("=" * 80)
    logger.info("🚀 INICIANDO API DE CLASSIFICAÇÃO DE EMAILS")
    logger.info("=" * 80)
    logger.info(f"API Key Gemini configurada: {'✅ SIM' if CHAVE_API_GEMINI else '❌ NÃO'}")
    if CHAVE_API_GEMINI:
        logger.info(f"API Key (primeiros 10 chars): {CHAVE_API_GEMINI[:10]}...")
    logger.info("=" * 80)

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
