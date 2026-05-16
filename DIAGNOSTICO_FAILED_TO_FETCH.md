# 🔧 Diagnóstico: Erro "Failed to fetch"

Você está recebendo **"Failed to fetch"** ao tentar usar o JARVIS? Vamos resolver!

## Passo 1: Abra DevTools e Teste a API

### 1a. Abra o DevTools
- Pressione **F12** ou **Ctrl+Shift+I**
- Vá para a aba **Console**

### 1b. Teste a Conectividade
No seu navegador, digite na barra de endereços:
```
https://llm.liaufms.org/v1/gemma-3-12b-it/chat/completions
```

**Resultado esperado:**
- ✅ Você vê um erro JSON (como `{"error": "..."}`) → Servidor está online ✓
- ❌ Você vê `ERR_NAME_NOT_FOUND` → Domínio não resolve (problema de DNS)
- ❌ Você vê branco/vazio → CORS ou servidor offline

### 1c. Use o Teste de API do JARVIS
1. Abra `jarvis_academico.html`
2. Vá para o painel **Logs**
3. Clique em **"🧪 Testar Conexão Gemma"**
4. Veja o resultado

---

## Passo 2: Analise a Causa

### Cenário A: ✅ Teste passou mas chat não funciona
**Causa provável**: Problema em outra parte do código (não é rede)

**Solução:**
1. Abra DevTools → Console
2. Digite uma mensagem no chat
3. Verifique se há erros JavaScript no console
4. Se houver erro, reporte-o (junto com screenshot)

---

### Cenário B: ❌ "Failed to fetch" no teste de API
Pode ser uma de 4 coisas:

#### B1: **CORS Bloqueado**
O servidor `llm.liaufms.org` pode não aceitar requisições diretas do navegador.

**Dica no console:**
```javascript
// No console (F12), teste isto:
fetch('https://llm.liaufms.org/v1/gemma-3-12b-it/chat/completions', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ model: 'test', messages: [] })
}).catch(e => console.log('Erro:', e.message))
```

Se vir `Access to fetch blocked by CORS policy` → É CORS.

**Solução para CORS:**
- Não há solução no frontend (servidor precisa habilitar CORS)
- Contacte o professor para:
  1. Habilitar CORS headers na API
  2. Ou fornecer um proxy/backend intermediário

---

#### B2: **VPN/Firewall/Proxy Corporativo**
Sua rede (trabalho/escola) está bloqueando `llm.liaufms.org`

**Teste:**
1. Tente em outro WiFi (ex: celular hotspot)
2. Se funcionar → É problema de rede

**Solução:**
- Use outro WiFi/conexão
- Ou peça ao admin de rede para desbloquear o domínio

---

#### B3: **DNS Quebrado**
Seu computador não consegue resolver `llm.liaufms.org`

**Teste (Windows PowerShell admin):**
```powershell
nslookup llm.liaufms.org
ping llm.liaufms.org
```

Se ver `Non-existent domain` → DNS está quebrado.

**Solução:**
```powershell
# No PowerShell (como admin):
ipconfig /flushdns
ipconfig /renew
```

Depois tente novamente.

---

#### B4: **Servidor Offline**
O servidor `llm.liaufms.org` está fora do ar.

**Teste:**
Visite na barra de endereços (não vai renderizar, mas se conectar já é sucesso):
```
https://llm.liaufms.org
```

Se página não carrega → Servidor está offline.

**Solução:**
- Aguarde o servidor voltar
- Contacte o professor

---

## Passo 3: Verifique Configuração

Abra `jarvis_academico.html` com um editor de texto (Notepad++) e procure por:

```javascript
const API_URL = 'https://llm.liaufms.org/v1/gemma-3-12b-it/chat/completions';
const API_KEY = 'Cxt2ftLF7d3mHS2JdiFqB-eSDAQeZvFATPXPs02lV9A';
const MODEL = 'gemma-3-12b-it';
```

✅ Certifique-se de que:
- `API_URL` começa com `https://` (não `http://`)
- `API_KEY` não está vazio ou com `undefined`
- `MODEL` é exatamente `gemma-3-12b-it`

---

## Passo 4: Debug no Console

Cole isto no DevTools → Console:

```javascript
// Teste 1: Verificar configuração
console.log('API_URL:', API_URL);
console.log('API_KEY:', API_KEY.substring(0, 10) + '...');
console.log('MODEL:', MODEL);

// Teste 2: Fazer requisição de teste
fetch(API_URL, {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer ' + API_KEY
  },
  body: JSON.stringify({
    model: MODEL,
    messages: [{ role: 'user', content: 'Hi' }],
    max_tokens: 10
  })
})
.then(r => {
  console.log('HTTP Status:', r.status);
  return r.json().then(d => ({ status: r.status, data: d }));
})
.then(result => console.log('Resposta:', result))
.catch(err => console.error('Erro:', err.message, err.stack));
```

**Resultado esperado:**
- ✅ Vê `HTTP Status: 200` → API funciona!
- ❌ Vê `Erro: Failed to fetch` → Problema de rede
- ❌ Vé `HTTP Status: 401` → API Key inválida

---

## Passo 5: Últimos Testes

Se nada funcionou:

### Teste Online
Visite: https://jsonplaceholder.typicode.com/posts/1

Se isto não funcionar → **Problema é sua internet**

### Teste Domínio
```javascript
// No console:
fetch('https://llm.liaufms.org')
  .then(() => console.log('✅ Conectou'))
  .catch(e => console.log('❌ Erro:', e.message));
```

---

## Resumo de Soluções Rápidas

| Erro | Causa Provável | Solução |
|------|---|---|
| **Failed to fetch** + Teste OK | Erro em outra parte | Verifique console para JS errors |
| **Failed to fetch** + Teste falha | CORS | Contacte professor |
| **Failed to fetch** no celular | Proxy corporativo | Use outro WiFi |
| **DNS error** | DNS quebrado | `ipconfig /flushdns` |
| **Timeout** | Servidor lento | Aguarde ou tente depois |
| **HTTP 401** | API Key inválida | Verifique chave no código |
| **HTTP 429** | Rate limit | Aguarde 5-10 minutos |

---

## Contacte o Professor Com:

Se nenhuma solução funcionar, envie ao professor:

1. **Screenshot** da mensagem de erro
2. **Resultado do teste** 🧪 (clique botão no painel Logs)
3. **Console output** (F12 → Console → copie tudo)
4. **Seu sistema operacional** (Windows/Mac/Linux)
5. **Tipo de rede** (WiFi/Ethernet/Celular 4G)

---

**Versão**: 1.0  
**Data**: 2024  
