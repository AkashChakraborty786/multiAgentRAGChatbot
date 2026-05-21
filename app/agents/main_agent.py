from dotenv import load_dotenv

load_dotenv()

from langchain_groq import ChatGroq
from langchain_classic.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate

from app.tools.google_search_tool import google_search_tool
from app.tools.rag_tool import rag_tool
# -----------------------------------
# LLM
# -----------------------------------

llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0
)

# -----------------------------------
# Prompt
# -----------------------------------

prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        """
You are a helpful enterprise AI assistant with two tools. Pick exactly one per turn based on the user message:

1. rag_retriever — internal knowledge base (uploaded PDF corpus). Use when the user asks about:
   - "the knowledge", "knowledge base", "corpus", "our documents", "from the documents"
   - topics covered in enterprise docs: AI fundamentals, RAG, vector DBs, cloud, cybersecurity
   - summaries or key points from internal/reference material

2. google_search — live public web. Use when the user asks about:
   - current events, news, weather, sports scores, stock prices, recent releases
   - facts that need up-to-date internet data and are NOT about the internal corpus
   - general web questions with no reference to internal documents

Rules:
- Call one tool with a focused search query, then answer using only that tool's results.
- Do not call both tools unless the user explicitly needs internal docs AND live web data.
- If the question is a simple greeting or chit-chat, respond directly without tools.
- If unsure between tools, prefer rag_retriever for document/knowledge wording; otherwise google_search.
"""
    ),
    ("human", "{input}"),
    ("placeholder", "{agent_scratchpad}")
])

# -----------------------------------
# Tools
# -----------------------------------

tools = [rag_tool, google_search_tool]

# -----------------------------------
# Agent
# -----------------------------------

agent = create_tool_calling_agent(
    llm=llm,
    tools=tools,
    prompt=prompt
)

# -----------------------------------
# Executor
# -----------------------------------

agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True
)

agent = agent_executor