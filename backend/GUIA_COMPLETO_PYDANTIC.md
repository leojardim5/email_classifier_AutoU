# 🎓 Guia Completo: Pydantic do Zero Absoluto (Para quem vem de Java)

## 📚 Índice
1. [Herança em Python vs Java](#1-herança-em-python-vs-java)
2. [O que é BaseModel?](#2-o-que-é-basemodel)
3. [Field() - Validações Básicas](#3-field---validações-básicas)
4. [Field() - Validações Avançadas](#4-field---validações-avançadas)
5. [Validadores Customizados](#5-validadores-customizados)
6. [Injeção de Dependência (FastAPI vs Spring Boot)](#6-injeção-de-dependência-fastapi-vs-spring-boot)
7. [Exemplos Práticos Completos](#7-exemplos-práticos-completos)

---

## 1. Herança em Python vs Java

### Java (O que você conhece)
```java
public class RequisicaoEmail extends BaseModel {
    private String texto;
    
    public RequisicaoEmail(String texto) {
        this.texto = texto;
    }
    
    // Getters e Setters...
}
```

### Python (Como funciona aqui)
```python
class RequisicaoEmail(BaseModel):  # Herda de BaseModel
    texto: str  # Atributo de classe (não precisa de getters/setters)
```

**Diferenças principais:**
- **Java**: Classes são "blueprints", você precisa criar objetos com `new`
- **Python**: Classes também são "blueprints", mas a sintaxe é mais simples
- **Java**: Herança usa `extends`
- **Python**: Herança usa parênteses `(BaseModel)`
- **Java**: Atributos privados com getters/setters
- **Python**: Atributos públicos (mas Pydantic valida automaticamente)

---

## 2. O que é BaseModel?

`BaseModel` é uma classe do Pydantic que adiciona **validação automática** aos seus modelos.

### Sem BaseModel (Python puro)
```python
class RequisicaoEmail:
    def __init__(self, texto: str):
        self.texto = texto

# Você pode criar com qualquer coisa
obj = RequisicaoEmail(123)  # ✅ Funciona, mas texto não é string!
obj = RequisicaoEmail(None)  # ✅ Funciona, mas texto é None!
```

### Com BaseModel (Pydantic)
```python
from pydantic import BaseModel

class RequisicaoEmail(BaseModel):
    texto: str

# Agora tem validação automática
obj = RequisicaoEmail(texto="Olá")  # ✅ Funciona
obj = RequisicaoEmail(texto=123)  # ❌ Erro! Tenta converter para string
obj = RequisicaoEmail()  # ❌ Erro! Campo obrigatório faltando
```

**O que BaseModel faz automaticamente:**
1. ✅ Valida tipos (string, int, float, etc.)
2. ✅ Converte tipos quando possível (int → str)
3. ✅ Rejeita valores inválidos
4. ✅ Gera JSON Schema (para documentação)
5. ✅ Serializa para JSON automaticamente

---

## 3. Field() - Validações Básicas

`Field()` é uma função que adiciona **regras extras** de validação aos campos.

### Sintaxe Básica
```python
from pydantic import BaseModel, Field

class ExemploBasico(BaseModel):
    # Campo obrigatório (sem valor padrão)
    nome: str = Field(...)
    
    # Campo opcional (com valor padrão)
    idade: int = Field(default=0)
    
    # Campo obrigatório com descrição
    email: str = Field(..., description="Email do usuário")
```

### O que significa `...` (Ellipsis)?

`...` em Python é um objeto especial chamado `Ellipsis`. No Pydantic, significa **"campo obrigatório"**.

```python
# ❌ ERRADO - Campo sem valor padrão e sem Field
texto: str  # Isso também funciona, mas não tem validações extras

# ✅ CORRETO - Campo obrigatório com Field
texto: str = Field(...)  # Obrigatório + validações extras

# ✅ CORRETO - Campo opcional
texto: str = Field(default="")  # Opcional, se não vier usa ""
```

### Exemplos de Validação de String

```python
from pydantic import BaseModel, Field

class ValidacaoString(BaseModel):
    # String obrigatória, mínimo 1 caractere
    nome: str = Field(..., min_length=1, max_length=100)
    
    # String obrigatória, mínimo 5 caracteres, máximo 50
    senha: str = Field(..., min_length=5, max_length=50)
    
    # String opcional, se vier deve ter no mínimo 3 caracteres
    apelido: str = Field(default="", min_length=3)
    
    # String com regex (deve ser email)
    email: str = Field(..., pattern=r'^[\w\.-]+@[\w\.-]+\.\w+$')
    
    # String com descrição (aparece na documentação)
    descricao: str = Field(..., description="Descrição do produto")
```

### Exemplos de Validação de Números

```python
from pydantic import BaseModel, Field

class ValidacaoNumero(BaseModel):
    # Inteiro obrigatório, maior que 0
    idade: int = Field(..., gt=0, description="Idade deve ser positiva")
    
    # Inteiro obrigatório, maior ou igual a 18
    idade_minima: int = Field(..., ge=18, description="Idade mínima 18 anos")
    
    # Inteiro obrigatório, menor que 120
    idade_maxima: int = Field(..., lt=120, description="Idade máxima 120 anos")
    
    # Float obrigatório, entre 0.0 e 1.0
    confianca: float = Field(..., ge=0.0, le=1.0, description="Confiança entre 0 e 1")
    
    # Inteiro opcional, se vier deve ser múltiplo de 5
    quantidade: int = Field(default=0, multiple_of=5)
```

**Significados:**
- `gt` = Greater Than (maior que)
- `ge` = Greater or Equal (maior ou igual)
- `lt` = Less Than (menor que)
- `le` = Less or Equal (menor ou igual)
- `multiple_of` = Múltiplo de

---

## 4. Field() - Validações Avançadas

### Validação de Listas

```python
from pydantic import BaseModel, Field
from typing import List

class ValidacaoLista(BaseModel):
    # Lista de strings, mínimo 1 item, máximo 10 itens
    tags: List[str] = Field(..., min_length=1, max_length=10)
    
    # Lista de inteiros, cada inteiro deve ser maior que 0
    numeros: List[int] = Field(..., min_length=1)
    
    # Lista opcional
    opcoes: List[str] = Field(default=[])
```

### Validação de Dicionários

```python
from pydantic import BaseModel, Field
from typing import Dict

class ValidacaoDict(BaseModel):
    # Dicionário string -> string
    metadados: Dict[str, str] = Field(default={})
    
    # Dicionário string -> qualquer coisa
    extras: Dict[str, any] = Field(default={})
```

### Validação com Enum

```python
from pydantic import BaseModel, Field
from enum import Enum

class StatusEmail(str, Enum):
    PRODUTIVO = "Produtivo"
    IMPRODUTIVO = "Improdutivo"

class EmailComEnum(BaseModel):
    # Campo obrigatório que só aceita valores do Enum
    status: StatusEmail = Field(..., description="Status do email")
    
    # Se você enviar "Produtivo" ou "Improdutivo" → ✅
    # Se você enviar "Outro" → ❌ Erro de validação
```

### Validação com Optional

```python
from pydantic import BaseModel, Field
from typing import Optional

class ValidacaoOptional(BaseModel):
    # Campo obrigatório
    nome: str = Field(...)
    
    # Campo opcional (pode ser None ou string)
    sobrenome: Optional[str] = Field(None, description="Sobrenome opcional")
    
    # Campo opcional com valor padrão
    idade: Optional[int] = Field(default=None)
    
    # Campo opcional, mas se vier deve ser maior que 0
    peso: Optional[float] = Field(None, gt=0)
```

**Diferença:**
- `Optional[str] = Field(None)` → Pode ser `None` OU string
- `str = Field(default="")` → Sempre é string, mas pode ter valor padrão

---

## 5. Validadores Customizados

Às vezes você precisa de validações mais complexas que `Field()` não consegue fazer.

### Validador de Campo Único

```python
from pydantic import BaseModel, Field, field_validator

class Usuario(BaseModel):
    email: str = Field(..., description="Email do usuário")
    senha: str = Field(..., min_length=8)
    confirmar_senha: str = Field(..., min_length=8)
    
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
```

### Validador de Múltiplos Campos

```python
from pydantic import BaseModel, Field, model_validator

class UsuarioComSenha(BaseModel):
    senha: str = Field(..., min_length=8)
    confirmar_senha: str = Field(..., min_length=8)
    
    @model_validator(mode='after')
    def senhas_devem_ser_iguais(self):
        """Valida se as senhas são iguais"""
        if self.senha != self.confirmar_senha:
            raise ValueError('Senhas não coincidem')
        return self
```

**Diferença:**
- `@field_validator` → Valida UM campo por vez
- `@model_validator` → Valida o MODELO INTEIRO (pode acessar todos os campos)

---

## 6. Injeção de Dependência (FastAPI vs Spring Boot)

### Spring Boot (Java - O que você conhece)

```java
@RestController
public class EmailController {
    
    @Autowired  // Spring injeta automaticamente
    private EmailService emailService;
    
    @PostMapping("/classify")
    public ResponseEntity<?> classify(@RequestBody EmailRequest request) {
        return emailService.classify(request);
    }
}
```

### FastAPI (Python - Como funciona aqui)

```python
from fastapi import Depends
from app.services.email_service import EmailService

# Opção 1: Injeção manual (mais simples)
@router.post("/classify")
def classify(payload: RequisicaoEmailTexto):
    service = EmailService()  # Cria manualmente
    return service.classify(payload.texto)

# Opção 2: Injeção automática (mais profissional)
def obter_email_service() -> EmailService:
    """Função que cria/retorna o serviço"""
    return EmailService()

@router.post("/classify")
def classify(
    payload: RequisicaoEmailTexto,
    service: EmailService = Depends(obter_email_service)  # FastAPI injeta automaticamente
):
    return service.classify(payload.texto)
```

**Como funciona `Depends()`:**
1. FastAPI vê `Depends(obter_email_service)`
2. Chama `obter_email_service()` automaticamente
3. Passa o resultado como parâmetro `service`
4. Você não precisa criar manualmente!

**Vantagens:**
- ✅ Testes mais fáceis (pode mockar `obter_email_service`)
- ✅ Reutilização (mesmo serviço em vários endpoints)
- ✅ Controle de ciclo de vida (singleton, etc.)

---

## 7. Exemplos Práticos Completos

### Exemplo 1: Modelo Simples com Validações Básicas

```python
from pydantic import BaseModel, Field
from typing import Optional

class RequisicaoEmailTexto(BaseModel):
    """Modelo para receber texto de email na requisição"""
    
    # Campo obrigatório: string, mínimo 1 caractere
    texto: str = Field(
        ..., 
        min_length=1, 
        max_length=10000,
        description="Texto do email para classificar"
    )
    
    # Campo opcional: email do remetente
    email_remetente: Optional[str] = Field(
        None,
        pattern=r'^[\w\.-]+@[\w\.-]+\.\w+$',
        description="Email do remetente (opcional)"
    )
    
    # Campo opcional: prioridade (1-5)
    prioridade: Optional[int] = Field(
        default=3,
        ge=1,
        le=5,
        description="Prioridade do email (1-5)"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "texto": "Olá, gostaria de saber o status da minha requisição",
                "email_remetente": "cliente@exemplo.com",
                "prioridade": 4
            }
        }
```

### Exemplo 2: Modelo com Validações Complexas

```python
from pydantic import BaseModel, Field, field_validator, model_validator
from typing import List, Optional
from datetime import datetime
from enum import Enum

class StatusEmail(str, Enum):
    PRODUTIVO = "Produtivo"
    IMPRODUTIVO = "Improdutivo"

class RequisicaoEmailCompleta(BaseModel):
    """Modelo completo com validações avançadas"""
    
    # Campos obrigatórios básicos
    texto: str = Field(..., min_length=10, max_length=50000)
    remetente: str = Field(..., min_length=3, max_length=100)
    
    # Campo com Enum
    status_esperado: Optional[StatusEmail] = Field(None)
    
    # Lista de tags
    tags: List[str] = Field(default=[], max_length=10)
    
    # Data opcional
    data_envio: Optional[datetime] = None
    
    # Validador customizado para texto
    @field_validator('texto')
    @classmethod
    def validar_texto(cls, v: str) -> str:
        """Remove espaços extras e valida conteúdo"""
        v = v.strip()
        if len(v) < 10:
            raise ValueError('Texto deve ter pelo menos 10 caracteres')
        if 'spam' in v.lower():
            raise ValueError('Texto contém palavras proibidas')
        return v
    
    # Validador customizado para tags
    @field_validator('tags')
    @classmethod
    def validar_tags(cls, v: List[str]) -> List[str]:
        """Remove tags vazias e duplicadas"""
        v = [tag.strip().lower() for tag in v if tag.strip()]
        if len(v) != len(set(v)):
            raise ValueError('Tags não podem ser duplicadas')
        return v
    
    # Validador do modelo inteiro
    @model_validator(mode='after')
    def validar_modelo(self):
        """Validações que dependem de múltiplos campos"""
        if self.status_esperado == StatusEmail.PRODUTIVO:
            if len(self.texto) < 50:
                raise ValueError('Emails produtivos devem ter pelo menos 50 caracteres')
        return self
```

### Exemplo 3: Modelo com Herança

```python
from pydantic import BaseModel, Field

class RequisicaoBase(BaseModel):
    """Classe base com campos comuns"""
    texto: str = Field(..., min_length=1)
    remetente: str = Field(..., min_length=3)

class RequisicaoEmailSimples(RequisicaoBase):
    """Herda campos da base, adiciona apenas o necessário"""
    pass  # Só usa os campos da base

class RequisicaoEmailCompleta(RequisicaoBase):
    """Herda campos da base, adiciona campos extras"""
    prioridade: int = Field(default=3, ge=1, le=5)
    tags: List[str] = Field(default=[])
```

### Exemplo 4: Uso no Controller com Injeção de Dependência

```python
from fastapi import APIRouter, Depends, HTTPException
from app.models.schemas import RequisicaoEmailTexto, RespostaClassificacao
from app.services.classificador_servico import ClassificadorService

router = APIRouter(prefix="/api/emails", tags=["Emails"])

# Função de dependência (cria o serviço)
def obter_classificador() -> ClassificadorService:
    """Retorna instância do serviço de classificação"""
    return ClassificadorService()

# Endpoint com injeção de dependência
@router.post("/classify-text", response_model=RespostaClassificacao)
def classificar_texto(
    payload: RequisicaoEmailTexto,  # Validação automática do JSON
    classificador: ClassificadorService = Depends(obter_classificador)  # Injeção automática
):
    """
    Classifica texto de email
    
    - **payload**: JSON validado automaticamente (deve ter campo 'texto')
    - **classificador**: Serviço injetado automaticamente pelo FastAPI
    """
    try:
        # Usa o serviço injetado
        resultado = classificador.classificar(payload.texto)
        
        # Retorna modelo validado
        return RespostaClassificacao(
            label=resultado["label"],
            confidence=resultado["confidence"],
            suggested_reply=resultado["reply"]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
```

---

## 🎯 Resumo Final

### BaseModel
- ✅ Herança simples: `class MeuModelo(BaseModel)`
- ✅ Validação automática de tipos
- ✅ Conversão automática quando possível
- ✅ Geração de JSON Schema

### Field()
- ✅ `Field(...)` = Campo obrigatório
- ✅ `Field(default=valor)` = Campo opcional com valor padrão
- ✅ `Field(..., min_length=1)` = Validações extras
- ✅ `Field(..., description="...")` = Documentação

### Validadores
- ✅ `@field_validator('campo')` = Valida um campo
- ✅ `@model_validator(mode='after')` = Valida o modelo inteiro

### Injeção de Dependência
- ✅ `Depends(funcao)` = FastAPI chama a função e injeta o resultado
- ✅ Mais fácil de testar
- ✅ Reutilização de código

---

## 🔥 Dicas Finais

1. **Sempre use `Field(...)` para campos obrigatórios** se quiser validações extras
2. **Use `Optional[Tipo]` para campos opcionais** que podem ser `None`
3. **Use `Field(default=valor)` para campos opcionais** com valor padrão
4. **Validações complexas → use `@field_validator`**
5. **Validações que dependem de múltiplos campos → use `@model_validator`**

---

**Agora você domina Pydantic! 🚀**
