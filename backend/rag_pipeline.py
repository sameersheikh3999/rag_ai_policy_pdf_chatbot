import logging
from typing import List, Dict, Tuple
import os
import numpy as np
from sentence_transformers import SentenceTransformer
from groq import Groq
from ingest import PDFIngester
from web_search import search_web, format_search_results

logger = logging.getLogger(__name__)

MODEL_NAME = "all-MiniLM-L6-v2"
LLM_MODEL = "llama-3.3-70b-versatile"  # Latest available Groq model

# Initialize Groq client (uses GROQ_API_KEY environment variable)
try:
    groq_client = Groq()
except Exception as e:
    logger.error(f"Failed to initialize Groq client: {e}")
    logger.error("Make sure GROQ_API_KEY environment variable is set")
    raise ValueError("GROQ_API_KEY environment variable is not set. Please set it before running.")


class RAGPipeline:
    def __init__(self):
        logger.info("Initializing RAG Pipeline...")
        self.embedding_model = SentenceTransformer(MODEL_NAME)
        self.index, self.chunks, self.metadata = PDFIngester.load_index()

        if self.index is None:
            logger.warning("FAISS index not loaded. Run ingest.py first.")

    def retrieve_chunks(self, query: str, top_k: int = 5) -> List[Dict]:
        """Retrieve top-k relevant chunks from FAISS."""
        if self.index is None:
            logger.warning("Index not available")
            return []

        query_embedding = self.embedding_model.encode([query])[0].astype("float32")
        query_embedding = np.array([query_embedding])

        distances, indices = self.index.search(query_embedding, top_k)

        retrieved = []
        for idx in indices[0]:
            if 0 <= idx < len(self.metadata):
                retrieved.append({
                    "text": self.chunks[idx],
                    "metadata": self.metadata[idx]
                })

        logger.info(f"Retrieved {len(retrieved)} chunks for query")
        return retrieved

    def format_context(self, retrieved: List[Dict], web_results: List[Dict]) -> str:
        """Format retrieved chunks and web results for the prompt."""
        context = "## Policy Reference Documents\n\n"

        for i, item in enumerate(retrieved, 1):
            context += f"### Source {i}\n"
            context += f"**Document:** {item['metadata']['filename']} (Page {item['metadata']['page']})\n"
            context += f"{item['text']}\n\n"

        if web_results:
            context += "## Web Search Results\n\n"
            for i, result in enumerate(web_results, 1):
                context += f"### Web Source {i}\n"
                context += f"**{result['title']}**\n"
                context += f"{result['snippet']}\n\n"

        return context

    def generate_response(self, context: str, query: str, use_streaming: bool = True):
        """Generate response using Groq API."""
        system_prompt = """You are an expert policy analyst specializing in education policy.
Your role is to:
1. Answer questions about education policies based on provided documents
2. Provide evidence-backed insights from the reference materials
3. Cite specific documents and pages when making claims
4. Offer balanced perspectives considering multiple policy approaches

Always cite the sources you're using from the provided documents."""

        user_message = f"""Based on the following reference materials, please answer this question:

{query}

Reference Materials:
{context}

Provide a comprehensive, evidence-based answer with citations."""

        if use_streaming:
            stream = groq_client.chat.completions.create(
                model=LLM_MODEL,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_message}
                ],
                stream=True,
                temperature=0.7,
                max_tokens=1500
            )
            return stream
        else:
            try:
                response = groq_client.chat.completions.create(
                    model=LLM_MODEL,
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_message}
                    ],
                    temperature=0.7,
                    max_tokens=1500
                )
                return response.choices[0].message.content
            except Exception as e:
                logger.error(f"Error generating response: {e}")
                return f"Error: Could not generate response. {str(e)}"

    def answer_question(self, query: str, include_web_search: bool = True) -> Tuple[str, List[Dict]]:
        """Full RAG pipeline: retrieve -> augment with web -> generate."""
        retrieved = self.retrieve_chunks(query)

        web_results = []
        if include_web_search:
            web_results = search_web(query, max_results=5)

        context = self.format_context(retrieved, web_results)
        response = self.generate_response(context, query, use_streaming=False)

        sources = [item["metadata"] for item in retrieved]
        return response, sources

    def evaluate_policy(self, policy_text: str) -> Tuple[str, List[Dict]]:
        """Evaluate user's policy with comprehensive comparison and standardization."""
        query = f"Evaluate this policy direction: {policy_text[:200]}"
        retrieved = self.retrieve_chunks(query, top_k=8)

        web_results = search_web(
            f"education policy {' '.join(policy_text.split()[:10])}",
            max_results=10
        )

        # Prepare reference text
        ref_text = "\n".join([f"Source: {item['metadata']['filename']} (Page {item['metadata']['page']})\n{item['text'][:400]}" for item in retrieved[:3]])

        # Prepare web results text
        web_text = "\n".join([f"• {r['title']}: {r['snippet']}" for r in web_results[:5]])

        evaluation_prompt = f"""You are an expert education policy analyst. Provide a comprehensive evaluation of the proposed policy by:

1. COMPARING with reference policies from Pakistan and globally
2. ASSESSING alignment with international best practices
3. STANDARDIZING the policy based on proven frameworks
4. RECOMMENDING improvements and implementation steps

PROPOSED POLICY:
{policy_text}

---REFERENCE POLICIES FROM PAKISTAN:---
{ref_text}

---GLOBAL BEST PRACTICES (From Web):---
{web_text}

PROVIDE DETAILED ANALYSIS WITH:

## 1. COMPARATIVE ANALYSIS
- How does this compare to current Pakistan policies?
- How does it align with global standards (UNESCO, World Bank, etc.)?
- Key similarities and differences with reference policies
- Benchmarking against 3-5 comparable policies

## 2. ALIGNMENT ASSESSMENT
- Alignment with global best practices (1-10 score)
- Alignment with Pakistan's education context (1-10 score)
- Coverage of critical areas (curriculum, teachers, equity, quality, etc.)

## 3. POLICY STANDARDIZATION
- Recommended structure based on best practices
- Key components that should be added
- Prioritized implementation framework
- Resource and timeline estimates

## 4. STRENGTHS & GAPS
- What your policy does well
- Critical gaps compared to comprehensive frameworks
- Missing elements from successful policies
- Risk factors and mitigation strategies

## 5. STANDARDIZED RECOMMENDATIONS
- Top 5 improvements for maximum impact
- Implementation roadmap (Phase 1, 2, 3)
- Key performance indicators (KPIs)
- Monitoring and evaluation framework

Use specific references from both local and global examples. Be analytical and constructive."""

        system_prompt = """You are a senior education policy analyst with 15+ years experience.
You analyze policies by comparing them against proven frameworks and best practices from Pakistan and globally.
Provide evidence-based, structured, and actionable insights."""

        try:
            response = groq_client.chat.completions.create(
                model=LLM_MODEL,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": evaluation_prompt}
                ],
                temperature=0.7,
                max_tokens=2500
            )

            evaluation_text = response.choices[0].message.content
            sources = [
                {"type": "pdf", "metadata": r["metadata"]} for r in retrieved
            ] + [
                {"type": "web", "title": r["title"], "url": r.get("href", "")} for r in web_results
            ]

            return evaluation_text, sources

        except Exception as e:
            logger.error(f"Error evaluating policy: {e}")
            return f"Error: Could not evaluate policy. {str(e)}", []


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    rag = RAGPipeline()

    # Test Q&A
    print("Testing Q&A...")
    answer, sources = rag.answer_question("What are the key education policies in Pakistan?", include_web_search=False)
    print(f"\nAnswer:\n{answer}\n")
    print(f"Sources: {sources}")

    # Test Policy Evaluation
    print("\n\nTesting Policy Evaluation...")
    test_policy = "Implement a universal basic education guarantee with special focus on rural areas, digitalized curriculum, and teacher training programs funded through progressive taxation."
    evaluation, eval_sources = rag.evaluate_policy(test_policy)
    print(f"\nEvaluation:\n{evaluation}")
