import logging
import json
from typing import Optional
import asyncio
from dotenv import load_dotenv

# Load environment variables FIRST, before any other imports
load_dotenv(override=True)

from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from rag_pipeline import RAGPipeline
from ingest import PDFIngester

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="AI Policy Analyzer", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

rag_pipeline = None


@app.on_event("startup")
async def startup_event():
    global rag_pipeline
    logger.info("Starting up AI Policy Analyzer...")
    try:
        rag_pipeline = RAGPipeline()
        logger.info("RAG Pipeline initialized successfully")
    except ValueError as e:
        logger.error(f"Configuration error: {e}")
        logger.error("Please set your GROQ_API_KEY in .env file or as environment variable")
        rag_pipeline = None
    except Exception as e:
        logger.error(f"Error initializing RAG Pipeline: {e}")
        rag_pipeline = None


class ChatRequest(BaseModel):
    question: str
    include_web_search: bool = True


class PolicyEvaluationRequest(BaseModel):
    policy_text: str


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "ok",
        "service": "AI Policy Analyzer",
        "rag_ready": rag_pipeline is not None and rag_pipeline.index is not None
    }


@app.post("/chat")
async def chat(request: ChatRequest):
    """
    Answer a policy question using RAG.
    Returns streamed response with sources.
    """
    if rag_pipeline is None or rag_pipeline.index is None:
        raise HTTPException(
            status_code=503,
            detail="RAG pipeline not initialized. Please ensure FAISS index is built."
        )

    try:
        # Retrieve relevant chunks
        retrieved = rag_pipeline.retrieve_chunks(request.question, top_k=5)
        sources = [item["metadata"] for item in retrieved]

        # Get web results if requested
        web_results = []
        if request.include_web_search:
            from web_search import search_web
            web_results = search_web(request.question, max_results=5)

        # Format context
        context = rag_pipeline.format_context(retrieved, web_results)

        # Generate response with streaming
        def generate():
            try:
                # Get streaming response from Groq via RAG pipeline
                stream = rag_pipeline.generate_response(context, request.question, use_streaming=True)

                # Iterate through Groq stream chunks
                for chunk in stream:
                    if chunk.choices and len(chunk.choices) > 0:
                        delta = chunk.choices[0].delta
                        if delta and delta.content:
                            yield json.dumps({"type": "content", "data": delta.content}) + "\n"

                # Send sources at the end
                yield json.dumps({"type": "sources", "data": sources}) + "\n"
                yield json.dumps({"type": "done"}) + "\n"

            except Exception as e:
                logger.error(f"Streaming error: {e}")
                yield json.dumps({"type": "error", "data": str(e)}) + "\n"

        return StreamingResponse(generate(), media_type="application/x-ndjson")

    except Exception as e:
        logger.error(f"Chat error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/evaluate-policy")
async def evaluate_policy(request: PolicyEvaluationRequest):
    """
    Evaluate a user-submitted policy against reference policies and global examples.
    Returns structured evaluation with alignment score, gaps, and recommendations.
    """
    if rag_pipeline is None or rag_pipeline.index is None:
        raise HTTPException(
            status_code=503,
            detail="RAG pipeline not initialized. Please ensure FAISS index is built."
        )

    try:
        evaluation, sources = rag_pipeline.evaluate_policy(request.policy_text)

        return JSONResponse({
            "evaluation": evaluation,
            "sources": sources
        })

    except Exception as e:
        logger.error(f"Policy evaluation error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/ingest")
async def trigger_ingest():
    """
    Trigger re-ingestion of PDFs from the data/pdfs directory.
    This rebuilds the FAISS index.
    """
    try:
        logger.info("Starting PDF ingestion...")
        ingester = PDFIngester()
        ingester.ingest_pdfs()

        global rag_pipeline
        rag_pipeline = RAGPipeline()

        return JSONResponse({
            "status": "success",
            "message": "PDFs ingested and index rebuilt",
            "chunks_created": len(ingester.chunks) if ingester.chunks else 0
        })

    except Exception as e:
        logger.error(f"Ingestion error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/documents")
async def list_documents():
    """List all documents in the FAISS index."""
    if rag_pipeline is None or rag_pipeline.metadata is None:
        raise HTTPException(status_code=503, detail="RAG pipeline not ready")

    # Get unique documents
    documents = {}
    for meta in rag_pipeline.metadata:
        filename = meta.get("filename", "Unknown")
        page = meta.get("page", 0)
        if filename not in documents:
            documents[filename] = {"pages": set()}
        documents[filename]["pages"].add(page)

    result = [
        {"filename": name, "pages": sorted(list(info["pages"]))}
        for name, info in documents.items()
    ]

    return JSONResponse({"documents": result})


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
