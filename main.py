from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from rag import retrieve_context
from memory import save_memory, load_memory
from prompts import SYSTEM_PROMPT
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class ChatRequest(BaseModel):
    session_id: str
    message: str
    mode: str

@app.post("/chat")
def chat(req: ChatRequest):

    # 1️⃣ Retrieve relevant resume context
    context = retrieve_context(req.message)

    # 2️⃣ Load conversation history
    history = load_memory(req.session_id)

    # 3️⃣ Build structured messages properly
    messages = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT
        },
        {
            "role": "system",
            "content": f"Mode: {req.mode}"
        }
    ]

    # Inject retrieved context if exists
    if context:
        messages.append({
            "role": "system",
            "content": f"Relevant Experience Context:\n{context}"
        })

    # Add previous conversation history
    for msg in history:
        if "user" in msg:
            messages.append({
                "role": "user",
                "content": msg["user"]
            })
        if "assistant" in msg:
            messages.append({
                "role": "assistant",
                "content": msg["assistant"]
            })

    # Add current user message
    messages.append({
        "role": "user",
        "content": req.message
    })

    # 4️⃣ Call LLM
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        temperature=0.3
    )

    answer = response.choices[0].message.content

    # 5️⃣ Save memory
    save_memory(req.session_id, {"user": req.message})
    save_memory(req.session_id, {"assistant": answer})

    return {"response": answer}
