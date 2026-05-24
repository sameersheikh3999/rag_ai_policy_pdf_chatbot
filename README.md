# 🚀 AI Policy Analyzer Tool

<div align="center">

[![Python](https://img.shields.io/badge/Python-3.10+-3776ab?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![React](https://img.shields.io/badge/React-18+-61dafb?style=for-the-badge&logo=react&logoColor=black)](https://react.dev/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![Groq API](https://img.shields.io/badge/Groq_API-LLaMA%203.3-FF6B35?style=for-the-badge&logo=cloud&logoColor=white)](https://console.groq.com/)
[![FAISS](https://img.shields.io/badge/FAISS-Vector%20DB-412991?style=for-the-badge&logo=meta&logoColor=white)](https://faiss.ai/)
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Production%20Ready-brightgreen?style=for-the-badge)](./DEPLOYMENT_CHECKLIST.md)

**An intelligent RAG-based chatbot for analyzing education policies with web search integration and comprehensive policy evaluation.**

[🎯 Features](#features) • [🏗️ Architecture](#architecture) • [⚡ Quick Start](#quick-start) • [📚 Documentation](#documentation) • [🚀 Deployment](#deployment)

</div>

---

## ✨ Features

### 🤖 **Intelligent Q&A with RAG**
- Answer questions about education policies using retrieval-augmented generation
- Powered by 21+ education policy PDFs from Pakistan and global sources
- Real-time streaming responses with natural language understanding
- Integration with Groq API (LLaMA 3.3 70B) for high-quality outputs

### 📊 **Policy Evaluation & Standardization**
- Submit your policy direction for comprehensive evaluation
- Get comparative analysis against existing policies
- Alignment scoring (1-10 scale) for both global and Pakistan context
- Standardization recommendations based on proven frameworks
- Detailed implementation roadmap with phases and milestones

### 🌐 **Web Search Integration**
- Augment answers with live internet search results
- DuckDuckGo integration for broader perspectives
- Web sources cited alongside document references
- Toggle-able web search in the UI

### 🎨 **Modern Dark-Themed UI**
- Beautiful React + Vite frontend with Tailwind CSS
- Responsive design for desktop and mobile
- Smooth animations and gradient effects
- Dark theme optimized for eye comfort
- Real-time streaming message display

### 📚 **Complete Citation System**
- Every answer includes sources (PDFs and web)
- Document name, page number, and direct links
- Transparent and auditable AI responses
- Trust through transparency

### 🔐 **Production Ready**
- Secure API key management with environment variables
- CORS enabled for cross-origin requests
- Health check endpoint for monitoring
- Comprehensive error handling
- Railway deployment ready

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                         Frontend (React + Vite)                      │
│  ┌───────────────────────────────────────────────────────────────┐  │
│  │  ChatWindow       │  PolicyEvaluator  │  SourcesPanel        │  │
│  │  (Q&A Interface)  │  (Policy Analysis)│  (Source Citations)  │  │
│  └───────────────────────────────────────────────────────────────┘  │
│                                 ▼                                      │
│                         Tailwind CSS + Dark Theme                    │
└─────────────────────────────────────────────────────────────────────┘
                                 ▼
                    ┌─────────────────────────────┐
                    │   REST API (FastAPI)         │
                    │  /chat  /evaluate-policy     │
                    └─────────────────────────────┘
                                 ▼
┌─────────────────────────────────────────────────────────────────────┐
│                      Backend (FastAPI + Python)                      │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │               RAG Pipeline (rag_pipeline.py)                │   │
│  │  ┌──────────────────────────────────────────────────────┐  │   │
│  │  │  1. Query Embedding     (Sentence Transformers)      │  │   │
│  │  │  2. Semantic Search     (FAISS Vector DB)           │  │   │
│  │  │  3. Web Search Results  (DuckDuckGo API)            │  │   │
│  │  │  4. Prompt Composition  (Context + Question)        │  │   │
│  │  │  5. LLM Generation      (Groq API / LLaMA 3.3)     │  │   │
│  │  │  6. Stream Response     (Real-time chunks)          │  │   │
│  │  └──────────────────────────────────────────────────────┘  │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                 ▼                                     │
│           ┌──────────────────────────────────────────┐             │
│           │  FAISS Index  │  Metadata JSON │ PDFs   │             │
│           │  (Embeddings) │  (Chunk Info)  │ Data   │             │
│           └──────────────────────────────────────────┘             │
└─────────────────────────────────────────────────────────────────────┘
```

---

## ⚡ Quick Start

### Prerequisites
- Python 3.10+
- Node.js 16+ & npm
- Groq API key (free at https://console.groq.com)
- Git

### 1️⃣ Clone & Setup

```bash
# Clone repository
git clone https://github.com/YOUR_USERNAME/AI_Policy_Analyzer_Tool.git
cd AI_Policy_Analyzer_Tool

# Backend setup
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

# Create .env file
echo 'GROQ_API_KEY=your_actual_groq_key_here' > .env

cd ..

# Frontend setup
cd frontend
npm install
cd ..
```

### 2️⃣ Start Services

```bash
# Terminal 1: Backend
cd backend
python -m uvicorn main:app --host 127.0.0.1 --port 8001

# Terminal 2: Frontend
cd frontend
npm run dev
```

### 3️⃣ Access Dashboard

Open your browser: **http://localhost:5173**

- 💬 **Chat Tab**: Ask questions about education policies
- 📋 **Evaluator Tab**: Submit policies for comprehensive analysis
- 🌐 **Web Search**: Toggle to include internet search results

### 4️⃣ Test It Out

**Chat Example:**
> "What are Pakistan's current education priorities?"

Expected: Answer grounded in PDFs with citations

**Evaluator Example:**
```
Submit: "Implement nationwide digital literacy program with focus on 
rural areas using low-bandwidth mobile learning platforms and 
teacher training initiatives"
```

Expected: Structured evaluation with alignment scores and recommendations

---

## 📁 Project Structure

```
AI_Policy_Analyzer_Tool/
├── 📄 README.md                 ← You are here
├── 📄 DEPLOYMENT.md             ← Railway deployment guide
├── 📄 DEPLOYMENT_CHECKLIST.md   ← Pre-deployment checklist
├── 📄 .gitignore                ← Git ignore configuration
├── 📄 LICENSE                   ← MIT License
│
├── 🐍 backend/
│   ├── main.py                  ← FastAPI app & routes
│   ├── rag_pipeline.py          ← RAG core logic
│   ├── web_search.py            ← DuckDuckGo integration
│   ├── requirements.txt          ← Python dependencies
│   ├── .env.example              ← Environment template
│   ├── .env.production           ← Production env template
│   ├── Procfile                  ← Railway start command
│   ├── README.md                 ← Backend documentation
│   │
│   └── 📂 data/
│       ├── pdfs/                ← Downloaded policy PDFs
│       └── faiss_index/         ← Vector database & metadata
│
├── ⚛️ frontend/
│   ├── package.json             ← Node dependencies
│   ├── vite.config.js           ← Vite configuration
│   ├── index.html               ← HTML entry point
│   ├── .env.example              ← Environment template
│   ├── README.md                 ← Frontend documentation
│   │
│   └── 📂 src/
│       ├── App.jsx              ← Main app component
│       ├── main.jsx             ← React entry point
│       ├── index.css            ← Global styles
│       │
│       ├── 📂 components/
│       │   ├── ChatWindow.jsx   ← Q&A chat interface
│       │   ├── Message.jsx      ← Chat message bubble
│       │   ├── PolicyEvaluator.jsx ← Policy analysis
│       │   └── SourcesPanel.jsx ← Source citations
│       │
│       └── 📂 config/
│           └── api.js           ← API configuration client
```

---

## 🛠️ Technology Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| **Frontend** | React 18 | Interactive UI |
| | Vite | Build tool & dev server |
| | Tailwind CSS | Utility-first styling |
| | Axios | HTTP client |
| **Backend** | FastAPI | REST API framework |
| | Uvicorn | ASGI server |
| | Python 3.10 | Runtime environment |
| **LLM** | Groq API | Cloud LLM inference |
| | LLaMA 3.3 70B | Language model |
| **Vector Search** | FAISS | Similarity search |
| | Sentence Transformers | Embeddings (all-MiniLM-L6-v2) |
| **Document Processing** | PyMuPDF | PDF text extraction |
| **Web Search** | DuckDuckGo Search | Internet search |
| **Deployment** | Railway | Cloud hosting |

---

## 🔌 API Reference

### Base URL
- **Local**: `http://127.0.0.1:8001`
- **Production**: `https://your-railway-backend.railway.app`

### Endpoints

#### 1. Health Check
```bash
curl http://127.0.0.1:8001/health
```

**Response:**
```json
{
  "status": "ok",
  "service": "AI Policy Analyzer",
  "rag_ready": true
}
```

#### 2. Chat (Streaming)
```bash
curl -X POST http://127.0.0.1:8001/chat \
  -H "Content-Type: application/json" \
  -d '{
    "question": "What is Pakistan'\''s education policy?",
    "include_web_search": true
  }'
```

**Response** (Server-Sent Events):
```json
{"type": "content", "data": "Pakistan's education"}
{"type": "content", "data": " policy focuses on"}
...
{"type": "sources", "data": [...]}
```

#### 3. Policy Evaluation
```bash
curl -X POST http://127.0.0.1:8001/evaluate-policy \
  -H "Content-Type: application/json" \
  -d '{
    "policy_text": "Implement universal basic education with digital literacy focus"
  }'
```

**Response:**
```json
{
  "evaluation": "## Comparative Analysis\n...",
  "sources": [
    {
      "type": "pdf",
      "metadata": {"filename": "policy.pdf", "page": 5}
    }
  ]
}
```

---

## 📚 Documentation

- **[Backend README](./backend/README.md)** - Setup, architecture, and API details
- **[Frontend README](./frontend/README.md)** - Development, components, and styling
- **[Deployment Guide](./DEPLOYMENT.md)** - Railway deployment step-by-step
- **[Deployment Checklist](./DEPLOYMENT_CHECKLIST.md)** - Pre-deployment verification
- **[Groq API Docs](https://console.groq.com/docs)** - LLM API reference
- **[FastAPI Docs](https://fastapi.tiangolo.com/)** - Backend framework
- **[React Docs](https://react.dev/)** - Frontend framework

---

## 🚀 Deployment

### Quick Deploy to Railway

1. **Push to GitHub**
```bash
git init
git add .
git commit -m "Initial commit: AI Policy Analyzer"
git remote add origin https://github.com/YOUR_USERNAME/AI_Policy_Analyzer_Tool.git
git branch -M main
git push -u origin main
```

2. **Create Railway Project**
   - Go to https://railway.app
   - Click "Start a New Project"
   - Select "Deploy from GitHub"
   - Choose your repository

3. **Configure Backend**
   - Base Directory: `backend`
   - Set `GROQ_API_KEY` in Railway Variables

4. **Configure Frontend**
   - Base Directory: `frontend`
   - Build Command: `npm install && npm run build`
   - Set `VITE_API_URL=your-backend-url.railway.app`

5. **Deploy & Test**
   - Generate public URL for frontend
   - Test health endpoint
   - Share your dashboard!

📖 **Full details**: See [DEPLOYMENT.md](./DEPLOYMENT.md)

### Cost Estimate
- Railway free tier: $5/month free credits
- This setup: ~$10-20/month for moderate use

---

## 🔐 Security

### Best Practices Implemented

✅ **Environment Variables**
- API keys stored in `.env` (not committed)
- Separate `.env.production` for production
- `load_dotenv()` loads from environment

✅ **CORS Protection**
- Backend allows configurable origins
- Production can restrict to specific domains

✅ **Input Validation**
- Pydantic models validate all inputs
- Error handling for malformed requests

✅ **Secure Defaults**
- No API keys in code or logs
- `.gitignore` prevents accidental commits
- Health check doesn't expose sensitive info

### Sensitive Files in .gitignore
```
.env              # API keys
backend/data/     # PDFs, FAISS index
node_modules/     # Dependencies
venv/             # Python environment
```

---

## 📊 Performance

### Response Times
- **Cold start**: ~30 seconds (model loading)
- **Subsequent queries**: 2-5 seconds
- **Streaming display**: Real-time chunks

### Resource Requirements
- **Backend RAM**: ~2GB
- **Storage**: ~500MB (PDFs + FAISS index)
- **Frontend Build**: ~10MB

### Optimization Tips
1. Enable caching in production
2. Use CDN for frontend assets
3. Monitor Groq API usage
4. Consider pagination for large result sets

---

## 🤝 Contributing

Contributions welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Development Setup
```bash
# Install dev dependencies
pip install -r backend/requirements.txt
npm install --prefix frontend

# Run linting (if configured)
# Run tests
# Check formatting
```

---

## 🐛 Troubleshooting

### Backend Won't Start
```
Error: Invalid API Key
→ Check GROQ_API_KEY in .env
→ Verify key at https://console.groq.com/

Error: Cannot read PDFs
→ Ensure backend/data/pdfs/ contains PDF files
→ FAISS index builds automatically on first run
```

### Frontend Shows Connection Errors
```
Error: Cannot reach backend
→ Verify backend is running on port 8001
→ Check VITE_API_URL in .env
→ Check browser console (F12) for CORS errors

Error: Slow responses
→ First request takes 30s for model loading (normal)
→ Subsequent requests should be 2-5s
```

### Web Search Not Working
```
→ Check internet connection
→ Verify DuckDuckGo API availability
→ Check backend logs for errors
```

---

## 📈 Roadmap

### v1.0 ✅ (Current)
- ✅ RAG-based policy Q&A
- ✅ Web search integration
- ✅ Policy evaluation engine
- ✅ Modern UI with streaming
- ✅ Railway deployment ready

### v1.1 (Planned)
- 📌 User authentication
- 📌 Query history & bookmarks
- 📌 Custom PDF uploads
- 📌 Policy comparison tool
- 📌 Export evaluations as PDF

### v2.0 (Future)
- 🎯 Multi-language support
- 🎯 Real-time collaboration
- 🎯 Analytics dashboard
- 🎯 Custom model fine-tuning
- 🎯 Mobile app

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👏 Credits

Built with ❤️ using:
- **Groq API** for powerful LLM inference
- **FAISS** for semantic search
- **FastAPI** for modern Python APIs
- **React** for interactive UIs
- **Tailwind CSS** for beautiful styling

---

## 📧 Support

- 📖 Check [documentation](./backend/README.md)
- 🐛 Report issues on GitHub
- 💬 Questions? Create a discussion
- 🚀 Deployment help? See [DEPLOYMENT.md](./DEPLOYMENT.md)

---

<div align="center">

**Made with ❤️ for education policy analysis**

⭐ If this project helps you, please star it on GitHub!

</div>
