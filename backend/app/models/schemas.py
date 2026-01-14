"""
Modelos de dados (Schemas) - Define a estrutura dos dados que a API recebe e retorna
"""
from pydantic import BaseModel, Field
from typing import Optional


class RequisicaoEmailTexto(BaseModel):
    """Modelo para receber texto de email na requisição"""
    texto: str = Field(..., min_length=1, description="Texto do email para classificar")
    
    class Config:
        json_schema_extra = {
            "example": {
                "texto": "Olá, gostaria de saber o status da minha requisição #12345"
            }
        }


class RespostaClassificacao(BaseModel):
    """Modelo para retornar resultado da classificação"""
    label: str  # "Produtivo" ou "Improdutivo"
    confidence: float  # Confiança da classificação (0.0 a 1.0)
    suggested_reply: str  # Resposta sugerida
    all_scores: Optional[dict] = None  # Scores adicionais (opcional)
