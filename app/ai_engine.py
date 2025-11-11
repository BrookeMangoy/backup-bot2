
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
Eres {nombre_chatbot}, asistente de TechSoluciones S.A. Ayudas a clientes a elegir su caja ideal de café/chocolate. Eres amable, entusiasta y breve.

Antes de responder:
1. ¿Qué quiere el cliente? (regalo, info, experiencia)
2. ¿Qué productos tenemos que coinciden?
3. Responde en 1-3 frases, con emoji si aplica.
4. Termina con una pregunta corta para seguir.

Contexto:
{contexto}

Pregunta del cliente:
{pregunta}

Responde como {nombre_chatbot}:
"""

    try:
        respuesta = modelo.generate_content(prompt)
        

        if not respuesta.candidates or not respuesta.candidates[0].content.parts:
            return "¡Ay, me quedé pensando demasiado!  ¿Podrías decirme un poco más sobre lo que buscas? Por ejemplo: ¿prefieres café, chocolate, o ambos? ¡Te ayudaré con gusto!"

        return respuesta.text.strip()

    except Exception as e:
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


    palabras_producto = ["caja", "producto", "recomienda", "venden", "tienen", "comprar", "café", "chocolate", "dual"]
    palabras_regalo = ["regalo", "regalar", "presente", "detalle", "sorpresa", "cumpleaños", "aniversario"]

    es_productos = any(palabra in mensaje.lower() for palabra in palabras_producto + palabras_regalo)
    es_info_empresa = any(palabra in mensaje.lower() for palabra in ["empresa", "misión", "visión", "contacto", "teléfono", "email", "dirección", "quién", "qué hacen", "dónde"])

    if es_productos:
        productos = buscar_productos(mensaje)
        if productos:
            contexto = "Productos disponibles:\n"
            for p in productos:
                contexto += f"- **{p['nombre']}** (${p['precio']:.2f})\n  {p['descripcion']}\n  Detalles: {p['detalles']}\n\n"
        else:
            if any(palabra in mensaje.lower() for palabra in palabras_regalo):
                contexto = """
Nuestras cajas son ideales como regalo porque ofrecen una experiencia sensorial única.
Te recomiendo estas opciones:

• **Caja Origen Café** (S/45): Perfecta para amantes del café. Incluye 2 variedades de grano (250g c/u), ficha de cata detallada y tips de preparación profesional.

• **Caja Origen Chocolate** (S/52): Ideal para quienes disfrutan del chocolate artesanal. Incluye 3 barras de origen único, guía de maridaje y perfil de cata exclusivo.

• **Caja Experiencia Dual** (S/65): La opción más completa. Combina café y chocolate seleccionados para realzar sabores, con guía de combinaciones.

¿Te gustaría que te ayude a elegir según el gusto de la persona?
"""
            else:
                contexto = "No encontré productos relacionados con tu consulta. ¿Quizás quisiste decir 'Caja Origen Café', 'Caja Origen Chocolate' o 'Experiencia Dual'?"
        
        # Añadir historial al contexto
        contexto += f"\n\nHistorial de la conversación:\n{historial_texto}"

        respuesta = generar_respuesta_con_gemini(contexto, mensaje, nombre_chatbot)

        # Guardar respuesta en historial
        CONVERSATION_HISTORY[user_id].append({"role": "assistant", "content": respuesta})
        return respuesta

    elif es_info_empresa:
        contexto = f"""Información de la empresa:
Nombre: {info.get('nombre', 'Stone Creek Coffee')}
Misión: {info.get('mision', 'Conectar a las personas con la esencia auténtica del café y el chocolate de origen')}
Visión: {info.get('vision', 'Ser la marca latinoamericana líder en experiencias de cata consciente, reconocida por su compromiso con la calidad, la sostenibilidad ')}
Contacto: Teléfono {info.get('telefono', '')} / Email {info.get('email', '')}
Dirección: {info.get('direccion', '')}
Descripción: {empresa_descripcion}

Historial de la conversación:
{historial_texto}"""

        respuesta = generar_respuesta_con_gemini(contexto, mensaje, nombre_chatbot)
        CONVERSATION_HISTORY[user_id].append({"role": "assistant", "content": respuesta})
        return respuesta

    else:
        contexto = f"""Eres {nombre_chatbot}, asistente de TechSoluciones S.A. Tu misión es ayudar a los clientes a descubrir su caja ideal de café y chocolate de origen. Eres amable, entusiasta, y conocedor de nuestros productos.

Empresa: {empresa_descripcion}

Pregunta del cliente: {mensaje}

Historial de la conversación:
{historial_texto}"""

        respuesta = generar_respuesta_con_gemini(contexto, mensaje, nombre_chatbot)
        CONVERSATION_HISTORY[user_id].append({"role": "assistant", "content": respuesta})
        return respuesta