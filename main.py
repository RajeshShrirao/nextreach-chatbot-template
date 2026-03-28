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
    
    return f"""You are a friendly assistant for {biz['business_name']}.

About us:
- Location: {biz.get('location', 'N/A')}
- Hours: {biz.get('hours', 'N/A')}
- Services: {services}

Common questions and answers:
{faq_text}

How to behave:
- Talk like a real person who works at the clinic. Warm, casual, helpful.
- Use the info above to answer. Don't make stuff up.
- If you genuinely don't know something, say: "{biz.get('escalation', 'Let me connect you with our team.')}"
- Keep it short — 2-3 sentences max unless they ask for details.
- If someone sounds worried or in pain, be extra reassuring and offer to book them in right away.
- Mention specific prices/services from the info above when relevant — people love concrete answers.
- Don't be robotic. No "As an AI" or "I'm a virtual assistant."
- One emoji max per message, and only if it fits naturally."""

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
