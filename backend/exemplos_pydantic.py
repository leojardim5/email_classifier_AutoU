"""
Exemplos Práticos de Pydantic - Para Testar e Entender

Execute este arquivo para ver os exemplos funcionando:
    python exemplos_pydantic.py
"""
from pydantic import BaseModel, Field, field_validator, model_validator, ValidationError
from typing import List, Optional, Dict
from enum import Enum
from datetime import datetime

print("=" * 80)
print("EXEMPLO 1: Modelo Básico com Field()")
print("=" * 80)

class UsuarioSimples(BaseModel):
    nome: str = Field(..., min_length=3, max_length=50)
    idade: int = Field(..., ge=0, le=120)
    email: str = Field(..., description="Email do usuário")

# [OK] Funciona
try:
    usuario1 = UsuarioSimples(nome="João", idade=25, email="joao@email.com")
    print(f"[OK] Usuario criado: {usuario1.nome}, {usuario1.idade} anos")
except ValidationError as e:
    print(f"[ERRO] Erro: {e}")

# Erro: nome muito curto
try:
    usuario2 = UsuarioSimples(nome="Jo", idade=25, email="joao@email.com")
except ValidationError as e:
    print(f"[ERRO ESPERADO] Nome muito curto: {e.errors()[0]['msg']}")

# Erro: idade invalida
try:
    usuario3 = UsuarioSimples(nome="Joao", idade=150, email="joao@email.com")
except ValidationError as e:
    print(f"[ERRO ESPERADO] Idade invalida: {e.errors()[0]['msg']}")

print("\n" + "=" * 80)
print("EXEMPLO 2: Campo Obrigatório vs Opcional")
print("=" * 80)

class UsuarioComOpcional(BaseModel):
    # Obrigatório
    nome: str = Field(..., min_length=1)
    
    # Opcional (pode ser None)
    sobrenome: Optional[str] = Field(None)
    
    # Opcional com valor padrão
    idade: int = Field(default=0)
    
    # Opcional, mas se vier deve ser maior que 0
    peso: Optional[float] = Field(None, gt=0)

# [OK] Funciona: só nome obrigatório
usuario4 = UsuarioComOpcional(nome="Maria")
print(f"[OK] Usuário criado: {usuario4.nome}, sobrenome={usuario4.sobrenome}, idade={usuario4.idade}")

# [OK] Funciona: todos os campos
usuario5 = UsuarioComOpcional(nome="Pedro", sobrenome="Silva", idade=30, peso=70.5)
print(f"[OK] Usuário criado: {usuario5.nome} {usuario5.sobrenome}, {usuario5.idade} anos, {usuario5.peso}kg")

print("\n" + "=" * 80)
print("EXEMPLO 3: Validação de Listas")
print("=" * 80)

class Produto(BaseModel):
    nome: str = Field(..., min_length=1)
    tags: List[str] = Field(default=[], max_length=5)
    preco: float = Field(..., gt=0)

# [OK] Funciona
produto1 = Produto(nome="Notebook", tags=["eletrônicos", "computadores"], preco=2500.00)
print(f"[OK] Produto: {produto1.nome}, tags: {produto1.tags}, preço: R$ {produto1.preco}")

# [ERRO] Erro: muitas tags
try:
    produto2 = Produto(
        nome="Mouse", 
        tags=["tag1", "tag2", "tag3", "tag4", "tag5", "tag6"],  # 6 tags, máximo é 5
        preco=50.00
    )
except ValidationError as e:
    print(f"[ERRO] Erro esperado (muitas tags): {e.errors()[0]['msg']}")

print("\n" + "=" * 80)
print("EXEMPLO 4: Validador Customizado de Campo")
print("=" * 80)

class UsuarioComValidacao(BaseModel):
    email: str = Field(..., description="Email do usuário")
    senha: str = Field(..., min_length=8)
    
    @field_validator('email')
    @classmethod
    def validar_email(cls, v: str) -> str:
        """Valida se o email contém @"""
        if '@' not in v:
            raise ValueError('Email deve conter @')
        return v.lower()  # Converte para minúsculas
    
    @field_validator('senha')
    @classmethod
    def validar_senha(cls, v: str) -> str:
        """Valida se a senha tem pelo menos uma letra maiúscula"""
        if not any(c.isupper() for c in v):
            raise ValueError('Senha deve conter pelo menos uma letra maiúscula')
        return v

# [OK] Funciona
usuario6 = UsuarioComValidacao(email="Joao@Email.com", senha="MinhaSenha123")
print(f"[OK] Usuário criado: email={usuario6.email} (convertido para minúsculas)")

# [ERRO] Erro: email sem @
try:
    usuario7 = UsuarioComValidacao(email="joaoemail.com", senha="MinhaSenha123")
except ValidationError as e:
    print(f"[ERRO] Erro esperado (email sem @): {e.errors()[0]['msg']}")

# [ERRO] Erro: senha sem maiúscula
try:
    usuario8 = UsuarioComValidacao(email="joao@email.com", senha="minhasenha123")
except ValidationError as e:
    print(f"[ERRO] Erro esperado (senha sem maiúscula): {e.errors()[0]['msg']}")

print("\n" + "=" * 80)
print("EXEMPLO 5: Validador de Modelo (Múltiplos Campos)")
print("=" * 80)

class UsuarioComSenha(BaseModel):
    senha: str = Field(..., min_length=8)
    confirmar_senha: str = Field(..., min_length=8)
    
    @model_validator(mode='after')
    def senhas_devem_ser_iguais(self):
        """Valida se as senhas são iguais"""
        if self.senha != self.confirmar_senha:
            raise ValueError('Senhas não coincidem')
        return self

