import os
import json
import logging
from pathlib import Path
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer
from typing import List, Dict

logger = logging.getLogger(__name__)

PDF_DIR = Path(__file__).parent / "data" / "pdfs"
FAISS_DIR = Path(__file__).parent / "data" / "faiss_index"
FAISS_DIR.mkdir(parents=True, exist_ok=True)

CHUNK_SIZE = 800
CHUNK_OVERLAP = 100
MODEL_NAME = "all-MiniLM-L6-v2"


class PDFIngester:
    def __init__(self):
        logger.info("Loading sentence transformer model...")
        self.model = SentenceTransformer(MODEL_NAME)
        self.chunks = []
        self.metadata = []
        self.index = None

    def extract_text_from_file(self, file_path: str) -> List[Dict]:
        """Extract text from PDF or text file."""
        try:
            file_name = Path(file_path).name
            pages_data = []

            # Try to handle as PDF first
            if file_path.endswith(".pdf"):
                try:
                    import fitz
                    doc = fitz.open(file_path)
                    for page_num, page in enumerate(doc, 1):
                        text = page.get_text()
                        if text.strip():
                            pages_data.append({
                                "page": page_num,
                                "text": text,
                                "filename": file_name
                            })
                    doc.close()
                except ImportError:
                    logger.warning(f"PyMuPDF not available, treating {file_name} as text")
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                        text = f.read()
                    pages_data.append({
                        "page": 1,
                        "text": text,
                        "filename": file_name
                    })
            else:
                # Handle as text file
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    text = f.read()
                pages_data.append({
                    "page": 1,
                    "text": text,
                    "filename": file_name
                })

            logger.info(f"Extracted {len(pages_data)} pages from {file_name}")
            return pages_data
        except Exception as e:
            logger.error(f"Error reading {file_path}: {e}")
            return []

    def chunk_text(self, text: str, chunk_size: int = CHUNK_SIZE, overlap: int = CHUNK_OVERLAP) -> List[str]:
        """Split text into overlapping chunks."""
        words = text.split()
        chunks = []

        for i in range(0, len(words), chunk_size - overlap):
            chunk = " ".join(words[i:i + chunk_size])
            if chunk.strip():
                chunks.append(chunk)

        return chunks

    def ingest_documents(self):
        """Process all PDFs/text files and build FAISS index."""
        if not PDF_DIR.exists():
            logger.warning(f"PDF directory not found: {PDF_DIR}")
            return

        # Get both PDF and text files
        doc_files = list(PDF_DIR.glob("*.pdf")) + list(PDF_DIR.glob("*.txt"))
        if not doc_files:
            logger.warning(f"No document files found in {PDF_DIR}")
            return

        logger.info(f"Found {len(doc_files)} documents to ingest")

        for doc_file in sorted(doc_files):
            logger.info(f"Processing {doc_file.name}...")
            pages = self.extract_text_from_file(str(doc_file))

            for page_data in pages:
                page_chunks = self.chunk_text(page_data["text"])
                for chunk_text in page_chunks:
                    self.chunks.append(chunk_text)
                    self.metadata.append({
                        "filename": page_data["filename"],
                        "page": page_data["page"],
                        "text": chunk_text[:500]  # Store preview
                    })

        logger.info(f"Total chunks created: {len(self.chunks)}")

        if self.chunks:
            self.build_index()
            self.save_index()
            logger.info("✓ Ingestion complete!")
        else:
            logger.error("No chunks created - check your documents")

    def build_index(self):
        """Build FAISS index from chunks."""
        logger.info("Embedding chunks...")
        embeddings = self.model.encode(self.chunks, show_progress_bar=True)
        embeddings = np.array(embeddings).astype("float32")

        logger.info(f"Building FAISS index for {len(embeddings)} vectors...")
        dimension = embeddings.shape[1]
        self.index = faiss.IndexFlatL2(dimension)
        self.index.add(embeddings)

        logger.info(f"FAISS index created with {self.index.ntotal} vectors")

    def save_index(self):
        """Save FAISS index and metadata."""
        if self.index is None:
            logger.error("No index to save")
            return

        index_path = FAISS_DIR / "index.faiss"
        metadata_path = FAISS_DIR / "metadata.json"

        faiss.write_index(self.index, str(index_path))
        with open(metadata_path, "w") as f:
            json.dump({
                "chunks": self.chunks,
                "metadata": self.metadata
            }, f, indent=2)

        logger.info(f"Index saved to {index_path}")
        logger.info(f"Metadata saved to {metadata_path}")

    @staticmethod
    def load_index():
        """Load saved FAISS index and metadata."""
        index_path = FAISS_DIR / "index.faiss"
        metadata_path = FAISS_DIR / "metadata.json"

        if not index_path.exists() or not metadata_path.exists():
            logger.warning("Index or metadata not found")
            return None, [], []

        index = faiss.read_index(str(index_path))
        with open(metadata_path, "r") as f:
            data = json.load(f)

        return index, data.get("chunks", []), data.get("metadata", [])


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    ingester = PDFIngester()
    ingester.ingest_documents()
