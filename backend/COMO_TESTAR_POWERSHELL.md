# 🧪 Como Testar no PowerShell

## ⚠️ Problema

No PowerShell, `curl` é um alias para `Invoke-WebRequest`, não o curl real. Por isso o `@` não funciona.

## ✅ Solução 1: Usar Invoke-RestMethod (RECOMENDADO)

Execute este comando no PowerShell:

```powershell
$body = Get-Content teste_email.json -Raw
Invoke-RestMethod -Uri "http://127.0.0.1:8000/api/emails/classify-text" -Method Post -ContentType "application/json" -Body $body
```

## ✅ Solução 2: Usar o script PowerShell

Execute:
```powershell
.\testar_powershell.ps1
```

## ✅ Solução 3: Usar curl.exe (se tiver instalado)

Se você tiver o curl real instalado, use:
```powershell
curl.exe -X POST http://127.0.0.1:8000/api/emails/classify-text -H "Content-Type: application/json" --data-binary "@teste_email.json"
```

## 🎯 Solução MAIS FÁCIL: Swagger UI

1. Acesse: `http://127.0.0.1:8000/docs`
2. Clique em `POST /api/emails/classify-text`
3. Clique em "Try it out"
4. Cole o texto
5. Clique em "Execute"

**É MUITO MAIS FÁCIL! Não precisa se preocupar com PowerShell, curl, ou escape de caracteres!**
