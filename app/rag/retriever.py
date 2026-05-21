from app.rag.vectordb import vectorstore
retriever = vectorstore.as_retriever(search_kwargs={"k": 4})