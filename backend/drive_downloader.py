import os
import base64
import json
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

DRIVE_FOLDER_ID = "18srNcGKevzodmYjO8W_N1L5AqPwpyCdI"
PDF_DIR = Path(__file__).parent / "data" / "pdfs"
PDF_DIR.mkdir(parents=True, exist_ok=True)


def get_file_ids_from_folder():
    """Returns file IDs from the previously saved drive folder query."""
    tool_results_file = Path.home() / ".claude" / "projects" / "c--Users-HP-Pictures-AI-Projects-AI-Policy-Analyzer-Tool" / "16387a08-a93e-4931-8478-90f0a2082026" / "tool-results" / "mcp-claude_ai_Google_Drive-search_files-1779558005213.txt"

    if not tool_results_file.exists():
        logger.warning("Google Drive file list not found. Please run the search first.")
        return []

    try:
        with open(tool_results_file, 'r') as f:
            data = json.load(f)

        pdf_files = [f for f in data.get("files", []) if f["mimeType"] == "application/pdf"]
        logger.info(f"Found {len(pdf_files)} PDF files")
        return pdf_files
    except Exception as e:
        logger.error(f"Error reading file list: {e}")
        return []


def download_pdfs_manual():
    """
    Returns information about PDFs that need to be downloaded.
    In a real scenario, you would use the Google Drive MCP tools to download these.
    For now, this provides a manifest of what needs to be downloaded.
    """
    pdf_files = get_file_ids_from_folder()

    manifest = {
        "total_files": len(pdf_files),
        "files": [
            {
                "id": f["id"],
                "title": f["title"],
                "mimeType": f["mimeType"],
                "path": str(PDF_DIR / f["title"])
            }
            for f in pdf_files
        ]
    }

    manifest_path = Path(__file__).parent / "data" / "download_manifest.json"
    with open(manifest_path, "w") as f:
        json.dump(manifest, f, indent=2)

    logger.info(f"Download manifest created at {manifest_path}")
    logger.info(f"Total files to download: {len(pdf_files)}")
    return manifest


def check_downloaded_files():
    """Check which PDFs are already downloaded."""
    if not PDF_DIR.exists():
        return []

    downloaded = [f.name for f in PDF_DIR.glob("*.pdf")]
    logger.info(f"Found {len(downloaded)} downloaded PDFs")
    return downloaded


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    manifest = download_pdfs_manual()
    downloaded = check_downloaded_files()
    print(f"Downloaded: {len(downloaded)}/{manifest['total_files']} PDFs")
