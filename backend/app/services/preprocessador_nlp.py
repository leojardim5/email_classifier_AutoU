"""
Serviço para pré-processamento de texto usando NLP
Remove stop words, aplica stemming/lemmatization
"""
import re
from typing import List


# Lista de stop words em português (palavras comuns que não agregam significado)
STOP_WORDS_PT = {
    'a', 'ao', 'aos', 'as', 'às', 'da', 'das', 'de', 'do', 'dos', 'e', 'em', 'na', 'nas', 
    'no', 'nos', 'o', 'os', 'para', 'por', 'que', 'um', 'uma', 'com', 'sem', 'sob', 'sobre',
    'entre', 'até', 'após', 'durante', 'mediante', 'segundo', 'conforme', 'consoante',
    'este', 'esta', 'estes', 'estas', 'esse', 'essa', 'esses', 'essas', 'aquele', 'aquela',
    'aqueles', 'aquelas', 'isto', 'isso', 'aquilo', 'meu', 'minha', 'meus', 'minhas',
    'teu', 'tua', 'teus', 'tuas', 'seu', 'sua', 'seus', 'suas', 'nosso', 'nossa', 'nossos',
    'nossas', 'deles', 'delas', 'ele', 'ela', 'eles', 'elas', 'eu', 'tu', 'nós', 'vós',
    'ser', 'estar', 'ter', 'haver', 'fazer', 'dizer', 'ir', 'vir', 'ver', 'dar', 'saber',
    'querer', 'poder', 'dever', 'ficar', 'passar', 'chegar', 'levar', 'deixar', 'encontrar',
    'começar', 'continuar', 'acabar', 'voltar', 'entrar', 'sair', 'subir', 'descer',
    'é', 'são', 'foi', 'foram', 'será', 'serão', 'está', 'estão', 'estava', 'estavam',
    'tem', 'têm', 'tinha', 'tinham', 'terá', 'terão', 'fez', 'fizeram', 'faz', 'fazem',
    'disse', 'disseram', 'diz', 'dizem', 'foi', 'foram', 'vai', 'vão', 'veio', 'vieram',
    'vê', 'veem', 'viu', 'viram', 'deu', 'deram', 'sabe', 'sabem', 'soube', 'souberam',
    'quer', 'querem', 'quis', 'quiseram', 'pode', 'podem', 'pôde', 'puderam', 'deve',
    'devem', 'ficou', 'ficaram', 'fica', 'ficam', 'passou', 'passaram', 'passa', 'passam'
}


def remover_stop_words(texto: str) -> str:
    """
    Remove stop words (palavras comuns) do texto
    
    Args:
        texto: Texto original
    
    Returns:
        Texto sem stop words
    """
    palavras = texto.lower().split()
    palavras_filtradas = [palavra for palavra in palavras if palavra not in STOP_WORDS_PT]
    return ' '.join(palavras_filtradas)


def normalizar_texto(texto: str) -> str:
    """
    Normaliza o texto: remove caracteres especiais e espaços extras
    
    Args:
        texto: Texto original
    
    Returns:
        Texto normalizado
    """
    # Remove caracteres especiais, mantendo apenas letras, números e espaços
    texto = re.sub(r'[^\w\s]', ' ', texto)
    # Remove espaços múltiplos
    texto = re.sub(r'\s+', ' ', texto)
    # Remove espaços no início e fim
    return texto.strip()


def aplicar_stemming_simples(palavra: str) -> str:
    """
    Aplica stemming simples (reduz palavra à raiz básica)
    Versão simplificada para português
    
    Args:
        palavra: Palavra a ser processada
    
    Returns:
        Palavra com stemming aplicado
    """
    palavra = palavra.lower()
    
    # Sufixos comuns em português
    sufixos = ['ção', 'ções', 'mente', 'mente', 'ando', 'endo', 'indo', 
               'ado', 'ido', 'ada', 'ida', 'ados', 'idos', 'adas', 'idas',
               'ar', 'er', 'ir', 'ou', 'am', 'em', 'im']
    
    # Remove sufixos comuns
    for sufixo in sufixos:
        if palavra.endswith(sufixo) and len(palavra) > len(sufixo) + 2:
            palavra = palavra[:-len(sufixo)]
            break
    
    return palavra


def preprocessar_texto_nlp(texto: str) -> str:
    """
    Aplica pré-processamento completo de NLP no texto
    
    Processos aplicados:
    1. Normalização (remove caracteres especiais)
    2. Remoção de stop words
    3. Stemming simples
    
    Args:
        texto: Texto original do email
    
    Returns:
        Texto pré-processado
    """
    if not texto or not texto.strip():
        return texto
    
    # 1. Normaliza o texto
    texto_normalizado = normalizar_texto(texto)
    
    # 2. Remove stop words
    texto_sem_stop_words = remover_stop_words(texto_normalizado)
    
    # 3. Aplica stemming em cada palavra
    palavras = texto_sem_stop_words.split()
    palavras_stemmed = [aplicar_stemming_simples(palavra) for palavra in palavras]
    
    # Retorna texto pré-processado
    texto_preprocessado = ' '.join(palavras_stemmed)
    
    return texto_preprocessado


def preprocessar_para_classificacao(texto: str, aplicar_nlp: bool = True) -> str:
    """
    Pré-processa texto para classificação
    
    Args:
        texto: Texto original
        aplicar_nlp: Se True, aplica NLP completo. Se False, apenas normaliza
    
    Returns:
        Texto pré-processado
    """
    if not texto or not texto.strip():
        return texto
    
    if aplicar_nlp:
        return preprocessar_texto_nlp(texto)
    else:
        return normalizar_texto(texto)
