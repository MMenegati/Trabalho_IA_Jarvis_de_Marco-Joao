# JARVIS Acadêmico

Assistente inteligente para estudantes de Ciência da Computação, desenvolvido como trabalho prático da disciplina de Inteligência Artificial — UFMS.

**Dupla**: Marco Menegati · João Antonow 
**Modelo**: Gemma 3 12B-IT (`google/gemma-3-12b-it`)  
**Arquitetura**: RAG + Tool Calling (LLM-driven) + FastAPI + SQLite

---

## Índice

1. [Arquitetura](#arquitetura)
2. [Funcionalidades implementadas](#funcionalidades-implementadas)
3. [Como instalar e rodar](#como-instalar-e-rodar)
4. [Como usar o sistema](#como-usar-o-sistema)
5. [Dataset](#dataset)
6. [Tool Calling](#tool-calling)
7. [Avaliação do sistema](#avaliação-do-sistema)
8. [Análise de erros](#análise-de-erros)
9. [Melhorias de aprendizado](#melhorias-de-aprendizado)
10. [Engenharia de software](#engenharia-de-software)
11. [IAs utilizadas no desenvolvimento](#ias-utilizadas-no-desenvolvimento)

---

## Arquitetura

```
jarvis/
├── backend/
│   ├── main.py              ← FastAPI: rotas REST + serve frontend
│   ├── config.py            ← API key, model, constantes
│   ├── rag/
│   │   ├── loader.py        ← lê arquivos de data/raw/
│   │   ├── chunker.py       ← sliding window (200 palavras, overlap 50)
│   │   ├── embedder.py      ← BERT (sentence-transformers) ou TF-IDF
│   │   ├── retriever.py     ← cosine similarity, top-k
│   │   └── pipeline.py      ← orquestra load→chunk→embed→retrieve
│   ├── tools/
│   │   ├── definitions.py   ← schemas JSON das 7 ferramentas (enviados à LLM)
│   │   ├── agenda.py        ← consultar_agenda
│   │   ├── tasks.py         ← listar/adicionar/concluir tarefas
│   │   ├── rag_tool.py      ← buscar_material_rag
│   │   ├── learning.py      ← gerar_exercicio, planejar_estudos
│   │   └── executor.py      ← recebe decisão da LLM, executa, loga
│   ├── llm/
│   │   ├── client.py        ← ciclo completo: decisão → execução → resposta
│   │   └── prompts.py       ← system prompt + prompt de roteamento de tools
│   ├── storage/
│   │   ├── database.py      ← cria tabelas SQLite + seed inicial
│   │   ├── agenda_repo.py   ← CRUD de eventos
│   │   └── tasks_repo.py    ← CRUD de tarefas
│   └── evaluation/
│       ├── questions.py     ← 10 perguntas com keywords esperadas
│       └── scorer.py        ← classifica correta/parcial/incorreta + recupera docs
├── frontend/
│   ├── index.html           ← estrutura HTML
│   ├── css/style.css        ← estilos (tema escuro)
│   └── js/
│       ├── api.js           ← todas as chamadas fetch ao backend
│       ├── app.js           ← estado global + inicialização
│       ├── chat.js          ← painel de chat
│       ├── agenda.js        ← painel de agenda
│       └── tasks.js         ← painel de tarefas
├── data/
│   ├── raw/                 ← 10 documentos acadêmicos (.txt)
│   └── metadata.json        ← origem, tipo, limitações e chunking de cada doc
├── storage/
│   └── jarvis.db            ← SQLite (gerado automaticamente)
├── tests/
│   ├── test_rag.py
│   ├── test_tools.py
│   └── test_evaluation.py
└── requirements.txt
```

### Fluxo de uma mensagem no chat

```
Usuário digita mensagem
        │
        ▼
[1ª chamada LLM] — Gemma recebe mensagem + schemas das 7 ferramentas
        │          e decide quais chamar (resposta em JSON)
        ▼
executor.py executa as ferramentas escolhidas pela LLM
        │          e registra logs (ferramenta, args, resultado)
        ▼
[2ª chamada LLM] — Gemma recebe os resultados das ferramentas
        │          e gera a resposta final em linguagem natural
        ▼
Frontend exibe resposta + atualiza painel de Logs
```

---

## Funcionalidades implementadas

### 3.1 Consulta a materiais de estudo (RAG)

Pipeline completo implementado em `backend/rag/`:

- **Carregamento**: `loader.py` lê arquivos `.txt` e `.pdf` de `data/raw/`
- **Chunking**: `chunker.py` usa sliding window com 200 palavras e overlap de 50
- **Embeddings**: `embedder.py` tenta BERT (`all-MiniLM-L6-v2`); fallback automático para TF-IDF se torch falhar
- **Recuperação**: `retriever.py` usa cosine similarity com `sklearn`
- **Cache**: o índice é salvo em `data/chunks.json` após a primeira build

Exemplos de uso no chat:
```
"Explique entropia em árvores de decisão"
"Resuma o material sobre embeddings"
"Quais são as vantagens das redes neurais?"
```

### 3.2 Agenda acadêmica

Armazenada em SQLite (`storage/jarvis.db`). Persiste entre reinicializações.

- 10 eventos pré-cadastrados (aulas, provas, trabalhos)
- Consultas por período: `hoje`, `amanha`, `semana`
- Painel visual com filtros

Exemplos de uso no chat:
```
"O que tenho hoje?"
"Tenho prova amanhã?"
"Quais são minhas aulas esta semana?"
```

### 3.3 Lista de tarefas

Também persistida em SQLite.

- Adicionar tarefa com prioridade (alta / média / baixa)
- Listar pendentes ou concluídas
- Marcar como concluída pelo ID
- Painel visual com formulário de adição

Exemplos de uso no chat:
```
"Adiciona tarefa: estudar redes neurais, prioridade alta"
"Liste minhas tarefas pendentes"
"Conclui a tarefa 3"
```

### 3.4 Planejamento de estudos

Ferramenta `planejar_estudos(foco)` em `backend/tools/learning.py`:

- Consulta agenda da semana
- Lista tarefas pendentes
- Busca materiais relevantes no RAG pelo foco informado
- Gera plano consolidado

Exemplos de uso no chat:
```
"Monte um plano de estudos para a prova de IA"
"O que devo priorizar hoje?"
"Me ajude a organizar a semana"
```

---

## Como instalar e rodar

### Pré-requisitos

- Python 3.11 ou 3.12
- Acesso à rede da UFMS (ou VPN) para `llm.liaufms.org`

### Passo 1 — instalar dependências

```powershell
pip install -r requirements.txt
```

Se quiser o torch CPU-only (evita problemas de DLL no Windows):

```powershell
pip install torch --index-url https://download.pytorch.org/whl/cpu
```

> O sistema funciona sem torch usando TF-IDF como fallback para embeddings.

### Passo 2 — iniciar o servidor

```powershell
python -m uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```

### Passo 3 — acessar o sistema

Abra no browser:

```
http://localhost:8000
```

Na **primeira execução**, o servidor vai:
1. Criar o banco SQLite em `storage/jarvis.db` com agenda e tarefas de exemplo
2. Carregar os 10 documentos de `data/raw/`, gerar chunks e embeddings
3. Salvar o índice em `data/chunks.json` (execuções seguintes carregam o cache)

### Rodar os testes

```powershell
python tests/test_rag.py
python tests/test_tools.py
python tests/test_evaluation.py
```

Ou com pytest:

```powershell
python -m pytest tests/ -v
```

---

## Como usar o sistema

A interface tem 4 painéis acessíveis pela barra lateral:

| Painel | Função |
|--------|--------|
| **Chat** | Conversa com JARVIS — aciona ferramentas automaticamente via LLM |
| **Agenda** | Visualiza eventos por período (hoje / amanhã / semana) |
| **Tarefas** | Adiciona, filtra e conclui tarefas |
| **Logs** | Registro de cada ferramenta acionada pela LLM |

### Exemplos práticos

**Consultar agenda:**
```
"O que tenho hoje?"
"Tenho prova esta semana?"
```

**Buscar material:**
```
"Explique o algoritmo TDIDT"
"O que é bias-variance tradeoff?"
"Como funciona o RAG?"
```

**Gerenciar tarefas:**
```
"Adiciona tarefa: revisar capítulo 3, prioridade alta"
"Quais tarefas tenho pendentes?"
"Conclui a tarefa 2"
```

**Plano de estudos:**
```
"Monte um plano para a prova de IA de amanhã"
"O que devo estudar hoje?"
```

**Exercícios e avaliação:**
```
"Me faça um exercício sobre árvores de decisão"
"Quero praticar embeddings"
"Me avalie sobre o conteúdo de IA"
```

---

## Dataset

Pasta: `data/raw/` — 10 documentos em formato `.txt`

| Arquivo | Tópico | Fontes principais |
|---------|--------|-------------------|
| `01_ia_fundamentos.txt` | IA — Fundamentos e história | Wikipedia, Russel & Norvig, MIT OCW |
| `02_arvores_decisao.txt` | Árvores de Decisão (TDIDT) | Quinlan C4.5, Breiman CART, Shannon |
| `03_aprendizado_maquina.txt` | Aprendizado de Máquina | Goodfellow, Andrew Ng, Tom Mitchell |
| `04_embeddings_rag.txt` | Embeddings e RAG | Sentence-BERT, Lewis et al (RAG paper) |
| `05_redes_neurais.txt` | Redes Neurais e Deep Learning | LeCun, Vaswani (Transformer) |
| `06_processamento_linguagem_natural.txt` | PLN | Jurafsky & Martin, Devlin (BERT) |
| `07_algoritmos_busca.txt` | Busca e Otimização | Russel & Norvig, Hart (A*) |
| `08_avaliacao_sistemas_ia.txt` | Avaliação e Explicabilidade | NIST, LIME, SHAP |
| `09_visao_computacional.txt` | Visão Computacional | LeCun, He (ResNet), Redmon (YOLO) |
| `10_etica_ia.txt` | Ética em IA | Floridi et al, Jobin et al |

**Estratégia de chunking:** sliding window com 200 palavras e overlap de 50 palavras (`backend/rag/chunker.py`). O overlap preserva contexto entre chunks adjacentes — sem ele, conceitos que atravessam a fronteira entre chunks seriam cortados. 200 palavras equilibra granularidade (precisão na recuperação) e conteúdo suficiente para a LLM gerar uma resposta completa.

**Limitações:** cobertura focada em tópicos da disciplina; temas como SVM, K-Means e Naive Bayes estão presentes mas com menos profundidade.

Metadados completos: [`data/metadata.json`](data/metadata.json)

---

## Tool Calling

7 ferramentas implementadas em `backend/tools/`:

| Ferramenta | Descrição |
|------------|-----------|
| `consultar_agenda` | Eventos de hoje, amanhã ou da semana |
| `listar_tarefas` | Pendentes ou concluídas |
| `adicionar_tarefa` | Adiciona tarefa com prioridade |
| `concluir_tarefa` | Marca tarefa como concluída pelo ID |
| `buscar_material_rag` | Busca semântica nos documentos |
| `gerar_exercicio` | Gera exercício sobre um tópico |
| `planejar_estudos` | Plano combinando agenda + tarefas + RAG |

### Como a LLM decide

Os schemas JSON das ferramentas são enviados à Gemma em cada mensagem (`backend/tools/definitions.py`). A LLM responde com um JSON indicando quais ferramentas chamar e com quais argumentos. O `executor.py` executa as ferramentas escolhidas e registra o log.

```
1ª chamada: "Gemma, dado o prompt do usuário e estas 7 ferramentas, quais você quer chamar?"
Gemma responde: {"tools": [{"name": "consultar_agenda", "args": {"periodo": "hoje"}}]}

executor.py executa consultar_agenda("hoje") → resultado do banco SQLite

2ª chamada: "Gemma, aqui estão os resultados. Gere uma resposta natural."
```

> O servidor `llm.liaufms.org` não tem `--enable-auto-tool-choice` habilitado, portanto a decisão de ferramentas é feita via prompt estruturado em vez do protocolo nativo do OpenAI. A LLM ainda decide — o protocolo de comunicação é diferente.

**Logs:** cada chamada registra ferramenta, argumentos, resultado e timestamp em `backend/tools/executor.py`. Visíveis no painel **Logs** da interface.

---

## Avaliação do sistema

10 perguntas em `backend/evaluation/questions.py`, cobrindo os tópicos do dataset:

| # | Pergunta | Tipo | Tópico |
|---|----------|------|--------|
| 1 | O que é o Teste de Turing? | Conceitual | IA Fundamentos |
| 2 | Explique a Entropia de Shannon em árvores de decisão | Técnico | Árvores |
| 3 | Diferença entre pré-poda e pós-poda | Conceitual | Árvores |
| 4 | O que é overfitting e o trade-off bias-variance? | Conceitual | ML |
| 5 | O que são embeddings e como a similaridade cosseno é usada no RAG? | Técnico | RAG |
| 6 | Explique Precision, Recall e F1. Quando usar F1? | Técnico | Avaliação |
| 7 | O que é o Transformer e o papel do Self-Attention? | Técnico | Redes Neurais |
| 8 | Descreva o fluxo completo de um sistema RAG | Técnico | RAG |
| 9 | O que é viés algorítmico? Cite um exemplo real | Conceitual | Ética |
| 10 | Explique o algoritmo A* e o que é uma heurística admissível | Técnico | Busca |

**Critério de classificação** (`backend/evaluation/scorer.py`):
- **Correta**: ≥ 70% das keywords esperadas presentes na resposta
- **Parcialmente correta**: 40–69%
- **Incorreta**: < 40%

Para cada resposta avaliada, o sistema também retorna os **3 chunks mais relevantes recuperados pelo RAG** para aquela questão.

**Como usar a avaliação no chat:**
```
"Me avalie sobre IA"
"Quero responder a questão 5"
"Me faça perguntas sobre o conteúdo"
```

---

## Análise de erros

### Erro 1 — BERT indisponível no Windows (DLL do PyTorch)

**Tipo:** ambiente / dependência  
**Causa:** o PyTorch instalado no Windows tem incompatibilidade de DLL (`c10.dll`), impedindo o carregamento do `sentence-transformers`.  
**Impacto:** embeddings BERT não funcionam; o sistema usa TF-IDF automaticamente.  
**Solução implementada:** fallback automático em `backend/rag/embedder.py` — tenta BERT, captura a exceção e ativa TF-IDF sem interromper o servidor.  
**Solução completa:** instalar a build CPU-only do PyTorch: `pip install torch --index-url https://download.pytorch.org/whl/cpu`

### Erro 2 — Tool calling nativo não suportado pelo servidor

**Tipo:** limitação de infraestrutura  
**Causa:** o servidor `llm.liaufms.org` não foi iniciado com `--enable-auto-tool-choice`, portanto rejeita requisições com `tool_choice="auto"` com erro 400.  
**Impacto:** não é possível usar o protocolo nativo OpenAI de function calling.  
**Solução implementada:** a decisão de ferramentas é feita via prompt estruturado — a Gemma lê os schemas e responde com JSON. Quatro estratégias de extração de JSON garantem resiliência à saída malformada do modelo.

### Erro 3 — JSON malformado na resposta de decisão de ferramentas

**Tipo:** geração  
**Causa:** o Gemma 12B às vezes gera JSON com vírgulas ou aspas faltando na resposta de roteamento de ferramentas.  
**Impacto:** a ferramenta correta não é acionada e a LLM responde sem contexto adicional.  
**Solução implementada:** `_extract_tool_calls()` em `backend/llm/client.py` tenta 4 estratégias: parse direto, extração de bloco markdown, busca por `{...}` no texto, e detecção de "nenhuma ferramenta".

### Erro 4 — Cobertura limitada do dataset

**Tipo:** recuperação  
**Causa:** 10 documentos cobrem apenas parte do currículo (não há SVM, K-Means, Naive Bayes em profundidade).  
**Impacto:** perguntas sobre tópicos não cobertos retornam chunks pouco relevantes.  
**Solução:** expandir `data/raw/` com mais documentos — o pipeline carrega automaticamente qualquer `.txt` ou `.pdf` novo na pasta.

### Erro 5 — Persistência depende do servidor estar no ar

**Tipo:** arquitetura  
**Causa:** agenda e tarefas vivem em SQLite local; se o banco for apagado, os dados somem.  
**Impacto:** sem backup, dados são perdidos.  
**Solução:** adicionar endpoint de exportação JSON ou backup automático do arquivo `.db`.

---

## Melhorias de aprendizado

Implementadas em `backend/tools/learning.py`:

### 1. Geração de exercícios (gerar_exercicio)

Gera enunciados práticos com resposta esperada para 5 tópicos: árvores de decisão, embeddings, redes neurais, aprendizado de máquina e RAG. Fallback genérico para outros tópicos via busca RAG.

```
"Me faça um exercício sobre entropia"
"Quero praticar árvores de decisão"
```

### 2. Planejamento de estudos (planejar_estudos) — interativo

Combina agenda da semana + tarefas pendentes + trechos RAG relevantes para montar um plano personalizado. O usuário informa o foco e o sistema retorna um plano detalhado com eventos e materiais associados.

```
"Monte um plano de estudos para a prova de IA"
"O que devo priorizar esta semana?"
```

### 3. Active recall via avaliação

O módulo `backend/evaluation/scorer.py` permite que o usuário responda perguntas e receba feedback imediato com: status (correta/parcial/incorreta), keywords encontradas, keywords faltantes, sugestão de revisão e documentos relevantes recuperados pelo RAG.

---

## Engenharia de software

### Organização e separação de responsabilidades

Cada módulo tem uma única responsabilidade. Nenhum módulo de UI acessa a rede diretamente (tudo passa por `frontend/js/api.js`). Nenhum módulo do backend mistura lógica de domínio com acesso a banco (repositórios separados).

### Tratamento de erros

- Embedder: fallback BERT → TF-IDF sem interromper o servidor
- LLM client: retry com backoff exponencial, sem retry em erros 400
- Tool executor: captura exceções por ferramenta individualmente, sem derrubar o ciclo
- Endpoints FastAPI: retornam mensagem de erro legível com traceback no log do servidor

### Logs

- Tool calling: `backend/tools/executor.py` loga ferramenta, args, resultado e status via `logging`
- LLM: `backend/llm/client.py` loga tentativas, rate limits e erros
- RAG: `backend/rag/embedder.py` loga qual backend foi carregado
- Painel **Logs** na interface mostra histórico em tempo real

### Testes

| Arquivo | O que testa |
|---------|-------------|
| `tests/test_rag.py` | loader encontra 10+ docs, chunker gera chunks com tamanho e overlap corretos, IDs únicos |
| `tests/test_tools.py` | schemas das ferramentas têm campos obrigatórios, todas as ferramentas do schema estão no registry, CRUD de agenda e tarefas |
| `tests/test_evaluation.py` | 10 questões com campos obrigatórios, scoring correto/parcial/incorreto, docs recuperados na resposta |

---

## IAs utilizadas no desenvolvimento

| Ferramenta | Uso |
|------------|-----|
| **Claude Code (Anthropic)** | Arquitetura do sistema, implementação do backend Python, módulos RAG, tool calling, testes, debug de erros |
| **Gemma 3 12B-IT** | Modelo de linguagem em produção (respostas ao usuário, decisão de ferramentas) |

---

## Critérios de avaliação atendidos

| Critério | Peso | Status |
|----------|------|--------|
| **Funcionalidade** (3.1 RAG, 3.2 Agenda, 3.3 Tarefas, 3.4 Planejamento) | 20% | Implementado |
| **RAG** (load → chunk → embed → retrieve → generate) | 20% | Implementado com TF-IDF e tentativa BERT |
| **Tool Calling** (≥5 tools, LLM decide, logs) | 15% | 7 tools, LLM decide via JSON, logs no painel |
| **Avaliação + Análise de erros** (10 perguntas, 3+ erros) | 20% | 10 perguntas, 5 erros documentados |
| **Aprendizado** (≥2 funcionalidades, 1 interativa) | 15% | Exercícios, planejamento, active recall |
| **Engenharia** (organização, separação, testes, logs) | 10% | Módulos separados, testes unitários, logs |

**Diferencial:** interface gráfica com tema escuro, separação backend/frontend com API REST, persistência real em SQLite, fallback automático de embeddings, arquitetura modular documentada.
