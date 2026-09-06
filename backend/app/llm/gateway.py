"""
LLM Gateway / Router.
Provides a unified interface for agents to get an LLM instance,
routing to Groq or Gemini based on agent role or explicit choice.
"""

import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Default model routing per agent role (can be overridden)
DEFAULT_ROUTING = {
    "ceo": "groq",
    "finance": "gemini",
    "product": "groq",
    "developer": "groq",
    "marketing": "gemini",
}

GROQ_MODEL = "openai/gpt-oss-120b"
GEMINI_MODEL = "gemini-3.6-flash"


def get_llm(agent_role: str, provider_override: str | None = None):
    """
    Returns a LangChain chat model instance for the given agent role.
    provider_override: force "groq" or "gemini" regardless of default routing.
    """
    provider = provider_override or DEFAULT_ROUTING.get(agent_role, "groq")

    if provider == "groq":
        return ChatGroq(api_key=GROQ_API_KEY, model=GROQ_MODEL, temperature=0.3)
    elif provider == "gemini":
        return ChatGoogleGenerativeAI(
            model=GEMINI_MODEL, google_api_key=GEMINI_API_KEY, temperature=0.3
        )
    else:
        raise ValueError(f"Unknown provider: {provider}")