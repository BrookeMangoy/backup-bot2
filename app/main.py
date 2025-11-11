# app/main.py
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from app.ai_engine import procesar_mensaje_usuario
from starlette.middleware.cors import CORSMiddleware  

app = FastAPI(
    title="Chatbot IA + SQLite",
    description="Chatbot con Gemini y base de datos local para recomendaciones y soporte.",
    version="1.0.0"
)

# Configuración de CORS para permitir que el frontend se conecte
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permite todas las origenes (para desarrollo)
    allow_credentials=True,
    allow_methods=["*"], # Permite todos los métodos (POST, GET, etc.)
    allow_headers=["*"], # Permite todos los headers
)

# Monta la carpeta 'static' para servir index.html, script.js, style.css
app.mount("/static", StaticFiles(directory="static"), name="static")

# Sirve el archivo index.html en la ruta raíz
@app.get("/", response_class=HTMLResponse)
async def root():
    try:
        with open("static/index.html", "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="index.html no encontrado.")

# --- INICIO DE LA SECCIÓN FALTANTE ---

# 1. Modelo Pydantic corregido: debe aceptar 'message' y 'user_id'
class ChatRequest(BaseModel):
    message: str
    user_id: str

# Modelo para la respuesta
class ChatResponse(BaseModel):
    reply: str

# 2. Endpoint de la API que recibe los mensajes del chat
@app.post("/api/chat", response_model=ChatResponse)
async def chat_api(request: ChatRequest):
    """
    Recibe el mensaje del usuario y el user_id, lo procesa usando
    el ai_engine y devuelve la respuesta del chatbot.
    """
    try:
        # Llama a la función que procesa la lógica del chatbot
        respuesta = procesar_mensaje_usuario(
            mensaje=request.message,
            user_id=request.user_id
        )
        
        # Devuelve la respuesta en el formato JSON esperado
        return ChatResponse(reply=respuesta)
        
    except Exception as e:
        # Imprime el error en la consola del servidor para depuración
        print(f"Error procesando el mensaje: {e}")
        # Devuelve un error HTTP 500
        raise HTTPException(
            status_code=500, 
            detail=f"Hubo un error interno en el servidor: {e}"
        )

# --- FIN DE LA SECCIÓN FALTANTE ---

# (Opcional) Para ejecutar directamente con 'python app/main.py'
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)