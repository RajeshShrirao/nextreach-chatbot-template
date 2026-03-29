# main.py — NextReach Chatbot Template
import json
import chainlit as cl
from config import client, cfg

# Load business config
with open("config.json") as f:
    BUSINESS = json.load(f)

def build_system_prompt(biz: dict) -> str:
    # Handle FAQ in both formats: dict or list of {q, a} objects
    faq_raw = biz.get("faq", {})
    if isinstance(faq_raw, dict):
        faq_text = "\n".join(f"- {k}: {v}" for k, v in faq_raw.items())
    elif isinstance(faq_raw, list):
        faq_text = "\n".join(f"- Q: {item['q']}\n  A: {item['a']}" for item in faq_raw if 'q' in item and 'a' in item)
    else:
        faq_text = "No FAQ data available."
    
    # Handle services in both formats: list of strings or list of {name, price, duration} objects
    services_raw = biz.get("services", [])
    if services_raw and isinstance(services_raw[0], dict):
        services = "\n".join(f"- {s.get('name', 'Unknown')}: {s.get('price', 'N/A')}" for s in services_raw)
    else:
        services = ", ".join(str(s) for s in services_raw)
    
    business_type = biz.get('business_type', 'business')
    
    return f"""You are a friendly AI receptionist for {biz['business_name']}, a {business_type}.

About us:
- Location: {biz.get('location', 'N/A')}
- Hours: {biz.get('hours', 'N/A')}
{f"- Phone: {biz.get('phone', 'N/A')}" if biz.get('phone') else ''}

Services and Pricing:
{services}

Common Questions:
{faq_text}

How to behave:
- Talk like a real person who works here. Warm, casual, helpful.
- Use the info above to answer. Don't make stuff up.
- If you genuinely don't know something, say: "{biz.get('escalation', 'Let me connect you with our team.')}"
- Keep it short — 2-3 sentences max unless they ask for details.
- Mention specific prices/services from the info above when relevant — people love concrete answers.
- Don't be robotic. No "As an AI" or "I'm a virtual assistant."
- One emoji max per message, and only if it fits naturally.
- If someone wants to book, collect: their name, phone, pet name/breed, desired service, and preferred time.
- Always be honest about what you don't know — never guess prices or policies."""

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
