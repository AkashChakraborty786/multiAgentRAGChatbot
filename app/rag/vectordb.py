from langchain_chroma import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings

from app.rag.paths import CHROMA_DIR
# from paths import CHROMA_DIR

embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
vectorstore = Chroma(
    persist_directory=str(CHROMA_DIR),
    embedding_function=embedding_model,
)
