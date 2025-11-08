# app/main.py
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from app.ai_engine import procesar_mensaje_usuario
from starlette.middleware.cors import CORSMiddleware  

app = FastAPI(
    title="Chatbot IA + SQLite",
    description="Chatbot con Gemini y base de datos local para recomendaciones y soporte.",
    version="1.0.0"
)

# ... (todo tu código de add_middleware y mount) ...
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/", response_class=HTMLResponse)
async def root():
    with open("static/index.html", "r", encoding="utf-8") as f:
        return f.read()


class ChatRequest(BaseModel):
    message: str
