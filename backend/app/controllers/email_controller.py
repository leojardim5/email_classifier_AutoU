"""
Controlador de Emails - Gerencia os endpoints da API
"""
import logging
from fastapi import APIRouter, UploadFile, File, HTTPException, Query
from pydantic import BaseModel
from app.models.schemas import RequisicaoEmailTexto, RespostaClassificacao
from app.services.extrator_servico import extrair_texto_de_arquivo
from app.services.classificador_servico import classificar_email_com_ia, obter_cliente_gemini
from app.services.resposta_servico import gerar_resposta_sugerida

logger = logging.getLogger(__name__)

# Cria o router para os endpoints de email
router = APIRouter(prefix="/api/emails", tags=["Emails"])


class TesteGeminiRequest(BaseModel):
    """Modelo para testar Gemini diretamente"""
    texto: str


@router.post("/teste-gemini")
def teste_gemini_direto(payload: TesteGeminiRequest):
    """
    Endpoint SIMPLES para testar o Gemini diretamente
    Só envia o texto e retorna a resposta bruta do Gemini
    """
    try:
        # Obtém o cliente Gemini
        cliente = obter_cliente_gemini()
        
        # Chama o Gemini com o texto direto
        resposta = cliente.models.generate_content(
            model="gemini-2.5-flash",
            contents=payload.texto
        )
        
        texto_resposta = (resposta.text or "").strip()
        
        return {
            "sucesso": True,
            "texto_enviado": payload.texto,
            "resposta_gemini": texto_resposta,
            "tamanho_resposta": len(texto_resposta)
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao testar Gemini: {str(e)}"
        )


@router.get("/classify-text-get")
def classificar_texto_get(texto: str = Query(..., description="Texto do email para classificar")):
    """
    Endpoint GET alternativo para classificar texto
    Útil para testar com URLs diretas ou quando JSON dá problema
    
    Exemplo: /api/emails/classify-text-get?texto=Olá, preciso de ajuda
    """
    try:
        # 1. Classifica o email usando IA
        resultado_classificacao = classificar_email_com_ia(texto)
        
        # 2. Gera resposta sugerida personalizada usando IA (baseada no conteúdo do email)
        resposta_sugerida = gerar_resposta_sugerida(resultado_classificacao["label"], texto)
        
        # 3. Retorna o resultado
        return RespostaClassificacao(
            label=resultado_classificacao["label"],
            confidence=resultado_classificacao["confidence"],
            suggested_reply=resposta_sugerida,
            all_scores=None
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Erro ao processar solicitação: {str(e)}"
        )


@router.post("/classify-text", response_model=RespostaClassificacao)
def classificar_texto(payload: RequisicaoEmailTexto):
    """
    Endpoint para classificar texto de email diretamente
    
    Recebe o texto do email e retorna:
    - Classificação (Produtivo/Improdutivo)
    - Confiança da classificação
    - Resposta sugerida
    
    Exemplo de requisição:
    {
        "texto": "Olá, gostaria de saber o status da minha requisição"
    }
    """
    logger.info("=" * 80)
    logger.info("📧 NOVA REQUISIÇÃO DE CLASSIFICAÇÃO DE TEXTO")
    logger.info("=" * 80)
    logger.info(f"Tamanho do texto recebido: {len(payload.texto)} caracteres")
    logger.debug(f"Texto recebido (primeiros 200 chars): {payload.texto[:200]}...")
    
    try:
        logger.info("🔍 PASSO 1: Iniciando classificação do email com IA...")
        # 1. Classifica o email usando IA
        resultado_classificacao = classificar_email_com_ia(payload.texto)
        logger.info(f"✅ Classificação concluída: {resultado_classificacao.get('label')} (confiança: {resultado_classificacao.get('confidence')})")
        logger.debug(f"Resultado completo da classificação: {resultado_classificacao}")
        
        logger.info("💬 PASSO 2: Gerando resposta sugerida com IA...")
        # 2. Gera resposta sugerida personalizada usando IA (baseada no conteúdo do email)
        resposta_sugerida = gerar_resposta_sugerida(resultado_classificacao["label"], payload.texto)
        logger.info(f"✅ Resposta gerada com sucesso (tamanho: {len(resposta_sugerida)} caracteres)")
        logger.debug(f"Resposta sugerida: {resposta_sugerida[:200]}...")
        
        logger.info("📤 PASSO 3: Montando resposta final...")
        # 3. Retorna o resultado
        resultado_final = RespostaClassificacao(
            label=resultado_classificacao["label"],
            confidence=resultado_classificacao["confidence"],
            suggested_reply=resposta_sugerida,
            all_scores=None
        )
        logger.info("✅ Requisição processada com SUCESSO!")
        logger.info("=" * 80)
        return resultado_final
    except HTTPException as he:
        # Re-lança exceções HTTP (já estão formatadas)
        logger.error(f"❌ HTTPException capturada: {he.status_code} - {he.detail}")
        logger.error("=" * 80)
        raise
    except Exception as e:
        # Captura outros erros inesperados
        logger.error("=" * 80)
        logger.error(f"❌ ERRO INESPERADO no endpoint classificar_texto!")
        logger.error(f"Tipo de exceção: {type(e).__name__}")
        logger.error(f"Mensagem: {str(e)}")
        import traceback
        logger.error(f"Traceback completo:\n{traceback.format_exc()}")
        logger.error("=" * 80)
        raise HTTPException(
            status_code=500, 
            detail=f"Erro ao processar solicitação: {str(e)}"
        )


@router.post("/classify-file", response_model=RespostaClassificacao)
async def classificar_arquivo(file: UploadFile = File(...)):
    """
    Endpoint para classificar email a partir de arquivo (.txt ou .pdf)
    
    Recebe um arquivo e retorna:
    - Classificação (Produtivo/Improdutivo)
    - Confiança da classificação
    - Resposta sugerida
    """
    try:
        # 1. Lê o conteúdo do arquivo
        conteudo = await file.read()
        
        if not conteudo:
            raise HTTPException(status_code=400, detail="Arquivo vazio ou não foi possível ler")
        
        # 2. Extrai o texto do arquivo
        texto_extraido = extrair_texto_de_arquivo(file.filename or "unknown", conteudo)
        
        if not texto_extraido or not texto_extraido.strip():
            raise HTTPException(
                status_code=400, 
                detail="Não foi possível extrair texto do arquivo. Verifique se o arquivo contém texto válido."
            )
        
        # 3. Classifica o email usando IA
        resultado_classificacao = classificar_email_com_ia(texto_extraido)
        
        # 4. Gera resposta sugerida personalizada usando IA (baseada no conteúdo do email)
        resposta_sugerida = gerar_resposta_sugerida(resultado_classificacao["label"], texto_extraido)
        
        # 5. Retorna o resultado
        return RespostaClassificacao(
            label=resultado_classificacao["label"],
            confidence=resultado_classificacao["confidence"],
            suggested_reply=resposta_sugerida,
            all_scores=None
        )
    except HTTPException:
        # Re-lança exceções HTTP
        raise
    except ValueError as e:
        # Erro de formato de arquivo
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        # Outros erros
        raise HTTPException(
            status_code=500, 
            detail=f"Erro ao processar arquivo: {str(e)}"
        )
