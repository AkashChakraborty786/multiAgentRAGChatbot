from dotenv import load_dotenv

load_dotenv()

from fastapi import FastAPI
from pydantic import BaseModel

from app.agents.main_agent import agent

app = FastAPI()

class ChatRequest(BaseModel):
    query: str

@app.post("/chat")
def chat(req: ChatRequest):
    response = agent.invoke(
        {"input": req.query}
    )

    return {
        "response": response["output"]
    }