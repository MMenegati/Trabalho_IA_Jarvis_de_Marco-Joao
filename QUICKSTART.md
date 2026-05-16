# 🚀 JARVIS Acadêmico - Quick Start (30 segundos)

## 1️⃣ Abrir a Aplicação
```bash
# Opção 1: Clicar em jarvis_academico.html no Windows Explorer
# Opção 2: Arrastar para o browser
# Opção 3: Browser → File → Open → jarvis_academico.html
```

## 2️⃣ Testar Imediatamente (5 comandos)

### Teste 1: Verificar Gemma API Conectado
```
Chat: "Olá JARVIS"
Esperado: Resposta do Gemma em 1-3 segundos
```

### Teste 2: RAG (Busca de Materiais)
```
Chat: "Explique entropia em árvores"
Esperado: [buscar_material_rag] → 3 chunks recuperados → Resposta inteligente
Painel: Materiais RAG (com chunks numerados)
```

### Teste 3: Ferramentas (Tool Calling)
```
Chat: "O que tenho hoje?"
Esperado: [consultar_agenda] → Lista de eventos
Painel: Logs (rastreamento da chamada)
```

### Teste 4: Avaliação
```
Chat: "Questão 1"
Esperado: Pergunta: "O que é Teste de Turing?"

Chat: "Um teste para avaliar inteligência de máquinas"
Esperado: Status: CORRETA + Feedback positivo
```

### Teste 5: Sistema Integrado
```
Chat: "Monte um plano de estudos para amanhã"
Esperado: 
  - [consultar_agenda(amanhã)]
  - [listar_tarefas(pendentes)]
  - Resposta com plano personalizado
```

---

## 3️⃣ Visualizar Todos os Painéis

**Sidebar esquerdo:**
- 🗨️ **Chat** (atual) - Conversa com JARVIS
- 📅 **Agenda** - Eventos acadêmicos
- ✅ **Tarefas** - To-do list com prioridades
- 📚 **Materiais RAG** - Base de conhecimento (25 chunks)
- 🔍 **Logs** - Histórico de ferramentas chamadas

---

## 4️⃣ Validação Automática

```bash
# Abrir test_validation.html para checklist automático
# Vai mostrar: ✅/❌ para cada funcionalidade
```

---

## 5️⃣ Testes Avançados (Opcional)

### Teste de Limite: Muitas Ferramentas Simultâneas
```
Chat: "Quais tarefas pendentes tenho? Qual minha agenda esta semana? 
       Gere um exercício sobre árvores de decisão"
Esperado: 3 ferramentas executadas em paralelo
```

### Teste de Busca Semântica Falhando
```
Chat: "O que é SVM?"
Esperado: "Nenhum trecho relevante encontrado nos materiais"
(SVM não está na base - esperado)
```

### Teste de Avaliação Parcial
```
Chat: "Questão 2"
Esperado: Pergunta sobre entropia vs ganho

Chat: "Entropia é bagunça, ganho é redução"
Esperado: Status: PARCIAL + "Faltaram conceitos: informação, particao"
```

---

## 📁 Estrutura de Arquivos

```
c:\Users\joaoa\OneDrive\Documentos\IA\
├── jarvis_academico.html          ← 🎯 ABRIR ESTE
├── README.md                       ← Documentação completa
├── dataset_metadata.json           ← Metadados do dataset
├── test_validation.html            ← Validação automática
├── INSTRUCOES_ENTREGA.md          ← Como entregar
├── RESUMO_IMPLEMENTACOES.md       ← Mudanças feitas
└── QUICKSTART.md                  ← Este arquivo
```

---

## ⚡ Atalhos Úteis no Chat

| Botão | Ação |
|-------|------|
| 📅 Agenda hoje | Mostra eventos de hoje |
| ✅ Tarefas | Lista tarefas pendentes |
| 📚 Material RAG | Busca na base de conhecimento |
| 🧠 Plano de estudos | Monta plano para amanhã |
| ❓ Active recall | Gera questões de revisão |

---

## 🔍 Debug: Se Algo Não Funcionar

