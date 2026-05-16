const express = require('express');
const cors = require('cors');
const app = express();

app.use(cors());
app.use(express.json());

const GEMMA_API_URL = 'https://llm.liaufms.org/v1/gemma-3-12b-it/chat/completions';
const API_KEY = 'Cxt2ftLF7d3mHS2JdiFqB-eSDAQeZvFATPXPs02lV9A';

// Proxy endpoint
app.post('/api/chat', async (req, res) => {
  try {
    console.log('[PROXY] Requisição recebida:', {
      modelo: req.body.model,
      mensagens: req.body.messages?.length,
      timestamp: new Date().toISOString()
    });

    const response = await fetch(GEMMA_API_URL, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${API_KEY}`
      },
      body: JSON.stringify(req.body)
    });

    if (!response.ok) {
      const errorText = await response.text();
      console.error('[PROXY] Erro da API:', {
        status: response.status,
        statusText: response.statusText,
        body: errorText.substring(0, 200)
      });
      return res.status(response.status).json({
        error: `API Error ${response.status}`,
        details: errorText
      });
    }

    const data = await response.json();
    console.log('[PROXY] Sucesso:', {
      status: response.status,
      choices: data.choices?.length
    });
    
    res.json(data);
  } catch (error) {
    console.error('[PROXY] Erro de conexão:', error.message);
    res.status(500).json({
      error: 'Proxy error',
      message: error.message
    });
  }
});

// Health check
app.get('/api/health', (req, res) => {
  res.json({ status: 'ok', timestamp: new Date().toISOString() });
});

const PORT = 3000;
app.listen(PORT, () => {
  console.log(`\n✅ JARVIS Proxy rodando em http://localhost:${PORT}`);
  console.log(`📡 Encaminhando requisições para: ${GEMMA_API_URL}`);
  console.log(`🔗 Use: http://localhost:${PORT}/api/chat\n`);
});
