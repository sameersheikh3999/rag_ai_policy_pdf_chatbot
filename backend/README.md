# 🐍 Backend - AI Policy Analyzer

<div align="center">

[![Python](https://img.shields.io/badge/Python-3.10+-3776ab?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![Groq API](https://img.shields.io/badge/Groq_API-LLaMA%203.3-FF6B35?style=for-the-badge)](https://console.groq.com/)
[![FAISS](https://img.shields.io/badge/FAISS-Vector%20DB-412991?style=for-the-badge&logo=meta&logoColor=white)](https://faiss.ai/)

**FastAPI backend with RAG pipeline for policy analysis and comprehensive LLM inference**

[🚀 Quick Start](#quick-start) • [🏗️ Architecture](#architecture) • [📡 API](#api-endpoints) • [🔧 Configuration](#configuration)

</div>

---

## 🚀 Quick Start

### 1. Setup Environment

```bash
# Navigate to backend directory
cd backend

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure API Key

Create a `.env` file in the backend directory:

```bash
# Option 1: Create file manually
echo 'GROQ_API_KEY=your_actual_groq_api_key_here' > .env

# Option 2: Or use a text editor and add:
# GROQ_API_KEY=your_actual_groq_api_key_here
```

Get your Groq API key from: https://console.groq.com/

### 3. Start Server

```bash
python -m uvicorn main:app --host 127.0.0.1 --port 8001 --reload
```

The server will start at: **http://127.0.0.1:8001**

### 4. Verify Installation

```bash
# Test health endpoint
curl http://127.0.0.1:8001/health

# Should return:
# {"status":"ok","service":"AI Policy Analyzer","rag_ready":true}
```

---

## 🏗️ Architecture

### High-Level Flow

```
Request (Chat or Evaluation)
    ▼
main.py (FastAPI Routes)
    ▼
rag_pipeline.py (RAG Logic)
    ├─ Embedding (Sentence Transformers)
    ├─ FAISS Search (Vector DB)
    ├─ Web Search (DuckDuckGo)
    ├─ Prompt Building
    └─ Groq API Call (LLaMA 3.3)
    ▼
Response (Streaming or JSON)
```

### Project Structure

```
backend/
├── main.py                  # FastAPI application & routes
├── rag_pipeline.py          # Core RAG logic
├── web_search.py            # DuckDuckGo integration
├── requirements.txt         # Python dependencies
├── Procfile                 # Railway deployment
├── .env.example             # Environment template
├── .env.production          # Production environment
├── README.md                # This file
│
└── data/
    ├── pdfs/                # Policy PDF files
    └── faiss_index/         # FAISS vector database
        ├── index.faiss      # Vector index
        └── metadata.json    # Chunk metadata
```

---

## 📡 API Endpoints

### 1. Health Check

**Endpoint**: `GET /health`

Check if backend is running and RAG is ready.

```bash
curl http://127.0.0.1:8001/health
```

**Response**:
```json
{
  "status": "ok",
  "service": "AI Policy Analyzer",
  "rag_ready": true
}
```

### 2. Chat (Streaming)

**Endpoint**: `POST /chat`

Answer a policy question using RAG with optional web search.

```bash
curl -X POST http://127.0.0.1:8001/chat \
  -H "Content-Type: application/json" \
  -d '{
    "question": "What are Pakistan'\''s current education priorities?",
    "include_web_search": true
  }'
```

**Request Body**:
```json
{
  "question": "string",           // User's question
  "include_web_search": boolean   // Include web search (optional, default: true)
}
```

**Response** (Server-Sent Events / Streaming):
```
data: {"type":"content","data":"Pakistan's education"}
data: {"type":"content","data":" policy focuses"}
...
data: {"type":"sources","data":[{...}, {...}]}
```

**Python Example**:
```python
import requests

response = requests.post(
    "http://127.0.0.1:8001/chat",
    json={
        "question": "What is education policy?",
        "include_web_search": True
    },
    stream=True
)

for line in response.iter_lines():
    if line:
        print(line.decode())
```

### 3. Policy Evaluation

**Endpoint**: `POST /evaluate-policy`

Comprehensive evaluation of a submitted policy direction.

```bash
curl -X POST http://127.0.0.1:8001/evaluate-policy \
  -H "Content-Type: application/json" \
  -d '{
    "policy_text": "Implement universal basic education with digital literacy focus"
  }'
```

**Request Body**:
```json
{
  "policy_text": "string"  // User'\''s policy proposal or direction
}
```

**Response**:
```json
{
  "evaluation": "## Comparative Analysis\n\nYour policy proposal...",
  "sources": [
    {
      "type": "pdf",
      "metadata": {
        "filename": "NEP_Pakistan.pdf",
        "page": 5
      },
      "text": "..."
    },
    {
      "type": "web",
      "title": "Global Best Practices in Education",
      "url": "https://example.com",
      "snippet": "..."
    }
  ]
}
```

**Evaluation Sections**:
1. **Comparative Analysis** - How it compares to Pakistan policies and global examples
2. **Alignment Assessment** - Scores (1-10) for alignment with both global and Pakistan context
3. **Policy Standardization** - Recommended structure based on proven frameworks
4. **Strengths & Gaps** - Detailed analysis of strengths and areas for improvement
5. **Implementation Roadmap** - Phased implementation plan (Phase 1, 2, 3)

---

## 🔧 Configuration

### Environment Variables

Create a `.env` file with:

```bash
# Required
GROQ_API_KEY=gsk_your_actual_key_here

# Optional (defaults shown)
# LLM_MODEL=llama-3.3-70b-versatile
# FAISS_INDEX_PATH=data/faiss_index
```

### Python Dependencies

See `requirements.txt` for all dependencies:

```
fastapi==0.109.0
uvicorn==0.27.0
groq==0.4.2
python-dotenv==1.0.0
faiss-cpu==1.7.4
sentence-transformers==2.2.2
PyMuPDF==1.23.8
duckduckgo-search==3.9.10
pydantic==2.5.0
python-multipart==0.0.6
requests==2.31.0
```

### Install Specific Version

```bash
# If you need specific versions
pip install -r requirements.txt --upgrade
```

---

## 📊 RAG Pipeline Details

### 1. Embedding & Search

**Embedding Model**: `all-MiniLM-L6-v2` (Sentence Transformers)
- 384-dimensional embeddings
- Lightweight (~50MB)
- Optimized for semantic similarity

**Vector Database**: FAISS (IndexFlatL2)
- Fast similarity search
- Stores embeddings locally
- No cloud dependency

**Search Process**:
```python
1. Embed user question → 384-dim vector
2. Query FAISS index → Top K results
3. Retrieve chunks from metadata.json
4. Sort by relevance score
5. Return top 5 chunks
```

### 2. Web Search

**Provider**: DuckDuckGo (free, no API key needed)

**Search Results**:
- Returns title, URL, and snippet
- Formatted as context for LLM
- Includes in sources for citations

### 3. LLM Inference

**Model**: LLaMA 3.3 70B (Groq API)
- Fast inference (~2-5 seconds)
- 70 billion parameters
- State-of-the-art quality

**Streaming**:
```python
stream = client.chat.completions.create(
    model="llama-3.3-70b-versatile",
    messages=[...],
    stream=True,  # Enable streaming
    temperature=0.7,
    max_tokens=2000
)

for chunk in stream:
    if chunk.choices[0].delta.content:
        yield chunk.choices[0].delta.content
```

---

## 📂 Data Structure

### FAISS Index Format

```
backend/data/faiss_index/
├── index.faiss          # Binary FAISS index file
└── metadata.json        # Chunk metadata
```

**metadata.json Structure**:
```json
{
  "chunks": [
    {
      "id": 0,
      "text": "The education policy emphasizes...",
      "metadata": {
        "filename": "NEP_Pakistan.pdf",
        "page": 5,
        "chunk_index": 0
      }
    },
    ...
  ]
}
```

### PDF Processing

**Extraction**: PyMuPDF (fitz)
- Extracts text from each PDF page
- Preserves structure and formatting
- ~500 PDFs processed: ~2-5 minutes

**Chunking**:
- Chunk size: ~800 tokens
- Overlap: ~100 tokens
- Prevents losing context at chunk boundaries

**Indexing**:
- Embed each chunk
- Add to FAISS
- Store metadata

---

## 🔐 Security & Best Practices

### API Key Management

```python
# ✅ Correct - Load from environment
from dotenv import load_dotenv
load_dotenv(override=True)  # Must be at TOP of file
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# ❌ Incorrect - Hardcoded key
GROQ_API_KEY = "gsk_..."  # Never do this!
```

### CORS Configuration

```python
# Allow specific origins in production
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://yourdomain.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Input Validation

```python
# Using Pydantic models
from pydantic import BaseModel

class ChatRequest(BaseModel):
    question: str  # Required, non-empty
    include_web_search: bool = True  # Optional, defaults to True
```

---

## 🐛 Troubleshooting

### Issue: `Invalid API Key` (401 Error)

**Symptoms**:
```
Error code: 401 - Authentication failed
```

**Solutions**:
1. Verify API key at https://console.groq.com/
2. Check `.env` file has correct key: `GROQ_API_KEY=gsk_...`
3. Ensure no extra spaces: `GROQ_API_KEY= gsk_...` ❌
4. Restart server after updating `.env`

### Issue: `Cannot find FAISS index`

**Symptoms**:
```
FileNotFoundError: data/faiss_index/index.faiss not found
```

**Solutions**:
1. Ensure PDFs are in `backend/data/pdfs/`
2. Run index builder (if provided)
3. FAISS index builds automatically on first run
4. Check permissions on `data/` directory

### Issue: Slow Responses

**Symptoms**:
- First request takes 30+ seconds
- Subsequent requests are fast

**Explanation**:
- This is normal! LLaMA model loads on first request (~30s)
- Subsequent requests reuse loaded model (~2-5s)

**Solutions**:
- Use a dedicated GPU for faster processing
- Increase Groq API timeout if needed
- Monitor API usage in Groq dashboard

### Issue: Out of Memory

**Symptoms**:
```
MemoryError: Unable to allocate memory
```

**Solutions**:
1. Ensure 2GB+ RAM available
2. Check for memory leaks in logs
3. Reduce PDF processing batch size
4. Monitor with `top` or Task Manager

---

## 🚀 Performance Optimization

### Caching

```python
from functools import lru_cache

@lru_cache(maxsize=100)
def embed_query(question: str):
    # Cache embeddings for repeated questions
    return model.encode(question)
```

### Batch Processing

```python
# Process multiple PDFs in parallel
from concurrent.futures import ThreadPoolExecutor

with ThreadPoolExecutor(max_workers=4) as executor:
    results = list(executor.map(process_pdf, pdf_files))
```

### Connection Pooling

```python
# Reuse HTTP connections
session = requests.Session()
response = session.get(url)
```

---

## 📈 Monitoring & Logging

### Enable Logging

```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)
logger.info("Processing request...")
```

### Monitor Groq API Usage

Check your dashboard at: https://console.groq.com/account/usage

---

## 🔌 Integration Example

### Python Client

```python
import requests
import json

BASE_URL = "http://127.0.0.1:8001"

# Chat endpoint
response = requests.post(
    f"{BASE_URL}/chat",
    json={
        "question": "What is education policy?",
        "include_web_search": True
    },
    stream=True
)

for line in response.iter_lines():
    if line:
        data = json.loads(line.decode())
        if data['type'] == 'content':
            print(data['data'], end='', flush=True)
        elif data['type'] == 'sources':
            print("\n\nSources:", data['data'])
```

### JavaScript/Node.js

```javascript
const response = await fetch('http://127.0.0.1:8001/chat', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
        question: 'What is education policy?',
        include_web_search: true
    })
});

const reader = response.body.getReader();
const decoder = new TextDecoder();

while (true) {
    const { done, value } = await reader.read();
    if (done) break;
    
    const chunk = decoder.decode(value);
    const lines = chunk.split('\n');
    
    for (const line of lines) {
        if (line.trim()) {
            const data = JSON.parse(line);
            console.log(data);
        }
    }
}
```

---

## 📚 Additional Resources

- **FastAPI Docs**: https://fastapi.tiangolo.com/
- **Groq API Docs**: https://console.groq.com/docs
- **FAISS Docs**: https://faiss.ai/
- **Sentence Transformers**: https://www.sbert.net/

---

## 🤝 Contributing

When contributing to the backend:

1. Follow PEP 8 style guide
2. Add docstrings to functions
3. Test with sample queries
4. Update this README if adding endpoints
5. Check API compatibility with frontend

---

## 📝 License

This backend is part of the AI Policy Analyzer project, licensed under MIT.

---

<div align="center">

**Built with ❤️ for policy analysis**

Need help? Check the main [README](../README.md) or [Deployment Guide](../DEPLOYMENT.md)

</div>
