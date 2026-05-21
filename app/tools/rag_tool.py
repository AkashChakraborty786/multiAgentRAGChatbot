from langchain_core.tools import Tool

from app.rag.retriever import retriever


def retrieve_docs(query: str) -> str:
    docs = retriever.invoke(query)
    if not docs:
        return "No relevant documents found in the knowledge base."
    return "\n\n---\n\n".join(
        f"Source: {doc.metadata.get('source', 'unknown')}\n{doc.page_content}"
        for doc in docs
    )


rag_tool = Tool(
    name="rag_retriever",
    description=(
        "Search the internal enterprise knowledge base (uploaded PDF corpus) for "
        "AI, RAG, vector databases, cloud, and cybersecurity topics. Use when the user "
        "asks about 'the knowledge', 'the corpus', 'our documents', or internal/reference material."
    ),
    func=retrieve_docs,
)
