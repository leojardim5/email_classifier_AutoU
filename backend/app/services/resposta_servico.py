"""
Serviço para gerar respostas automáticas usando IA
"""
from app.services.classificador_servico import obter_cliente_gemini
from app.config.configuracao import MODELO_GEMINI
from fastapi import HTTPException


def gerar_resposta_sugerida(label: str, texto_email: str) -> str:
    """
    Gera uma resposta automática personalizada usando IA baseada no conteúdo do email
    
    Args:
        label: "Produtivo" ou "Improdutivo"
        texto_email: Texto original do email para personalizar a resposta
    
    Returns:
        Texto da resposta sugerida personalizada
    """
    try:
        cliente = obter_cliente_gemini()
        
        # Monta prompt para gerar resposta personalizada
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
        
        # Chama a IA para gerar resposta
        resposta = cliente.models.generate_content(
            model=MODELO_GEMINI,
            contents=prompt
        )
        
        texto_resposta = (resposta.text or "").strip()
        
        # Se a resposta vier vazia ou com texto extra, limpa
        if not texto_resposta:
            # Fallback para resposta padrão se IA falhar
            return _resposta_padrao(label)
        
        # Remove possíveis prefixos como "Resposta:" ou "Aqui está:"
        linhas = texto_resposta.split('\n')
        linhas_limpas = [linha for linha in linhas if not linha.strip().lower().startswith(('resposta:', 'aqui está:', 'segue:'))]
        texto_resposta = '\n'.join(linhas_limpas).strip()
        
        return texto_resposta if texto_resposta else _resposta_padrao(label)
        
    except Exception as e:
        # Se der erro, retorna resposta padrão
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
