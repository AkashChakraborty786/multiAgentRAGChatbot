import os

import serpapi
from dotenv import load_dotenv
from langchain_core.tools import Tool

load_dotenv()


def google_search(query: str) -> str:
    api_key = os.getenv("SERPAPI_API_KEY")
    if not api_key:
        return "Google search is not configured. Set SERPAPI_API_KEY in .env."

    client = serpapi.Client(api_key=api_key)
    results = client.search({"engine": "google", "q": query, "num": 5})
    organic = results.get("organic_results", [])
    if not organic:
        return f"No web results found for: {query}"

    return "\n\n".join(
        f"{i}. {r.get('title', 'N/A')}\n   {r.get('link', '')}\n   {r.get('snippet', '')}"
        for i, r in enumerate(organic[:5], start=1)
    )


google_search_tool = Tool(
    name="google_search",
    description=(
        "Search the public web for current events, news, live data, or general facts "
        "not in the internal knowledge base. Use for weather, stock prices, recent news, "
        "and anything requiring up-to-date internet information."
    ),
    func=google_search,
)
