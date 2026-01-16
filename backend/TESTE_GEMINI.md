# 🔧 Como Testar o Gemini

## 1. Verificar se o arquivo .env existe

Crie um arquivo `.env` na pasta `backend/` com:

```env
GEMINI_API_KEY=sua_chave_aqui
GEMINI_MODEL=gemini-2.5-flash
```

## 2. Verificar se a API key está sendo carregada

Acesse: `http://127.0.0.1:8000/`

Se aparecer `"api_key_status": "✅ Configurada"` = OK
Se aparecer `"api_key_status": "❌ Não configurada"` = Problema no .env

## 3. Testar no Swagger

1. Acesse: `http://127.0.0.1:8000/docs`
2. Clique em `POST /api/emails/classify-text`
3. Clique em "Try it out"
4. Cole este exemplo:
```json
{
  "texto": "Olá, gostaria de saber o status da minha requisição #12345"
}
```
5. Clique em "Execute"

## 4. Possíveis Erros

### Erro: "API key do Gemini não configurada"
- **Solução:** Verifique se o arquivo `.env` existe na pasta `backend/`
- **Solução:** Verifique se a variável se chama `GEMINI_API_KEY` (sem espaços)

### Erro: "Erro ao inicializar cliente Gemini"
- **Solução:** Verifique se a API key está correta
- **Solução:** Verifique se há conexão com a internet

### Erro: "Erro ao classificar email com Gemini"
- **Solução:** Verifique se a API key é válida
- **Solução:** Verifique se há créditos na conta do Google AI Studio

## 5. Como obter a API key

1. Acesse: https://aistudio.google.com/apikey
2. Faça login com sua conta Google
3. Clique em "Create API Key"
4. Copie a chave gerada
5. Cole no arquivo `.env`

## 6. Verificar logs no terminal

Quando você rodar `uvicorn app.main:app --reload`, verifique se aparecem erros no terminal.
