from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = PROJECT_ROOT / "data"
CHROMA_DIR = PROJECT_ROOT / "chromadb"
DEFAULT_PDF = DATA_DIR / "rag_enriched_corpus.pdf"
