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

# Modelos disponíveis do Gemini:
# - "gemini-2.5-flash" (padrão) - Mais rápido, menor custo
# - "gemini-1.5-flash" - Versão anterior do Flash
# - "gemini-1.5-pro" - Mais potente, maior custo
# - "gemini-2.0-flash-exp" - Experimental (pode ter cota diferente)
#
# ⚠️ IMPORTANTE: O limite de 20 requisições/dia é do PLANO GRATUITO (Free Tier),
# não do modelo específico. TODOS os modelos têm o mesmo limite no Free Tier.
# Para aumentar a cota, você precisa:
# 1. Ativar billing no Google Cloud (Tier 1: ~10.000 requisições/dia)
# 2. Ou aguardar o reset diário (20/dia no Free Tier)
# 3. Ou usar múltiplas API keys (cada uma com 20/dia)
#
# Para mudar o modelo, defina GEMINI_MODEL no arquivo .env:
# GEMINI_MODEL=gemini-1.5-flash
# GEMINI_MODEL=gemini-1.5-pro
# etc.
MODELO_GEMINI = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")

# Configurações de arquivo
EXTENSOES_PERMITIDAS = [".txt", ".pdf"]
TAMANHO_MAXIMO_ARQUIVO = 10 * 1024 * 1024  # 10MB
 