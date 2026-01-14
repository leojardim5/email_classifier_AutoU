"""
Serviço para classificar emails usando IA (Gemini)
"""
import json
from fastapi import HTTPException
from google import genai
from app.config.configuracao import CHAVE_API_GEMINI, MODELO_GEMINI
from app.services.preprocessador_nlp import preprocessar_para_classificacao

# Variável global para o cliente Gemini
cliente_gemini = None


def obter_cliente_gemini():
    """
    Obtém ou cria o cliente Gemini
    """
    global cliente_gemini
    
    if cliente_gemini is None:
        if not CHAVE_API_GEMINI:
            raise HTTPException(
                status_code=500,
                detail="API key do Gemini não configurada. Configure GEMINI_API_KEY no arquivo .env"
            )
        try:
            cliente_gemini = genai.Client(api_key=CHAVE_API_GEMINI)
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Erro ao inicializar cliente Gemini: {str(e)}"
            )
    
    return cliente_gemini


def classificar_email_com_ia(texto_email: str) -> dict:
    """
    Classifica email usando a API Gemini AI
    
    Aplica pré-processamento NLP (remoção de stop words, stemming) antes da classificação
    
    Args:
        texto_email: Texto do email a ser classificado
    
    Returns:
        Dicionário com label, confidence e reason
    
    Raises:
        HTTPException: Se houver erro na classificação
    """
    # Obtém o cliente Gemini (cria se necessário)
    cliente = obter_cliente_gemini()
    
    # Pré-processa o texto usando NLP (remove stop words, aplica stemming)
    texto_preprocessado = preprocessar_para_classificacao(texto_email, aplicar_nlp=True)
    
    # Monta o prompt para a IA (usa texto original para contexto, mas menciona pré-processamento)
    prompt = f"""
Você é um classificador de emails de uma empresa do setor financeiro.
Classifique o email em uma das categorias: "Produtivo" ou "Improdutivo".

Definições:
- Produtivo: requer ação/resposta específica (status de requisição, suporte, dúvidas do sistema, envio de arquivos para análise, etc.)
- Improdutivo: não requer ação imediata (felicitações, agradecimentos, mensagens sociais).

Responda APENAS em JSON válido, no formato:
{{"label":"Produtivo|Improdutivo","confidence":0.0-1.0,"reason":"explicação breve"}}

EMAIL (texto pré-processado com NLP):
\"\"\"{texto_preprocessado[:2000]}\"\"\"

EMAIL ORIGINAL (para contexto):
\"\"\"{texto_email[:2000]}\"\"\"
""".strip()
    
    try:
        # Chama a API Gemini
        resposta = cliente.models.generate_content(
            model=MODELO_GEMINI,
            contents=prompt
        )
        texto_resposta = (resposta.text or "").strip()
        
        if not texto_resposta:
            raise HTTPException(
                status_code=500,
                detail="A API Gemini retornou uma resposta vazia. Verifique se a API key está correta."
            )
        
        # Extrai o JSON da resposta (pode vir com texto extra)
        if "{" in texto_resposta and "}" in texto_resposta:
            inicio = texto_resposta.find("{")
            fim = texto_resposta.rfind("}") + 1
            json_str = texto_resposta[inicio:fim]
        else:
            json_str = texto_resposta
        
        # Converte JSON para dicionário Python
        dados = json.loads(json_str)
        
        # Valida e normaliza o label
        label = dados.get("label", "Improdutivo")
        if label not in ["Produtivo", "Improdutivo"]:
            label = "Improdutivo"
        
        # Valida e normaliza a confiança (entre 0.0 e 1.0)
        confidence = float(dados.get("confidence", 0.5))
        confidence = max(0.0, min(1.0, confidence))
        
        return {
            "label": label,
            "confidence": confidence,
            "reason": dados.get("reason", "")
        }
    except json.JSONDecodeError as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Erro ao processar resposta da IA (JSON inválido): {str(e)}. Resposta recebida: {texto_resposta[:200] if 'texto_resposta' in locals() else 'N/A'}"
        )
    except HTTPException:
        # Re-lança exceções HTTP
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Erro ao classificar email com Gemini: {str(e)}. Verifique se a API key está correta e se há conexão com a internet."
        )
