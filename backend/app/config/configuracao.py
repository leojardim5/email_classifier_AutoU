"""
Configurações da aplicação
"""
import os
from dotenv import load_dotenv

load_dotenv(override=False)

# Configurações da API Gemini
CHAVE_API_GEMINI = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
if not CHAVE_API_GEMINI:
    raise RuntimeError("Defina GEMINI_API_KEY (ou GOOGLE_API_KEY) nas variáveis de ambiente.")

MODELO_GEMINI = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")

# Configurações de arquivo
EXTENSOES_PERMITIDAS = [".txt", ".pdf"]
TAMANHO_MAXIMO_ARQUIVO = 10 * 1024 * 1024  # 10MB
 