### Problema: "Erro ao conectar com o modelo"
```
✅ Solução 1: Verificar internet
✅ Solução 2: Verificar se acesso a https://llm.liaufms.org está bloqueado
✅ Solução 3: Abrir DevTools (F12) → Console → ver error exato
✅ Solução 4: Trocar modelo (veja "Configuração" em README.md)
```

### Problema: RAG não retorna resultados
```
✅ Verificar: A query usa palavras-chave que existem
✅ Exemplo funciona: "Explique entropia" (keywords na base)
✅ Exemplo falha: "O que é SVM" (SVM não no dataset)
```

### Problema: Tarefa não salva ao recarregar
```
✅ Esperado: Dados salvos em localStorage (refreshar mantém)
✅ Se perder: Browser limpou cache (abra novamente)
✅ Futuro: Usar banco de dados persistente
```

---

## 📊 Checklist Rápido (Antes de Entregar)

- [ ] Gemma API respondendo (testar com "Olá")
- [ ] RAG recuperando 3+ chunks para buscas
- [ ] 10 questões (1-10) respondendo corretamente
- [ ] Avaliação dando feedback (correta/parcial/incorreta)
- [ ] Logs rastreando ferramentas
- [ ] Todos os 5 painéis navegáveis
- [ ] README.md com 15+ seções
- [ ] Sem erros no console (F12)

---

## ⏱️ Tempo de Testes Recomendado

| Teste | Tempo | Total |
|-------|-------|-------|
| Verificar API | 30s | 30s |
| Testar RAG | 30s | 1m |
| Testar Tools | 1m | 2m |
| Testar Avaliação | 1m | 3m |
| Revisar Documentação | 2m | 5m |
| Gravar Vídeo (3min) | 10m | 15m |
| **TOTAL RECOMENDADO** | - | **~20 min** |

---

## 🎯 Performance Esperada

| Operação | Tempo | Nota |
|----------|-------|------|
| Gemma resposta | 1-3s | Dependente da latência UFMS |
| RAG busca | <100ms | Local no browser |
| UI renderização | <100ms | Animações suaves |
| Tool execution | <50ms | Local, muito rápido |

**Se mais lento**: Pode ser latência de rede (normal em Wi-Fi público)

---

## 📱 Browsers Testados

✅ Chrome 90+  
✅ Firefox 88+  
✅ Edge 90+  
✅ Safari 14+ (não testado, deverá funcionar)  
❌ IE 11 (não suporta ES6)

---

## 🎓 Material Recomendado para Ler (Antes de Defender)

1. **README.md** (5 min)
   - Seção: "Funcionalidades" e "Sistema de Avaliação"

2. **Análise de Erros** (10 min)
   - README.md seção "Análise de Erros"
   - Entender 6 erros + soluções

3. **Dataset** (5 min)
   - dataset_metadata.json
   - Visão geral de origem + limitações

4. **Código-chave** (5 min)
   - `ragRetrieve()` - Como busca funciona
   - `avaliar_resposta()` - Como avaliação funciona
   - `callLLM()` - Como integração com Gemma funciona

---

## 💡 Dicas Profissionais

1. **Ao apresentar**: Mostre primeiro RAG funcionando (é o core)
2. **Se algo quebrar na live**: Use botões quick-actions (mais confiável)
3. **Fale sobre**: Arquitetura, não apenas "cliquei aqui"
4. **Aponte**: 6 erros identificados + como seriam soluções
5. **Demonstre**: Avaliação automática (é diferencial)

---

## 📞 Precisa de Ajuda?

1. **Erro técnico?** → Leia README.md seção FAQ
2. **Como implementou X?** → Veja RESUMO_IMPLEMENTACOES.md
3. **Como entregar?** → INSTRUCOES_ENTREGA.md
4. **Como usar?** → README.md seção "Como Usar"
5. **Por que fez assim?** → Comentários no HTML + README

---

**Tempo esperado**: 30 seg para abrir + 5 min para testar tudo  
**Status**: ✅ Pronto para apresentação  
**Última atualização**: 2026-05-16
