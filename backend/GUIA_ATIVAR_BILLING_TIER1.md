# 🚀 Guia: Como Ativar Billing Tier 1 no Google Cloud (Gemini API)

## 📋 O que você ganha com Tier 1:

| Métrica | Free Tier | Tier 1 (com Billing) |
|---------|-----------|----------------------|
| **Requisições/Dia** | 20 | ~10.000 |
| **Requisições/Minuto** | ~1 | ~150 |
| **Tokens/Minuto** | Baixo | ~2 milhões |
| **Custo** | Gratuito | Paga apenas o que usar |

**💰 Custo estimado:** ~$0,0001 por requisição (muito barato!)

---

## 🛠️ Passo a Passo Completo

### **Passo 1: Acesse o Google Cloud Console**

1. Acesse: https://console.cloud.google.com/
2. Faça login com sua conta Google (a mesma que usa para Gemini API)

---

### **Passo 2: Crie ou Selecione um Projeto**

1. No topo da página, clique no dropdown de projetos
2. Clique em **"NEW PROJECT"** (Novo Projeto)
3. Preencha:
   - **Nome do projeto:** `EmailClassifier` (ou qualquer nome)
   - **Organization:** (deixe padrão se não tiver)
4. Clique em **"CREATE"** (Criar)
5. Aguarde alguns segundos enquanto o projeto é criado

> ⚠️ **Importante:** Anote o **Project ID** (vai precisar depois)

---

### **Passo 3: Ative a API do Gemini**

1. No menu lateral, vá em **"APIs & Services"** → **"Library"**
2. Pesquise por: **"Generative Language API"**
3. Clique no resultado **"Generative Language API"**
4. Clique em **"ENABLE"** (Ativar)
5. Aguarde a ativação (pode levar alguns segundos)

---

### **Passo 4: Configure o Billing (Faturamento)**

1. No menu lateral, vá em **"Billing"** (Faturamento)
2. Se não tiver nenhuma conta de billing:
   - Clique em **"LINK A BILLING ACCOUNT"** (Vincular conta de faturamento)
   - Clique em **"CREATE BILLING ACCOUNT"** (Criar conta de faturamento)
3. Preencha o formulário:
   - **Account name:** `EmailClassifier Billing` (ou qualquer nome)
   - **Country/Region:** Selecione seu país
   - **Currency:** USD (ou sua moeda)
   - **Legal name:** Seu nome completo (ou empresa)
   - **Address:** Seu endereço
4. Clique em **"SUBMIT AND ENABLE BILLING"** (Enviar e ativar faturamento)

> 💳 **Método de Pagamento:**
> - Você precisará adicionar um cartão de crédito ou débito
> - O Google pode fazer uma verificação (geralmente ~$1 que é reembolsado)
> - **IMPORTANTE:** Você só paga pelo que usar, não há mensalidade mínima!

---

### **Passo 5: Vincule o Billing ao Projeto**

1. Se ainda estiver na tela de billing, selecione o projeto que criou
2. Ou vá em **"Billing"** → Selecione sua conta → **"MANAGE BILLING ACCOUNTS"**
3. Clique em **"LINK PROJECT"** (Vincular projeto)
4. Selecione o projeto criado no Passo 2
5. Clique em **"LINK"** (Vincular)

---

### **Passo 6: Verifique o Tier no Google AI Studio**

1. Acesse: https://aistudio.google.com/
2. No canto superior direito, clique no ícone de **perfil**
3. Vá em **"Settings"** (Configurações)
4. Procure por **"API Key"** ou **"Usage & Billing"**
5. Verifique o **Tier** (deve mostrar "Tier 1" ou "Paid")

> ✅ **Status esperado:** 
> - Antes: "Free Tier" (20 requisições/dia)
> - Depois: "Tier 1" ou "Paid" (~10.000 requisições/dia)

---

### **Passo 7: Atualize a API Key (Opcional, mas Recomendado)**

1. Se você quiser, pode criar uma nova API key vinculada ao projeto com billing:
   - Acesse: https://aistudio.google.com/apikey
   - Clique em **"Create API Key"**
   - Selecione o projeto com billing ativado
   - Copie a nova API key
   - Atualize o arquivo `.env` no backend:
     ```env
     GEMINI_API_KEY=nova_chave_aqui
     ```

> ℹ️ **Nota:** Sua API key antiga também deve funcionar, mas vincular ao projeto com billing garante que está usando o Tier 1.

---

### **Passo 8: Teste a Nova Cota**

1. Reinicie seu backend (se estiver rodando)
2. Faça uma requisição de teste
3. Verifique os logs — não deve mais aparecer erro 429!

---

## ⚠️ Importante: Custos e Proteções

### **Quanto custa?**

- **Custo por requisição:** ~$0,0001 (muito barato!)
- **Exemplo:** 1.000 requisições = ~$0,10
- **Sem mensalidade mínima:** Você paga apenas o que usar

### **Proteções contra gastos inesperados:**

1. **Orçamentos e Alertas:**
   - Vá em **"Billing"** → **"Budgets & Alerts"**
   - Crie um orçamento mensal (ex: $10)
   - Configure alertas por email quando atingir 50%, 90%, 100%

2. **Limite de Gastos:**
   - Vá em **"Billing"** → **"Account Settings"**
   - Configure um limite diário/mensal se desejar

3. **Monitoramento:**
   - Vá em **"APIs & Services"** → **"Dashboard"**
   - Monitore o uso da API em tempo real

---

## ❓ FAQ (Perguntas Frequentes)

### **P: Vou ser cobrado imediatamente?**
R: Não! Você só paga pelo que usar. O Google pode fazer uma verificação de ~$1 no cartão, mas é reembolsado.

### **P: Posso desativar o billing depois?**
R: Sim! Você pode desativar o billing a qualquer momento. A API voltará ao Free Tier.

### **P: O que acontece se eu exceder o limite do Tier 1?**
R: Você pode solicitar aumento de quota ou pode ser cobrado além do limite (mas com proteções de orçamento).

### **P: Preciso mudar minha API key?**
R: Não necessariamente. Sua API key atual deve funcionar com Tier 1, mas vincular ao projeto com billing é recomendado.

### **P: Quanto tempo leva para o Tier 1 ficar ativo?**
R: Geralmente é imediato após ativar o billing. Pode levar alguns minutos em casos raros.

---

## 🔗 Links Úteis

- **Google Cloud Console:** https://console.cloud.google.com/
- **Google AI Studio:** https://aistudio.google.com/
- **Documentação Gemini API:** https://ai.google.dev/gemini-api/docs
- **Billing Documentation:** https://cloud.google.com/billing/docs
- **Rate Limits:** https://ai.google.dev/gemini-api/docs/rate-limits

---

## ✅ Checklist Final

- [ ] Projeto criado no Google Cloud
- [ ] Generative Language API ativada
- [ ] Conta de billing criada
- [ ] Billing vinculado ao projeto
- [ ] Verificado Tier 1 no Google AI Studio
- [ ] API key atualizada (opcional)
- [ ] Teste realizado com sucesso
- [ ] Orçamento/configurações de alerta configurados (recomendado)

---

## 🆘 Precisa de Ajuda?

Se encontrar problemas:

1. Verifique se o billing está realmente vinculado ao projeto
2. Aguarde alguns minutos (pode levar um tempo para processar)
3. Verifique os logs do backend para ver erros específicos
4. Consulte a documentação oficial: https://ai.google.dev/gemini-api/docs/billing

---

**🎉 Pronto! Com o Tier 1 ativado, você tem ~10.000 requisições/dia ao invés de apenas 20!**
