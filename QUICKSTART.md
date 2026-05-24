# Quick Start Guide

## 5-Minute Setup

### Step 1: Prerequisites Check (2 min)

```bash
# Verify Python
python --version    # Should be 3.10+

# Verify Node
node --version      # Should be 18+

# Verify Ollama
ollama --version    # Should be installed

# Download LLaMA3
ollama pull llama3
```

### Step 2: Backend Setup (2 min)

```bash
cd backend

# Windows
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Step 3: Prepare PDFs (Optional - skip if not ready)

1. Download all 21 PDF files from your Google Drive folder
2. Save to: `backend/data/pdfs/`
3. Run: `python ingest.py` (takes 2-5 minutes)

### Step 4: Start Backend

```bash
# From backend directory (with venv activated)
python main.py

# You should see: Uvicorn running on http://127.0.0.1:8000
```

### Step 5: Frontend Setup (new terminal)

```bash
cd frontend
npm install
npm run dev

# Opens at http://localhost:5173
```

## You're Done! 🎉

### Test It

1. Open http://localhost:5173
2. You'll see an error about RAG pipeline (that's normal if no PDFs yet)
3. Once you add PDFs and run `python ingest.py`, you're ready to use it

## Common First Steps

### Add Your PDFs

1. Download 21 education policy PDFs from Google Drive folder
2. Save to `backend/data/pdfs/`
3. Run:
   ```bash
   cd backend
   python ingest.py  # Takes 2-5 minutes
   ```

### Test Without PDFs (Demo Mode)

Even without PDFs, you can test the web search integration:
- It will show an error about FAISS index
- This is expected - just means no local docs to search

### Verify Everything Works

```bash
# Check backend health
curl http://localhost:8000/health

# Check documents are indexed
curl http://localhost:8000/documents
```

## Troubleshooting

| Problem | Solution |
|---------|----------|
| "Backend not responding" | Make sure `python main.py` is running |
| "LLaMA3 not found" | Run `ollama pull llama3` |
| "No documents found" | Add PDFs to `backend/data/pdfs/` and run `python ingest.py` |
| "FAISS index error" | Run `python ingest.py` in backend directory |
| "Port 8000 already in use" | Change port in `main.py` or kill process on port 8000 |

## Next: Explore Features

### 💬 Chat Mode
- Ask: "What is Pakistan's education policy?"
- Enable web search for global context
- See cited sources from your documents

### 📋 Evaluate Policy
- Paste a policy proposal
- Get alignment score, gaps, recommendations
- See references from your document database

---

**That's it!** You now have a RAG-powered policy analysis chatbot running locally.
