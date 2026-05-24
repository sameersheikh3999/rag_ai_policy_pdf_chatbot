#!/usr/bin/env python
"""Test script to verify Groq API and RAG pipeline setup"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

print("=" * 60)
print("AI Policy Analyzer - Setup Test")
print("=" * 60)

# Check 1: API Key
print("\n[1] Checking GROQ_API_KEY...")
api_key = os.getenv("GROQ_API_KEY")
if api_key:
    masked_key = api_key[:10] + "..." + api_key[-5:] if len(api_key) > 15 else "***"
    print(f"    ✓ API key found: {masked_key}")
else:
    print("    ✗ GROQ_API_KEY not set")
    print("    Please add it to .env file: GROQ_API_KEY=your_key_here")
    exit(1)

# Check 2: Groq Client
print("\n[2] Initializing Groq client...")
try:
    from groq import Groq
    client = Groq()
    print("    ✓ Groq client initialized")
except Exception as e:
    print(f"    ✗ Error: {e}")
    exit(1)

# Check 3: Dependencies
print("\n[3] Checking dependencies...")
dependencies = [
    ("sentence-transformers", "SentenceTransformer"),
    ("faiss", "faiss"),
    ("fastapi", "fastapi"),
    ("uvicorn", "uvicorn"),
]

all_ok = True
for package, import_name in dependencies:
    try:
        __import__(import_name)
        print(f"    ✓ {package}")
    except ImportError:
        print(f"    ✗ {package} - run: pip install {package}")
        all_ok = False

if not all_ok:
    exit(1)

# Check 4: FAISS Index
print("\n[4] Checking FAISS index...")
if os.path.exists("data/faiss_index/index.faiss"):
    print("    ✓ FAISS index found")
else:
    print("    ✗ FAISS index not found")
    print("    Run: python ingest.py")
    exit(1)

# Check 5: Test Groq Connection (non-streaming)
print("\n[5] Testing Groq API connection...")
try:
    response = client.chat.completions.create(
        model="mixtral-8x7b-32768",
        messages=[
            {"role": "user", "content": "Say 'Hello' in one word"}
        ],
        max_tokens=10,
        temperature=0
    )
    print(f"    ✓ API response: {response.choices[0].message.content[:30]}")
except Exception as e:
    print(f"    ✗ Error: {e}")
    exit(1)

# Check 6: Test RAG Pipeline
print("\n[6] Initializing RAG Pipeline...")
try:
    from rag_pipeline import RAGPipeline
    rag = RAGPipeline()
    print("    ✓ RAG Pipeline initialized")
    if rag.index is not None:
        print(f"      - Index loaded with {len(rag.chunks)} chunks")
        print(f"      - Metadata items: {len(rag.metadata)}")
    else:
        print("      - Index not ready")
except Exception as e:
    print(f"    ✗ Error: {e}")
    exit(1)

print("\n" + "=" * 60)
print("✓ All checks passed! Ready to start the backend.")
print("=" * 60)
print("\nStart the backend with:")
print("  python -m uvicorn main:app --host 127.0.0.1 --port 8001")
