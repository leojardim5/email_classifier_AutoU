"""
Serviço para extrair texto de arquivos
"""
import io
import pdfplumber


def extrair_texto_de_arquivo(nome_arquivo: str, conteudo: bytes) -> str:
    """
    Extrai texto de arquivos .txt ou .pdf
    
    Args:
        nome_arquivo: Nome do arquivo (para identificar extensão)
        conteudo: Conteúdo do arquivo em bytes
    
    Returns:
        Texto extraído do arquivo
    
    Raises:
        ValueError: Se o formato não for suportado
    """
    nome_lower = (nome_arquivo or "").lower()
    
    # Processa arquivo .txt
    if nome_lower.endswith(".txt"):
        try:
            return conteudo.decode("utf-8").strip()
        except UnicodeDecodeError:
            # Tenta com encoding alternativo se UTF-8 falhar
            return conteudo.decode("latin-1", errors="ignore").strip()
    
    # Processa arquivo .pdf
    elif nome_lower.endswith(".pdf"):
        texto_partes = []
        with pdfplumber.open(io.BytesIO(conteudo)) as pdf:
            for pagina in pdf.pages:
                texto_pagina = pagina.extract_text()
                if texto_pagina:
                    texto_partes.append(texto_pagina)
        return "\n".join(texto_partes).strip()
    
    else:
        raise ValueError("Formato não suportado. Use arquivos .txt ou .pdf")
