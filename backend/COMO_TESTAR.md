# 🧪 Como Testar a API

## ⚠️ Problema com Curl e Quebras de Linha

Quando você cola texto com quebras de linha direto no curl, o JSON fica inválido. 

## ✅ Solução 1: Usar Swagger UI (RECOMENDADO)

1. Acesse: `http://127.0.0.1:8000/docs`
2. Clique em `POST /api/emails/classify-text`
3. Clique em "Try it out"
4. Cole o texto no campo `texto` (o Swagger faz o escape automaticamente)
5. Clique em "Execute"

**É MUITO MAIS FÁCIL!** O Swagger trata tudo automaticamente.

## ✅ Solução 2: Usar arquivo JSON

1. Use o arquivo `teste_email.json` que está na pasta `backend/`
2. Execute:
```bash
curl -X POST http://127.0.0.1:8000/api/emails/classify-text \
  -H "Content-Type: application/json" \
  -d @teste_email.json
```

## ✅ Solução 3: Curl com texto escapado

Se quiser usar curl direto, precisa escapar as quebras de linha:

```bash
curl -X POST http://127.0.0.1:8000/api/emails/classify-text \
  -H "Content-Type: application/json" \
  -d '{"texto": "Boa tarde!\\n\\nApós análise, você foi aprovado."}'
```

## 🎯 Endpoint de Teste Simples

Para testar o Gemini diretamente (sem classificação):

```bash
curl -X POST http://127.0.0.1:8000/api/emails/teste-gemini \
  -H "Content-Type: application/json" \
  -d '{"texto": "Olá, como você está?"}'
```

## 💡 Dica

**SEMPRE use o Swagger UI (`/docs`) para testar!** É muito mais fácil e não tem problema com escape de caracteres.
