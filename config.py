# config.py — universal provider switcher
import os
from openai import OpenAI

PROVIDER = os.getenv("PROVIDER", "cerebras")

PROVIDERS = {
    "cerebras": {
        "base_url": "https://api.cerebras.ai/v1",
        "api_key": os.getenv("CEREBRAS_API_KEY"),
        "model": "llama-4-scout-17b-16e-instruct"
    },
    "openai": {
        "base_url": "https://api.openai.com/v1",
        "api_key": os.getenv("OPENAI_API_KEY"),
        "model": "gpt-4o-mini"
    },
    "groq": {
        "base_url": "https://api.groq.com/openai/v1",
        "api_key": os.getenv("GROQ_API_KEY"),
        "model": "llama-3.3-70b-versatile"
    }
}

cfg = PROVIDERS[PROVIDER]
client = OpenAI(base_url=cfg["base_url"], api_key=cfg["api_key"])
