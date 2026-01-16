"""
Serviço para classificar emails usando IA (Gemini)
"""
import json
import logging
from fastapi import HTTPException
from google import genai
from google.genai import errors as genai_errors
from app.config.configuracao import CHAVE_API_GEMINI, MODELO_GEMINI
from app.services.preprocessador_nlp import preprocessar_para_classificacao

logger = logging.getLogger(__name__)

# Variável global para o cliente Gemini
cliente_gemini = None


def obter_cliente_gemini():
    """
    Obtém ou cria o cliente Gemini
    """
    global cliente_gemini
    
    logger.debug("🔑 Verificando cliente Gemini...")
    
    if cliente_gemini is None:
        logger.info("🔧 Cliente Gemini não existe, criando novo...")
        if not CHAVE_API_GEMINI:
            logger.error("❌ API key do Gemini não configurada!")
            raise HTTPException(
                status_code=500,
                detail="API key do Gemini não configurada. Configure GEMINI_API_KEY no arquivo .env"
            )
        try:
            logger.debug(f"🔑 API Key presente (primeiros 10 chars): {CHAVE_API_GEMINI[:10]}...")
            logger.info("🔧 Inicializando cliente Gemini...")
            cliente_gemini = genai.Client(api_key=CHAVE_API_GEMINI)
            logger.info("✅ Cliente Gemini criado com sucesso!")
        except Exception as e:
            logger.error(f"❌ Erro ao inicializar cliente Gemini: {type(e).__name__} - {str(e)}")
            import traceback
            logger.error(f"Traceback: {traceback.format_exc()}")
            raise HTTPException(
                status_code=500,
                detail=f"Erro ao inicializar cliente Gemini: {str(e)}"
            )
    else:
        logger.debug("✅ Cliente Gemini já existe, reutilizando...")
    
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
    logger.info("🤖 Iniciando classificação com IA...")
    logger.debug(f"Texto original (tamanho: {len(texto_email)} chars)")
    
    # Obtém o cliente Gemini (cria se necessário)
    logger.debug("🔑 Obtendo cliente Gemini...")
    cliente = obter_cliente_gemini()
    logger.debug("✅ Cliente Gemini obtido")
    
    # Pré-processa o texto usando NLP (remove stop words, aplica stemming)
    logger.debug("📝 Aplicando pré-processamento NLP...")
    texto_preprocessado = preprocessar_para_classificacao(texto_email, aplicar_nlp=True)
    logger.debug(f"Texto pré-processado (tamanho: {len(texto_preprocessado)} chars)")
    
    # Monta o prompt para a IA (usa texto original para contexto, mas menciona pré-processamento)
    logger.debug("📋 Montando prompt para a IA...")
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
    
    logger.debug(f"Prompt montado (tamanho: {len(prompt)} chars)")
    logger.debug(f"Modelo a ser usado: {MODELO_GEMINI}")
    
    try:
        # Chama a API Gemini
        logger.info("🌐 Chamando API Gemini para classificação...")
        logger.debug(f"Enviando requisição para modelo: {MODELO_GEMINI}")
        resposta = cliente.models.generate_content(
            model=MODELO_GEMINI,
            contents=prompt
        )
        logger.debug("✅ Resposta recebida da API Gemini")
        texto_resposta = (resposta.text or "").strip()
        logger.debug(f"Texto da resposta (tamanho: {len(texto_resposta)} chars)")
        logger.debug(f"Resposta bruta (primeiros 500 chars): {texto_resposta[:500]}...")
        
        if not texto_resposta:
            logger.error("❌ API Gemini retornou resposta VAZIA!")
            raise HTTPException(
                status_code=500,
                detail="A API Gemini retornou uma resposta vazia. Verifique se a API key está correta."
            )
        
        # Extrai o JSON da resposta (pode vir com texto extra)
        logger.debug("🔍 Extraindo JSON da resposta...")
        if "{" in texto_resposta and "}" in texto_resposta:
            inicio = texto_resposta.find("{")
            fim = texto_resposta.rfind("}") + 1
            json_str = texto_resposta[inicio:fim]
            logger.debug(f"JSON extraído (posição {inicio} até {fim})")
        else:
            logger.warning("⚠️ Não encontrou chaves {} na resposta, usando texto completo")
            json_str = texto_resposta
        
        logger.debug(f"JSON a ser parseado: {json_str[:200]}...")
        
        # Converte JSON para dicionário Python
        try:
            dados = json.loads(json_str)
            logger.debug(f"✅ JSON parseado com sucesso: {dados}")
        except json.JSONDecodeError as je:
            logger.error(f"❌ Erro ao fazer parse do JSON!")
            logger.error(f"JSON que falhou: {json_str}")
            logger.error(f"Erro: {str(je)}")
            raise
        
        # Valida e normaliza o label
        logger.debug("✅ Validando e normalizando dados...")
        label = dados.get("label", "Improdutivo")
        logger.debug(f"Label recebido: {label}")
        if label not in ["Produtivo", "Improdutivo"]:
            logger.warning(f"⚠️ Label inválido '{label}', usando 'Improdutivo' como padrão")
            label = "Improdutivo"
        
        # Valida e normaliza a confiança (entre 0.0 e 1.0)
        confidence_raw = dados.get("confidence", 0.5)
        logger.debug(f"Confidence recebido: {confidence_raw} (tipo: {type(confidence_raw)})")
        confidence = float(confidence_raw)
        confidence = max(0.0, min(1.0, confidence))
        logger.debug(f"Confidence normalizado: {confidence}")
        
        resultado = {
            "label": label,
            "confidence": confidence,
            "reason": dados.get("reason", "")
        }
        logger.info(f"✅ Classificação concluída: {label} (confiança: {confidence})")
        return resultado
    except json.JSONDecodeError as e:
        logger.error("=" * 80)
        logger.error("❌ ERRO: JSON inválido na resposta da IA!")
        logger.error(f"Erro: {str(e)}")
        logger.error(f"Resposta recebida completa: {texto_resposta if 'texto_resposta' in locals() else 'N/A'}")
        logger.error("=" * 80)
        raise HTTPException(
            status_code=500, 
            detail=f"Erro ao processar resposta da IA (JSON inválido): {str(e)}. Resposta recebida: {texto_resposta[:200] if 'texto_resposta' in locals() else 'N/A'}"
        )
    except genai_errors.ClientError as e:
        # Trata especificamente erros 429 (quota excedida)
        error_str = str(e)
        if "429" in error_str or "RESOURCE_EXHAUSTED" in error_str or "quota" in error_str.lower():
            logger.error("=" * 80)
            logger.error("⚠️ ERRO 429: QUOTA DA API GEMINI EXCEDIDA!")
            logger.error("=" * 80)
            logger.error("📊 Limite do plano gratuito: 20 requisições/dia")
            logger.error("💡 Soluções:")
            logger.error("   1. Aguardar o reset da cota (próximo dia)")
            logger.error("   2. Usar outra API key do Gemini")
            logger.error("   3. Fazer upgrade do plano na Google Cloud")
            logger.error(f"⏰ Erro completo: {error_str[:300]}...")
            logger.error("=" * 80)
            raise HTTPException(
                status_code=429,
                detail={
                    "erro": "Quota da API Gemini excedida",
                    "mensagem": "Você atingiu o limite de 20 requisições/dia do plano gratuito.",
                    "solucoes": [
                        "Aguardar até o próximo dia para o reset da cota",
                        "Usar outra API key do Gemini",
                        "Fazer upgrade do plano na Google Cloud Console"
                    ],
                    "link_documentacao": "https://ai.google.dev/gemini-api/docs/rate-limits",
                    "erro_original": error_str[:500]
                }
            )
        else:
            # Outro erro do cliente (400, 401, 403, etc)
            logger.error("=" * 80)
            logger.error(f"❌ ERRO DO CLIENTE GEMINI (ClientError)")
            logger.error(f"Erro: {error_str}")
            logger.error("=" * 80)
            raise HTTPException(
                status_code=500,
                detail=f"Erro na API Gemini: {error_str[:300]}. Verifique sua API key e conectividade."
            )
    except HTTPException:
        # Re-lança exceções HTTP
        logger.debug("Re-lançando HTTPException...")
        raise
    except Exception as e:
        logger.error("=" * 80)
        logger.error(f"❌ ERRO INESPERADO em classificar_email_com_ia!")
        logger.error(f"Tipo: {type(e).__name__}")
        logger.error(f"Mensagem: {str(e)}")
        import traceback
        logger.error(f"Traceback completo:\n{traceback.format_exc()}")
        logger.error("=" * 80)
        raise HTTPException(
            status_code=500, 
            detail=f"Erro ao classificar email com Gemini: {str(e)}. Verifique se a API key está correta e se há conexão com a internet."
        )
