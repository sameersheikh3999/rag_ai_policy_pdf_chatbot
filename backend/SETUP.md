# Backend Setup Instructions

## Quick Start

### 1. Get Your Groq API Key
Visit https://console.groq.com/ and create a free API key.

### 2. Add API Key to `.env` File
Edit the `.env` file in the backend directory:
```
GROQ_API_KEY=your_actual_api_key_from_groq
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Test Your Setup
```bash
python test_setup.py
```

This will verify:
- ✓ GROQ_API_KEY is set
- ✓ All Python packages are installed
- ✓ Groq API connection works
- ✓ FAISS index is available
- ✓ RAG Pipeline initializes

### 5. Start the Backend Server
```bash
python -m uvicorn main:app --host 127.0.0.1 --port 8001
```

## Using the API

**Health Check:**
```bash
curl http://127.0.0.1:8001/health
```

**Ask a Question:**
```bash
curl -X POST http://127.0.0.1:8001/chat \
  -H "Content-Type: application/json" \
  -d '{"question": "What are education policies?", "include_web_search": false}'
```

**Evaluate a Policy:**
```bash
curl -X POST http://127.0.0.1:8001/evaluate-policy \
  -H "Content-Type: application/json" \
  -d '{"policy_text": "Implement digital education with teacher training"}'
```

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/health` | GET | Health check - verify server is running |
| `/chat` | POST | Answer policy questions with RAG |
| `/evaluate-policy` | POST | Evaluate a policy proposal |
| `/ingest` | POST | Rebuild FAISS index from PDFs |
| `/documents` | GET | List all indexed documents |

## Troubleshooting

| Issue | Solution |
|-------|----------|
| "Invalid API Key" | Get a key from https://console.groq.com/ and add to `.env` |
| "GROQ_API_KEY not set" | Add `GROQ_API_KEY=your_key` to `.env` file |
| "Port 8001 already in use" | Use different port: `--port 8002` |
| "FAISS index not loaded" | Run `python ingest.py` first |

## Configuration

The backend uses environment variables from `.env` file:
- `GROQ_API_KEY` - Your Groq API key (required)
