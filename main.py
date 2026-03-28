# main.py — NextReach Chatbot Template
import json
import chainlit as cl
from config import client, cfg

# Load business config
with open("config.json") as f:
    BUSINESS = json.load(f)

def build_system_prompt(biz: dict) -> str:
    faq_text = "\n".join(f"- {k}: {v}" for k, v in biz.get("faq", {}).items())
    services = ", ".join(biz.get("services", []))
    
    return f"""You are a friendly, helpful assistant for {biz['business_name']}.

About the business:
- Location: {biz.get('location', 'N/A')}
- Hours: {biz.get('hours', 'N/A')}
- Services: {services}

Frequently asked questions:
{faq_text}

Rules:
- Be warm, concise, and conversational. No corporate speak.
- Answer based ONLY on the information above. Do not make things up.
- If you don't know the answer, say: "{biz.get('escalation', 'Let me connect you with our team.')}"
- Keep responses under 3-4 sentences unless the customer needs detail.
- Use the customer's name if they share it.
- Don't use emojis excessively — one at most per message.
- Never say "As an AI" or "I'm a chatbot"."""

SYSTEM_PROMPT = build_system_prompt(BUSINESS)
GREETING = BUSINESS.get("greeting", f"Hi! I'm the {BUSINESS['business_name']} assistant. How can I help?")

@cl.on_chat_start
async def start():
    cl.user_session.set("history", [])
    await cl.Message(content=GREETING).send()

@cl.on_message
async def main(message: cl.Message):
    history = cl.user_session.get("history", [])
    history.append({"role": "user", "content": message.content})

    messages = [{"role": "system", "content": SYSTEM_PROMPT}] + history

    res = client.chat.completions.create(
        model=cfg["model"],
        messages=messages,
        max_tokens=300,
        temperature=0.7
    )
    reply = res.choices[0].message.content
    history.append({"role": "assistant", "content": reply})
    cl.user_session.set("history", history)
    await cl.Message(content=reply).send()
