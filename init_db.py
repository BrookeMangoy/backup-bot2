
import sqlite3
import os

os.makedirs("data", exist_ok=True)

conn = sqlite3.connect("data/empresa.db")
cursor = conn.cursor()


cursor.execute("""
CREATE TABLE IF NOT EXISTS productos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    descripcion TEXT NOT NULL,
    categoria TEXT,
    precio REAL,
    disponible BOOLEAN DEFAULT 1,
    detalles TEXT  -- Información adicional para el chatbot
)   
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS empresa_info (
    clave TEXT PRIMARY KEY,
    valor TEXT NOT NULL
)
""")

productos_ejemplo = [
    ("Caja Origen Café", 
     "Caja con 2 variedades de grano (250g c/u) + ficha de cata + tips de preparación.",
     "Café", 45.0, 1,
     "• Variedad 1: Guatemala Altura Volcánica - Notas a chocolate y especias\n• Variedad 2: Colombia Supremo - Acidez brillante y notas cítricas\n• Incluye guía de molienda y extracción para cafetera francesa, pour over y espresso"),
    
    ("Caja Origen Chocolate", 
     "3 barras de origen único + guía de maridaje + perfil de cata exclusivo.",
     "Chocolate", 52.0, 1,
     "• Barra 1: Ecuador 70% - Notas florales y frutales\n• Barra 2: Perú 65% - Sabores terrosos y nueces tostadas\n• Barra 3: Madagascar 80% - Frutas rojas y acidez vibrante\n• Guía de maridaje con café, vino y queso"),
    
    ("Caja Experiencia Dual", 
     "1 café + 1 chocolate seleccionados + maridaje perfecto + guía de combinaciones.",
     "Combo", 65.0, 1,
     "• Café: Guatemala Altura Volcánica (250g)\n• Chocolate: Ecuador 70% (80g)\n• Guía de maridaje: cómo combinar ambos para realzar sabores\n• Tips: temperatura ideal, tiempos de degustación, orden de cata")
]

cursor.executemany("""
INSERT OR IGNORE INTO productos (nombre, descripcion, categoria, precio, disponible, detalles)
VALUES (?, ?, ?, ?, ?, ?)
""", productos_ejemplo)


info_empresa = [
    ("nombre", "Stone Creek Coffee"),
    ("mision", "Ofrecer tecnología accesible y de calidad para todos."),
    ("vision", "Ser líder en innovación tecnológica en Latinoamérica para 2030."),
    ("telefono", "+56 9 1234 5678"),
    ("email", "contacto@cata-consciente.com"),
    ("direccion", "Av. Siempre Viva 123, Santiago, Chile"),
    ("chatbot_nombre", "Mocca"),
    ("empresa_descripcion", "Somos Stone Creek Coffee, especialistas en experiencias sensoriales con café y chocolate de origen. Nuestro sommelier digital, Mocca, te guiará para encontrar tu caja ideal.")
]



cursor.executemany("""
INSERT OR REPLACE INTO empresa_info (clave, valor) VALUES (?, ?)
""", info_empresa)

conn.commit()
conn.close()
print(" Base de datos actualizada con productos reales y contexto de la empresa.")