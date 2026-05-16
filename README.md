# 📚 JARVIS Acadêmico - Sistema de Assistência Inteligente para Estudos

**Versão**: 1.0  
**Data**: Maio 2026  
**Modelo**: Gemma 3 12B-IT (Google)  
**Arquitetura**: RAG + Tool Calling + LLM  

---

## 📋 Índice

1. [Visão Geral](#visão-geral)
2. [Arquitetura](#arquitetura)
3. [Funcionalidades](#funcionalidades)
4. [Dataset e Conhecimento](#dataset-e-conhecimento)
5. [Sistema de Avaliação](#sistema-de-avaliação)
6. [Análise de Erros](#análise-de-erros)
7. [Como Usar](#como-usar)
8. [Configuração](#configuração)
9. [Melhorias Futuras](#melhorias-futuras)

---

## 🎯 Visão Geral

JARVIS Acadêmico é um assistente inteligente baseado em **Retrieval-Augmented Generation (RAG)** e **Tool Calling** para suportar estudantes de Ciência da Computação em:

- 📚 **Consulta a Materiais**: Busca semântica em base de conhecimento com 25+ chunks
- 📅 **Agenda Acadêmica**: Visualização e consulta a eventos (aulas, provas, trabalhos)
- ✅ **Gerenciamento de Tarefas**: Adicionar, marcar conclusão, priorizar tarefas
- 🧠 **Active Recall**: Geração de exercícios e questões para revisão
- 📊 **Avaliação Systemática**: 10 perguntas de teste com feedback automático
- 🔍 **Rastreamento**: Logs de todas as ferramentas executadas

---

## 🏗️ Arquitetura

### Componentes Principais

```
┌─────────────────────────────────────────────────────┐
│              INTERFACE (HTML/CSS/JS)                 │
│  - Chat Panel (5+ painéis navegáveis)                │
│  - Real-time Rendering (React-like state updates)    │
└──────────────────┬──────────────────────────────────┘
                   │
        ┌──────────┴──────────┐
        │                     │
    ┌───▼──────┐      ┌──────▼────────┐
    │ TOOLS    │      │ LLM (Gemma)    │
    │ CALLING  │◄────►│ 12B-IT         │
    └────┬─────┘      └────────────────┘
         │
    ┌────▼────────────────────────────┐
    │  RAG (Retrieval-Augmented Gen)  │
    │  - Knowledge Base (25 chunks)    │
    │  - TF-based Retrieval             │
    └────────────────────────────────┘
```

### Fluxo de Requisição

1. **Usuário envia mensagem** no chat
2. **detectTools()** analisa a mensagem com regex + keywords
3. **Se ferramentas detectadas**:
   - Executa tool(args) → obtém resultado
   - Passa resultado para LLM como contexto
4. **callLLM()** envia para Gemma com:
   - System prompt (instruções)
   - Chat history (últimas 6 mensagens)
   - Tool results (contexto recuperado)
5. **Gemma responde** naturalmente, integrando dados das tools
6. **Mensagem é renderizada** e adicionada ao histórico

---

## ✨ Funcionalidades

### 1. **Consulta a Materiais (RAG)**
- **Tool**: `buscar_material_rag(query)`
- **Método**: TF (Term Frequency) com tokenização + keywords
- **Base**: 25 chunks documentados com origem (Wikipedia, livros, papers)
- **Exemplo**: 
  ```
  Usuário: "Explique entropia em árvores de decisão"
  → Tool: buscar_material_rag(query="entropia ganho informação")
  → Retorna: [3 chunks] sobre entropia em TDIDT
  → Gemma: Integra dados + explica naturalmente
  ```

### 2. **Agenda Acadêmica**
- **Tool**: `consultar_agenda(periodo: "hoje" | "amanhã" | "semana")`
- **Dados**: 10 eventos pré-carregados (2025-01-13 a 2025-01-17)
- **Tipos**: Aulas, Provas, Trabalhos
- **UI**: Painel com agendamento por data e tipo de evento

### 3. **Lista de Tarefas**
- **Tools**:
  - `listar_tarefas(filtro: "pendentes" | "concluídas")`
  - `adicionar_tarefa(texto, prioridade)`
  - `concluir_tarefa(id_ou_nome)`
- **Prioridades**: Alta, Média, Baixa
- **Estatísticas**: Pendentes, Concluídas, % Progresso

### 4. **Exercícios e Active Recall**
- **Tool**: `gerar_exercicio(tópico)`
- **Tópicos**: Árvores de Decisão, Entropia, IA Geral
- **Formato**: Questão descritiva com dicas
- **Integração**: Detecta "me faça perguntas", "active recall" etc.

### 5. **Sistema de Avaliação (10 Questões)**
- **Tool**: `gerar_questao_avaliacao(id_questao: 1-10)`
- **Tool**: `avaliar_resposta(id_questao, resposta_usuario)`
- **Tipos**: Conceitual (30%), Técnico (70%)
- **Critério**: Palavras-chave esperadas (70%+ = correta, 40%-70% = parcial)
- **Feedback**: Automático com conceitos faltantes

### 6. **Logs de Tool Calling**
- **Rastreamento**: Todas as ferramentas executadas
- **Dados**: Tempo, Tool, Input, Output, Status
- **UI**: Painel com estatísticas (total, sucesso, erros)

---

## 📊 Dataset e Conhecimento

### Cobertura (25 chunks)

| Tópico | Chunks | Fontes | Keywords |
|--------|--------|--------|----------|
| **IA Geral** | 5 | Wikipedia, Russel & Norvig, MIT OCW | ia, turing, transformers, historia |
| **Árvores de Decisão** | 8 | Quinlan, Breiman, Tan et al | tdidt, entropia, ganho, poda |
| **Aprendizado de Máquina** | 6 | Goodfellow, Ng, Mitchell | supervisionado, validação, overfitting |
| **Embeddings** | 3 | Bengio, Sentence-BERT, OpenAI | embedding, rag, similaridade |
| **Avaliação** | 3 | NIST, Ribeiro, Goodfellow | teste, interpretavel, robustez |

### Estratégia de Retrieval

**Método**: TF com Keywords Manuais
- ✅ **Vantagens**: Rápido, interpretável, sem dependências
- ❌ **Limitações**: Sem semântica real, falha em sinônimos
- **Exemplo de falha**: "redes neurais" ≠ "deep learning" (diferentes keywords)

**Melhoria Proposta**: Implementar embeddings reais (Sentence-Transformers)

---

## 📝 Sistema de Avaliação

### 10 Questões de Teste

| ID | Pergunta | Tipo | Keywords Esperadas |
|----|----------|------|-------------------|
| 1 | Teste de Turing? | Conceitual | turing, inteligencia, máquina |
| 2 | Entropia vs Ganho? | Técnico | entropia, ganho, informação |
| 3 | TDIDT seleciona atributo? | Conceitual | tdidt, ganho, máximo |
| 4 | Overfitting e pós-poda? | Técnico | overfitting, poda, validação |
| 5 | Supervisionado vs Não-Supervisionado? | Conceitual | supervisionado, labels |
| 6 | Fórmula Recall? | Técnico | recall, verdadeiro, positivo |
| 7 | O que são Embeddings? | Conceitual | embedding, vetorial, rag |
| 8 | Fluxo RAG completo? | Técnico | rag, vetorizar, contexto |
| 9 | Gain Ratio > Ganho Simples? | Conceitual | gain, ratio, penaliza |
| 10 | Vantagens/Limitações Árvores? | Técnico | interpretavel, instabilidade |

### Critério de Avaliação

```javascript
matchPercentage = (palavras_chave_encontradas / palavras_chave_esperadas) * 100

if (matchPercentage >= 70%)
  status = "CORRETA" // Demonstrou compreensão
else if (matchPercentage >= 40%)
  status = "PARCIAL" // Conceitos faltando
else
  status = "INCORRETA" // Não responde adequadamente
```

### Exemplo de Uso

```
Usuário: "Me faça a questão 1"
→ Tool: gerar_questao_avaliacao(id_questao=1)
→ Retorna: "O que é o Teste de Turing?"

Usuário: "É um teste para avaliar se uma máquina consegue conversar como humano"
→ Tool: avaliar_resposta(id_questao=1, resposta="...")
→ Status: CORRETA
→ Feedback: "Excelente! Você demonstrou compreensão dos conceitos-chave."
```

---

## 🚨 Análise de Erros

### ERRO 1: RAG com TF Básico (Sem Embeddings Reais)

**Problema**:
- Tokenização simples + keywords manualmente definidas
- Não captura semântica (sinônimos, conceitos relacionados)
- Buscas falham para variações de termos

**Cenário**:
- Usuário: "O que são redes neurais?"
- Base contém: "deep learning" com keywords ['deep', 'learning', 'redes']
- TF: Busca por "redes, neurais" → match parcial (1/2)
- Resultado: Pode não recuperar ou recuperar com score baixo

**Solução**:
```python
# Implementar Sentence-Transformers (production)
from sentence_transformers import SentenceTransformer
model = SentenceTransformer('distiluse-base-multilingual-cased-v2')

query_embedding = model.encode("O que são redes neurais?")
chunk_embeddings = [model.encode(c['text']) for c in knowledgeBase]
scores = cosine_similarity([query_embedding], chunk_embeddings)[0]
top_k = np.argsort(scores)[-3:][::-1]
```

### ERRO 2: Tool Calling por Lógica Fixa (Não por LLM)

**Problema**:
- `detectTools()` usa regex + keywords hardcoded
- LLM (Gemma) não decide quais ferramentas chamar
- Não compreende variações ou intenções complexas

**Cenário**:
- Usuário: "Quais aulas tenho na próxima semana?"
- Regex: `/agenda|aula|tenho/i` detecta "aula" + "tenho"
- Mas: Se usuário disser "Mostre minha agenda semanal" (sem "aula")
- Resultado: Ferramenta pode não ser acionada

**Solução**:
```javascript
// Passar tool schemas para Gemma (OpenAI-style)
const tools = [
  {
    "type": "function",
    "function": {
      "name": "consultar_agenda",
      "description": "Consulta eventos acadêmicos por período",
      "parameters": {
        "type": "object",
        "properties": {
          "periodo": { "type": "string", "enum": ["hoje", "amanhã", "semana"] }
        }
      }
    }
  }
  // ... mais tools
];

// Gemma.messages com tool_choice="auto" gera chamadas JSON
// Frontend valida e executa
```

### ERRO 3: Sem Sanitização de Input

**Problema**:
- `avaliar_resposta()` recebe resposta_usuario sem validação
- XSS potencial ao renderizar no HTML
- DoS possível com strings muito grandes

**Cenário**:
```
resposta_usuario = "<img src=x onerror='alert(\"XSS\")'>"
→ Renderizado no chat sem escape
→ Script executado

resposta_usuario = "A" * 1000000
→ Processamento lento, memory leak
```

**Solução**:
```javascript
function sanitizeInput(text) {
  // Remover tags HTML
  text = text.replace(/<[^>]*>/g, '');
  
  // Limitar tamanho (ex: 500 chars)
  if (text.length > 500) text = text.substring(0, 500);
  
  // Remover caracteres de controle
  text = text.replace(/[\x00-\x1F\x7F]/g, '');
  
  return text;
}

const resposta = sanitizeInput(args.resposta_usuario);
const tokensSanitized = tokenize(resposta);
```

### ERRO 4: API Key Exposta em Client-Side

**Problema**:
- Credenciais Gemma (`API_KEY`) visíveis no código-fonte HTML
- Qualquer pessoa pode inspecionar e copiar a chave
- Abuso de quota API

**Cenário**:
```
Usuário abre DevTools (F12) → Ctrl+F → "Cxt2ftLF7d3..."
→ Copia a chave
→ Usa em outro lugar ou compartilha
```

**Solução**:
```javascript
// Backend (Node.js / Python Flask)
app.post('/api/llm', async (req, res) => {
  const { messages } = req.body;
  
  // Backend guarda a chave segura (environment variable)
  const API_KEY = process.env.GEMMA_API_KEY;
  
  const response = await fetch('https://llm.liaufms.org/...', {
    headers: { 'Authorization': `Bearer ${API_KEY}` },
    body: JSON.stringify({ messages, ... })
  });
  
  res.json(response.json());
});

// Frontend só faz requisição local
const response = await fetch('/api/llm', {
  method: 'POST',
  body: JSON.stringify({ messages })
});
```

### ERRO 5: Sem Retry/Timeout em API Calls

**Problema**:
- Se Gemma lento ou retornar erro 429 (rate limit), app trava
- Sem timeout configurado, requisição pode ficar pendente infinitamente
- Sem retry, erro transiente mata a experiência

**Cenário**:
```
Múltiplos usuários → muitas requisições simultâneas
→ Gemma retorna: 429 Too Many Requests
→ App mostra: "Erro ao conectar..."
→ Usuário recarrega página (pior ainda)
```

**Solução**:
```javascript
async function callLLMWithRetry(msg, toolResults, maxRetries = 3) {
  for (let attempt = 1; attempt <= maxRetries; attempt++) {
    try {
      const controller = new AbortController();
      const timeout = setTimeout(() => controller.abort(), 10000); // 10s timeout
      
      const response = await fetch(API_URL, {
        signal: controller.signal,
        // ... headers, body
      });
      
      clearTimeout(timeout);
      
      if (response.status === 429) {
        // Rate limit: aguardar exponencial
        const waitTime = Math.pow(2, attempt) * 1000;
        console.log(`Rate limited. Retrying in ${waitTime}ms...`);
        await new Promise(r => setTimeout(r, waitTime));
        continue;
      }
      
      if (!response.ok) throw new Error(`HTTP ${response.status}`);
      return await response.json();
      
    } catch (error) {
      if (attempt === maxRetries) throw error;
      console.warn(`Attempt ${attempt} failed:`, error.message);
    }
  }
}
```

### ERRO 6: Dataset Limitado (25 chunks)

**Problema**:
- Cobertura insuficiente para buscas diversificadas
- Conceitos importantes podem estar ausentes (SVM, Naive Bayes, etc.)
- Buscas por tópicos não cobertos retornam "não encontrado"

**Cenário**:
```
Usuário: "Explique Support Vector Machines (SVM)"
→ Base: Sem chunks sobre SVM
→ Resultado: "Nenhum trecho relevante encontrado"
```

**Solução**:
```python
# Python script para expandir dataset com Web Scraping

import requests
from bs4 import BeautifulSoup
import json

topics = [
  "Support Vector Machines",
  "Naive Bayes",
  "K-means Clustering",
  "Gradient Descent"
]

for topic in topics:
  # Buscar em Wikipedia
  url = f"https://en.wikipedia.org/wiki/{topic}"
  response = requests.get(url)
  soup = BeautifulSoup(response.content, 'html.parser')
  
  paragraphs = soup.find_all('p')[:3]  # Primeiras 3 paráfrases
  
  for i, para in enumerate(paragraphs):
    chunk = {
      "id": f"k_scraped_{len(knowledgeBase) + i}",
      "doc": f"{topic} - Wikipedia",
      "source": f"Wikipedia - {topic}",
      "text": para.get_text(),
      "keywords": topic.lower().split() + ["machine", "learning"]
    }
    knowledgeBase.append(chunk)

# Ou usar API acadêmica (arXiv)
import arxiv

client = arxiv.Client()
results = client.results(arxiv.Search(query="machine learning classification"))
for result in results[:5]:
  chunk = {
    "id": f"arxiv_{result.entry_id}",
    "doc": result.title,
    "source": f"arXiv - {result.published.year}",
    "text": result.summary,
    "keywords": result.title.lower().split()
  }
  knowledgeBase.append(chunk)

# Salvar expandido
with open('knowledgebase_expanded.json', 'w') as f:
  json.dump(knowledgeBase, f, ensure_ascii=False, indent=2)
```

---

## 📖 Como Usar

### 1. Abrir a Aplicação
- Arquivo: `jarvis_academico.html`
- Browser: Chrome, Firefox, Edge (moderno)
- Sem instalação necessária (pure HTML/JS)

### 2. Interface

**Sidebar (esquerda)**:
- 🗨️ Chat (padrão)
- 📅 Agenda
- ✅ Tarefas
- 📚 Materiais RAG
- 🔍 Logs

**Chat Area**:
- Input: Digite pergunta ou comando
- Quick Actions: Botões pré-definidos
- Histórico: Conversa com timestamps

### 3. Exemplos de Uso

#### Exemplo 1: Consultar Agenda
```
Você: "O que tenho hoje?"
JARVIS: [Executa: consultar_agenda("hoje")]
        08:00 - Inteligência Artificial (aula) @ Lab 204
        10:00 - Estrutura de Dados (aula) @ Sala 102
        ...
```

#### Exemplo 2: Aprender com RAG
```
Você: "Explique entropia em árvores de decisão"
JARVIS: [Executa: buscar_material_rag("entropia ganho")]
        [Recupera 3 chunks]
        Entropia mede o grau de mistura de classes...
        O atributo escolhido fornece o Ganho Máximo...
```

#### Exemplo 3: Gerar Exercício
```
Você: "Me faça um exercício sobre árvores"
JARVIS: [Executa: gerar_exercicio("arvores")]
        Questão: Dada tabela com atributos [Tempo, Temp, Umidade]...
        calcule entropia e ganho de informação...
```

#### Exemplo 4: Sistema de Avaliação
```
Você: "Questão 1"
JARVIS: [Executa: gerar_questao_avaliacao(1)]
        [Questão] O que é Teste de Turing?
        
Você: "É um teste para avaliar inteligência de uma máquina"
JARVIS: [Executa: avaliar_resposta(1, resposta)]
        [Status: CORRETA]
        Excelente! Você demonstrou compreensão...
```

#### Exemplo 5: Plano de Estudos
```
Você: "Monte um plano de estudos para amanhã"
JARVIS: [Executa: consultar_agenda("amanha")]
        [Executa: listar_tarefas("pendentes")]
        
        PLANO PARA AMANHÃ:
        - 08:00: Prova Cálculo II (revisar...)
        - 14:00: Redes de Computadores (acompanhar)
        
        TAREFAS CRÍTICAS:
        1. Estudar Árvores de Decisão (ALTA)
        2. Implementar RAG (ALTA)
        ...
```

---

## ⚙️ Configuração

### Pré-requisitos
- ✅ Browser moderno (Chrome 90+, Firefox 88+, Edge 90+)
- ✅ Conexão à internet (para Gemma API)
- ✅ Acesso a `https://llm.liaufms.org` (rede da UFMS)

### Variáveis de Configuração

No código (linhas 238-244):
```javascript
const API_URL = 'https://llm.liaufms.org/v1/gemma-3-12b-it/chat/completions';
const API_KEY = 'Cxt2ftLF7d3mHS2JdiFqB-eSDAQeZvFATPXPs02lV9A';
const MODEL   = 'google/gemma-3-12b-it';
```

**Para mudar para outra LLM**:
```javascript
// OpenAI ChatGPT
const API_URL = 'https://api.openai.com/v1/chat/completions';
const API_KEY = 'sk-...';
const MODEL   = 'gpt-4-turbo';

// Local (Ollama)
const API_URL = 'http://localhost:11434/v1/chat/completions';
const MODEL   = 'mistral';
```

### Limites e Timeouts
```javascript
// RAG: Top-K chunks
const topK = 3; // Aumentar para mais contexto (custo)

// LLM: Máximo de tokens
max_tokens: 1024 // Aumentar para respostas mais longas

// Chat History: Últimas N mensagens
state.chatHistory.slice(-6) // Aumentar para mais contexto
```

---

## 🚀 Melhorias Futuras

### Curto Prazo (Priority 1)
- [ ] Implementar **Sentence-Transformers** para embeddings reais
- [ ] Mover API Key para backend (proxy Node.js/Python)
- [ ] Adicionar **retry com backoff exponencial**
- [ ] Sanitizar input em `avaliar_resposta()`
- [ ] Expandir dataset para 50+ chunks (web scraping)

### Médio Prazo (Priority 2)
- [ ] **Tool Calling decidido por LLM** (passar schemas ao Gemma)
- [ ] Implementar **Vector Database** (Pinecone, Weaviate)
- [ ] Adicionar **Testes Unitários** (Vitest, Jest)
- [ ] Criar **Backend API** (Express/FastAPI) para operações intensivas
- [ ] Integrar **PostgreSQL** para persistência (agenda, tarefas, resultados)

### Longo Prazo (Priority 3)
- [ ] Mobile app (React Native)
- [ ] Suporte a **streaming** (respostas em tempo real)
- [ ] **Fine-tuning** do Gemma com dados acadêmicos
- [ ] Análise de **learning paths** personalizados
- [ ] **Integração com LMS** (Canvas, Moodle)
- [ ] Geração automática de **resumos PDF**

---

## 📊 Estatísticas e Métricas

### Performance Esperada
| Métrica | Valor |
|---------|-------|
| Tempo de resposta RAG | 50-200ms |
| Latência Gemma API | 1-3s |
| Uso de memória (app) | ~5MB |
| Tamanho do arquivo HTML | ~80KB |

### Cobertura de Conteúdo
- ✅ **IA Geral**: 20% (fundamentos, história)
- ✅ **Árvores de Decisão**: 32% (TDIDT, entropia, poda)
- ✅ **Aprendizado de Máquina**: 24% (supervisionado, validação, métricas)
- ✅ **Embeddings e RAG**: 12% (vetores, busca semântica)
- ✅ **Avaliação**: 12% (testes, explicabilidade)

### Questões de Teste
- **Total**: 10 questões
- **Tipos**: 40% conceitual, 60% técnico
- **Cobertura**: Todos os tópicos principais
- **Feedback**: Automático com palavras-chave esperadas

---

## 📞 Suporte e Créditos

**Desenvolvido para**: Trabalho Prático de Inteligência Artificial  
**Professor**: [Seu Professor]  
**Disciplina**: Inteligência Artificial  
**Instituição**: UFMS  

**Tecnologias**:
- 🤖 Gemma 3 12B (Google)
- 🔍 TF-IDF + Keywords (RAG)
- 💾 LocalStorage (persistência frontend)
- 🎨 Tabler Icons (UI)

**Licença**: MIT (para fins educacionais)

---

**Última atualização**: 2026-05-16  
**Status**: ✅ Production-ready para MVP  
**Próximo release**: v1.1 (embeddings reais + backend)