# [OK] Funciona: senhas iguais
usuario9 = UsuarioComSenha(senha="MinhaSenha123", confirmar_senha="MinhaSenha123")
print(f"[OK] Senhas coincidem!")

# [ERRO] Erro: senhas diferentes
try:
    usuario10 = UsuarioComSenha(senha="MinhaSenha123", confirmar_senha="OutraSenha456")
except ValidationError as e:
    print(f"[ERRO] Erro esperado (senhas diferentes): {e.errors()[0]['msg']}")

print("\n" + "=" * 80)
print("EXEMPLO 6: Enum (Valores Fixos)")
print("=" * 80)

class StatusEmail(str, Enum):
    PRODUTIVO = "Produtivo"
    IMPRODUTIVO = "Improdutivo"

class EmailComStatus(BaseModel):
    texto: str = Field(..., min_length=1)
    status: StatusEmail = Field(..., description="Status do email")

# [OK] Funciona: status válido
email1 = EmailComStatus(texto="Olá, preciso de ajuda", status=StatusEmail.PRODUTIVO)
print(f"[OK] Email criado: status={email1.status}")

# [OK] Funciona: também aceita string (converte automaticamente)
email2 = EmailComStatus(texto="Olá", status="Improdutivo")
print(f"[OK] Email criado: status={email2.status}")

# [ERRO] Erro: status inválido
try:
    email3 = EmailComStatus(texto="Olá", status="Invalido")
except ValidationError as e:
    print(f"[ERRO] Erro esperado (status inválido): {e.errors()[0]['msg']}")

print("\n" + "=" * 80)
print("EXEMPLO 7: Serialização para JSON")
print("=" * 80)

class ProdutoJSON(BaseModel):
    nome: str
    preco: float
    tags: List[str] = Field(default=[])

produto = ProdutoJSON(nome="Notebook", preco=2500.00, tags=["eletrônicos"])

# Converte para dict (Python)
dict_produto = produto.model_dump()
print(f"[OK] Dict: {dict_produto}")

# Converte para JSON (string)
json_produto = produto.model_dump_json()
print(f"[OK] JSON: {json_produto}")

# Converte de dict para objeto
produto_criado = ProdutoJSON(**dict_produto)
print(f"[OK] Objeto criado de dict: {produto_criado.nome}")

print("\n" + "=" * 80)
print("EXEMPLO 8: Herança de Modelos")
print("=" * 80)

class RequisicaoBase(BaseModel):
    """Classe base com campos comuns"""
    texto: str = Field(..., min_length=1)
    remetente: str = Field(..., min_length=3)

class RequisicaoEmailSimples(RequisicaoBase):
    """Herda campos da base"""
    pass  # Só usa os campos da base

class RequisicaoEmailCompleta(RequisicaoBase):
    """Herda campos da base, adiciona campos extras"""
    prioridade: int = Field(default=3, ge=1, le=5)
    tags: List[str] = Field(default=[])

# [OK] Modelo simples (só campos da base)
email_simples = RequisicaoEmailSimples(texto="Olá", remetente="João")
print(f"[OK] Email simples: {email_simples.texto} de {email_simples.remetente}")

# [OK] Modelo completo (base + extras)
email_completo = RequisicaoEmailCompleta(
    texto="Olá", 
    remetente="Maria",
    prioridade=5,
    tags=["urgente", "importante"]
)
print(f"[OK] Email completo: {email_completo.texto}, prioridade={email_completo.prioridade}, tags={email_completo.tags}")

print("\n" + "=" * 80)
print("EXEMPLO 9: Validações de Números")
print("=" * 80)

class ValidacaoNumeros(BaseModel):
    idade: int = Field(..., ge=0, le=120, description="Idade entre 0 e 120")
    altura: float = Field(..., gt=0.0, le=3.0, description="Altura em metros")
    confianca: float = Field(..., ge=0.0, le=1.0, description="Confiança entre 0 e 1")
    quantidade: int = Field(default=0, multiple_of=5, description="Quantidade múltipla de 5")

# [OK] Funciona
numeros1 = ValidacaoNumeros(idade=25, altura=1.75, confianca=0.9, quantidade=10)
print(f"[OK] Números válidos: idade={numeros1.idade}, altura={numeros1.altura}m, confianca={numeros1.confianca}")

# [ERRO] Erro: idade inválida
try:
    numeros2 = ValidacaoNumeros(idade=150, altura=1.75, confianca=0.9)
except ValidationError as e:
    print(f"[ERRO] Erro esperado (idade inválida): {e.errors()[0]['msg']}")

# [ERRO] Erro: quantidade não é múltipla de 5
try:
    numeros3 = ValidacaoNumeros(idade=25, altura=1.75, confianca=0.9, quantidade=7)
except ValidationError as e:
    print(f"[ERRO] Erro esperado (quantidade não múltipla de 5): {e.errors()[0]['msg']}")

print("\n" + "=" * 80)
print("EXEMPLO 10: Modelo Real (Como no seu projeto)")
print("=" * 80)

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

# [OK] Criar requisição
requisicao = RequisicaoEmailTexto(texto="Olá, preciso de ajuda com meu pedido")
print(f"[OK] Requisição criada: {requisicao.texto}")

# [OK] Criar resposta
resposta = RespostaClassificacao(
    label="Produtivo",
    confidence=0.95,
    suggested_reply="Olá! Vamos verificar seu pedido.",
    all_scores=None
)
print(f"[OK] Resposta criada: {resposta.label} (confiança: {resposta.confidence})")

# Converter para JSON (como o FastAPI faz)
json_resposta = resposta.model_dump_json()
print(f"[OK] JSON da resposta: {json_resposta}")

print("\n" + "=" * 80)
print("[OK] TODOS OS EXEMPLOS EXECUTADOS COM SUCESSO!")
print("=" * 80)
