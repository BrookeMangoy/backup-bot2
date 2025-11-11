# app/ai_engine.py - VERSIÓN FINAL DE AJUSTE DE BÚSQUEDA

import os
import google.generativeai as genai
from dotenv import load_dotenv
from app.crud import buscar_productos, obtener_info_empresa

load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

if not GOOGLE_API_KEY:
    raise ValueError(" Falta la clave API de Google en el archivo .env")

genai.configure(api_key=GOOGLE_API_KEY)

generation_config = {
    "temperature": 0.75,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 1024,
}

modelo = genai.GenerativeModel(
    model_name="models/gemini-2.5-flash",
    generation_config=generation_config,
)

def generar_respuesta_con_gemini(contexto: str, pregunta: str, nombre_chatbot: str = "Mocca") -> str:
    """Respuesta rápida, con personalidad y sin sobrecargar el modelo."""
    prompt = f"""
Eres {nombre_chatbot}, asistente de Stone Creek Coffee. Ayudas a clientes a elegir cafés, chocolates y combos de origen peruano.
Eres amable, entusiasta y breve.

Antes de responder:
1. ¿Qué quiere el cliente? (info de un producto, un combo, la dirección)
2. ¿Qué productos tenemos que coinciden? (usando el contexto)
3. Responde en 1-3 frases, con emoji si aplica. ☕🍫
4. Termina con una pregunta corta para seguir (ej: ¿Te gustaría pedirlo?, ¿Te provoca algo más?).

Contexto:
{contexto}

Pregunta del cliente:
{pregunta}

Responde como {nombre_chatbot}:
"""

    try:
        respuesta = modelo.generate_content(prompt)
        
        if not respuesta.candidates or not respuesta.candidates[0].content.parts:
            return "¡Ay, me quedé pensando demasiado! ¿Podrías decirme un poco más sobre lo que buscas? Por ejemplo: ¿un café, un chocolate o un combo? ¡Te ayudaré con gusto!"

        return respuesta.text.strip()

    except Exception as e:
        # Esto te ayudará a diagnosticar si hay problemas de API en el servidor
        print(f"Error de Gemini/API: {e}") 
        return "¡Ups! Me quedé sin ideas por un momento. ¿Podrías intentarlo de nuevo? 🙏"

CONVERSATION_HISTORY = {}

def procesar_mensaje_usuario(mensaje: str, user_id: str = "default_user") -> str:
    """Decide si buscar en BD o usar IA, y genera una respuesta con personalidad y memoria."""
    
    if user_id not in CONVERSATION_HISTORY:
        CONVERSATION_HISTORY[user_id] = []

    CONVERSATION_HISTORY[user_id].append({"role": "user", "content": mensaje})

    if len(CONVERSATION_HISTORY[user_id]) > 5:
        CONVERSATION_HISTORY[user_id].pop(0)

    # Obtener info general de la empresa
    info = obtener_info_empresa()
    nombre_chatbot = info.get("chatbot_nombre", "Mocca")
    empresa_descripcion = info.get("empresa_descripcion", "")

    historial_texto = "\n".join([
        f"{'Usuario' if msg['role'] == 'user' else 'Mocca'}: {msg['content']}"
        for msg in CONVERSATION_HISTORY[user_id]
    ])

    
    # Lista de nombres específicos (cortos y fáciles de buscar)
    # Ordenados por longitud (los más largos primero) para evitar coincidencias parciales incorrectas
    nombres_a_buscar = [
        "fuerte amanecer", "piura blanco", "sal de maras", "geisha de altura",
        "Pack degustación café", "Pack degustación chocolate", "Pack dúo",
        "tunkimayo", "chuncho", "aguaymanto", "cremosa", "descafeinado", 
        "chocolate", "café", "combo", "barra", "tableta", "cafe", "chocolates"
    ]
    
    
    # 2. Palabras clave de información
    es_info_empresa = any(palabra in mensaje.lower() for palabra in ["empresa", "misión", "visión", "contacto", "teléfono", "email", "dirección", "ubicados"])

    # 3. Identificar si la consulta es sobre productos
    es_productos = any(palabra in mensaje.lower() for palabra in nombres_a_buscar)


    if es_productos:
        
        # --- LÓGICA DE EXTRACCIÓN MEJORADA ---
        termino_busqueda = None
        mensaje_lower = mensaje.lower()
        
        # Iterar para encontrar el nombre de producto más específico en el mensaje
        for nombre in nombres_a_buscar:
            if nombre in mensaje_lower:
                termino_busqueda = nombre # Encontró una coincidencia
                break
        
        # Si no encontró un nombre específico, usa la última palabra como último recurso
        if not termino_busqueda:
             termino_busqueda = mensaje_lower.split()[-1]


        # Realiza la búsqueda en SQLite
        productos = buscar_productos(termino_busqueda)
        
        # --- Lógica de Contexto ---
        if productos:
            # Si encuentra productos, construye el contexto con la información real de la BD
            contexto = "Productos que coinciden con tu búsqueda:\n"
            for p in productos:
                # ¡Asegurar el formato de precio!
                contexto += f"- **{p['nombre']}** (S/ {p['precio']:.2f})\n  {p['descripcion']}\n  Detalles: {p['detalles']}\n\n"
        else:
            # Si la búsqueda falla
            contexto = f"""
No encontré el producto {termino_busqueda.capitalize()} en el inventario. 
Nuestras categorías principales son: Cafés, Chocolates y Combos. 
¿Te gustaría saber sobre el café Tunkimayo, la Tableta Piura Blanco, o algún Combo?
"""
        
        # Añadir historial al contexto
        contexto += f"\n\nHistorial de la conversación:\n{historial_texto}"

        respuesta = generar_respuesta_con_gemini(contexto, mensaje, nombre_chatbot)

    elif es_info_empresa:
        # (Lógica de información de la empresa)
        contexto = f"""Información de la empresa:
Nombre: {info.get('nombre', 'Stone Creek Coffee')}
Misión: {info.get('mision', 'Ofrecer la esencia auténtica del café y cacao peruano.')}
Visión: {info.get('vision', 'Ser la marca latinoamericana líder en experiencias de cata consciente.')}
Contacto: Teléfono {info.get('telefono', '')} / Email {info.get('email', '')}
Dirección: {info.get('direccion', '')}
Descripción: {empresa_descripcion}

Historial de la conversación:
{historial_texto}"""

        respuesta = generar_respuesta_con_gemini(contexto, mensaje, nombre_chatbot)
    
    else:
        # (Respuesta genérica)
        contexto = f"""Eres {nombre_chatbot}, asistente de Stone Creek Coffee. Tu misión es ayudar a los clientes a descubrir su bebida o postre ideal. Eres amable y entusiasta.

Empresa: {empresa_descripcion}

Pregunta del cliente: {mensaje}

Historial de la conversación:
{historial_texto}"""

        respuesta = generar_respuesta_con_gemini(contexto, mensaje, nombre_chatbot)

    # Guardar respuesta en historial
    CONVERSATION_HISTORY[user_id].append({"role": "assistant", "content": respuesta})
    return respuesta