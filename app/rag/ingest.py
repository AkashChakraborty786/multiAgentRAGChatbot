from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

from app.rag.paths import DEFAULT_PDF
from app.rag.vectordb import vectorstore
# from paths import DEFAULT_PDF
# from vectordb import vectorstore

loader = PyPDFLoader(str(DEFAULT_PDF))
docs = loader.load()

splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
chunks = splitter.split_documents(docs)
vectorstore.add_documents(chunks)
print(f"Ingestion complete to ChromaDB ({len(chunks)} chunks from {DEFAULT_PDF})!")
