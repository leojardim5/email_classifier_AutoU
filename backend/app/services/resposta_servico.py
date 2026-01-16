"""
Serviço para gerar respostas automáticas usando IA
"""
import logging
from app.services.classificador_servico import obter_cliente_gemini
from app.config.configuracao import MODELO_GEMINI
from fastapi import HTTPException
from google.genai import errors as genai_errors

logger = logging.getLogger(__name__)


def gerar_resposta_sugerida(label: str, texto_email: str) -> str:
    """
    Gera uma resposta automática personalizada usando IA baseada no conteúdo do email
    
    Args:
        label: "Produtivo" ou "Improdutivo"
        texto_email: Texto original do email para personalizar a resposta
    
    Returns:
        Texto da resposta sugerida personalizada
    """
    logger.info(f"💬 Gerando resposta sugerida (label: {label})...")
    logger.debug(f"Texto do email (tamanho: {len(texto_email)} chars)")
    
    try:
        logger.debug("🔑 Obtendo cliente Gemini...")
        cliente = obter_cliente_gemini()
        logger.debug("✅ Cliente Gemini obtido")
        
        # Monta prompt para gerar resposta personalizada
        logger.debug(f"📋 Montando prompt para gerar resposta ({label})...")
        if label == "Produtivo":
            prompt = f"""
Você é um assistente de uma empresa do setor financeiro. Gere uma resposta profissional e personalizada para este email.

O email foi classificado como PRODUTIVO (requer ação/resposta específica).

Diretrizes:
- Seja profissional e cordial
- Reconheça a solicitação do cliente
- Se mencionar número de chamado/requisição, faça referência
- Se pedir status, ofereça ajuda para verificar
- Se for dúvida técnica, ofereça suporte
- Mantenha tom profissional mas acessível
- Use no máximo 4 parágrafos
- Assine com "Atenciosamente"

EMAIL RECEBIDO:
\"\"\"{texto_email[:1500]}\"\"\"

Gere APENAS a resposta, sem explicações adicionais:
""".strip()
        else:
            prompt = f"""
Você é um assistente de uma empresa do setor financeiro. Gere uma resposta profissional e personalizada para este email.

O email foi classificado como IMPRODUTIVO (não requer ação imediata - felicitações, agradecimentos, etc).

Diretrizes:
- Seja cordial e agradeça
- Se for felicitação, retribua de forma breve
- Se for agradecimento, responda de forma calorosa mas profissional
- Mantenha resposta breve (2-3 parágrafos)
- Assine com "Atenciosamente"

EMAIL RECEBIDO:
\"\"\"{texto_email[:1500]}\"\"\"

Gere APENAS a resposta, sem explicações adicionais:
""".strip()
        
        logger.debug(f"Prompt montado (tamanho: {len(prompt)} chars)")
        logger.debug(f"Modelo: {MODELO_GEMINI}")
        
        # Chama a IA para gerar resposta
        logger.info("🌐 Chamando API Gemini para gerar resposta...")
        resposta = cliente.models.generate_content(
            model=MODELO_GEMINI,
            contents=prompt
        )
        logger.debug("✅ Resposta recebida da API Gemini")
        
        texto_resposta = (resposta.text or "").strip()
        logger.debug(f"Texto da resposta (tamanho: {len(texto_resposta)} chars)")
        logger.debug(f"Resposta bruta (primeiros 300 chars): {texto_resposta[:300]}...")
        
        # Se a resposta vier vazia ou com texto extra, limpa
        if not texto_resposta:
            logger.warning("⚠️ Resposta vazia da IA, usando resposta padrão")
            return _resposta_padrao(label)
        
        # Remove possíveis prefixos como "Resposta:" ou "Aqui está:"
        logger.debug("🧹 Limpando resposta (removendo prefixos)...")
        linhas = texto_resposta.split('\n')
        linhas_limpas = [linha for linha in linhas if not linha.strip().lower().startswith(('resposta:', 'aqui está:', 'segue:'))]
        texto_resposta = '\n'.join(linhas_limpas).strip()
        
        if not texto_resposta:
            logger.warning("⚠️ Resposta ficou vazia após limpeza, usando resposta padrão")
            return _resposta_padrao(label)
        
        logger.info(f"✅ Resposta gerada com sucesso (tamanho final: {len(texto_resposta)} chars)")
        return texto_resposta
        
    except genai_errors.ClientError as e:
        # Se for erro 429, usa resposta padrão e loga aviso
        error_str = str(e)
        if "429" in error_str or "RESOURCE_EXHAUSTED" in error_str:
            logger.warning("⚠️ Quota excedida ao gerar resposta, usando resposta padrão")
        else:
            logger.warning(f"⚠️ Erro do cliente Gemini ao gerar resposta, usando resposta padrão: {error_str[:200]}")
        return _resposta_padrao(label)
    except Exception as e:
        # Se der erro, retorna resposta padrão
        logger.error("=" * 80)
        logger.error(f"❌ ERRO ao gerar resposta com IA!")
        logger.error(f"Tipo: {type(e).__name__}")
        logger.error(f"Mensagem: {str(e)}")
        import traceback
        logger.error(f"Traceback completo:\n{traceback.format_exc()}")
        logger.error("Usando resposta padrão como fallback...")
        logger.error("=" * 80)
        return _resposta_padrao(label)


def _resposta_padrao(label: str) -> str:
    """Resposta padrão caso a IA falhe"""
    if label == "Produtivo":
        return (
            "Olá! Obrigado pelo contato.\n\n"
            "Recebemos sua solicitação e vamos dar andamento. "
            "Se possível, envie o número do chamado/requisição e qualquer detalhe adicional "
            "para agilizar a análise.\n\n"
            "Atenciosamente."
        )
    else:
        return (
            "Olá! Obrigado pela mensagem.\n\n"
            "Registramos seu contato. Caso precise de suporte ou tenha uma solicitação específica, "
            "é só nos chamar por aqui.\n\n"
            "Atenciosamente."
        )
