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
    precio REAL, -- Aseguramos que sea REAL (número con decimales)
    disponible BOOLEAN DEFAULT 1,
    detalles TEXT  
)   
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS empresa_info (
    clave TEXT PRIMARY KEY,
    valor TEXT NOT NULL
)
""")

# --- LISTA DE PRODUCTOS CON PRECIOS SOLO NUMÉRICOS (REALES) ---
productos_ejemplo = [
    # --- Cafés ---
    ("Grano Selecto: Tunkimayo", 
     "Café de especialidad 250g, notas a frutos secos y panela.",
     "Café", 48.00, 1, # <-- CORREGIDO: Solo número
     "• Origen: Cusco (Valle de Tunkimayo) • Perfil: Notas a nuez, panela, acidez media. • Proceso: Lavado. Ideal para V60 o Chemex."),
    
    ("Blend de la Casa: Fuerte Amanecer", 
     "Mezcla intensa 500g, ideal para espresso y moka.",
     "Café", 42.00, 1, # <-- CORREGIDO
     "• Origen: Blend de Chanchamayo y Cajamarca. • Perfil: Tostado oscuro, cuerpo alto, notas a chocolate amargo y muy baja acidez."),
     
    ("Café Exótico: Geisha de Altura", 
     "Grano Geisha 250g, notas florales y cítricas.",
     "Café", 65.00, 1, # <-- CORREGIDO
     "• Origen: Cajamarca (Jaén) • Perfil: Notas a jazmín, bergamota, té de durazno. • Proceso: Lavado. Una joya para métodos de goteo."),
     
    ("Descafeinado Natural", 
     "Café 250g, descafeinado por proceso natural Swiss Water.",
     "Café", 45.00, 1, # <-- CORREGIDO
     "• Origen: Cajamarca. • Perfil: Sabor suave, notas a caramelo y malta. • Proceso: Swiss Water Process, libre de químicos."),
     
    # --- Chocolates ---
    ("Tableta Piura Blanco", 
     "Barra 80g. Cacao blanco de Piura, notas cítricas y frutales.",
     "Chocolate", 22.00, 1, # <-- CORREGIDO
     "• Origen: Piura (Morropón) • Perfil: Notas a lima, frutos secos. Cremoso y de bajo amargor, único en su tipo."),
     
    ("Barra Artesanal con Sal de Maras", 
     "Barra 80g. Oscuro con cristales de Sal de Maras.",
     "Chocolate", 24.00, 1, # <-- CORREGIDO
     "• Origen: Blend peruano con Sal de Maras (Cusco). • Perfil: Contraste salino perfecto que realza las notas del cacao."),
     
    ("Tableta Cremosa", 
     "Barra 80g. Chocolate con leche (milk chocolate).",
     "Chocolate", 20.00, 1, # <-- CORREGIDO
     "• Origen: Amazonas (Bagua) • Perfil: Cremoso, notas a caramelo y nueces tostadas. El balance perfecto."),
     
    ("Barra Intensa: Chuncho", 
     "Barra 80g. Cacao Chuncho aromático, notas a frutos secos.",
     "Chocolate", 25.00, 1, # <-- CORREGIDO
     "• Origen: Cusco (Valle de La Convención) • Perfil: Cacao Chuncho muy aromático, notas a café y un toque floral."),
     
    ("Bombones de Aguaymanto", 
     "6 Bombones rellenos de ganache de aguaymanto.",
     "Chocolate", 30.00, 1, # <-- CORREGIDO
     "• Centro de ganache de chocolate 60% con pulpa de aguaymanto fresco. Cubierta de chocolate 70%."),

    # --- Combos ---
    ("Caja Degustación Café", 
     "Prueba 3 de nuestros mejores cafés de origen (150g c/u).",
     "Combo", 85.00, 1, # <-- CORREGIDO
     "• 1x Grano Selecto: Tunkimayo • 1x Café Exótico: Geisha de Altura • 1x Blend de la Casa. Incluye guía de cata."),
    
    ("Caja Degustación Chocolate", 
     "Un viaje por nuestras 3 barras artesanales más vendidas.",
     "Combo", 70.00, 1, # <-- CORREGIDO
     "• 1x Tableta Piura Blanco • 1x Barra Artesanal con Sal de Maras • 1x Barra Intensa: Chuncho. Incluye guía de maridaje."),
     
    ("Caja Dúo: Maridaje Perfecto", 
     "Un café + un chocolate seleccionados.",
     "Combo", 75.00, 1, # <-- CORREGIDO
     "• Café: Grano Selecto: Tunkimayo (250g) • Chocolate: Tableta Piura Blanco (80g) • Guía de maridaje.")
]

cursor.executemany("""
INSERT OR IGNORE INTO productos (nombre, descripcion, categoria, precio, disponible, detalles)
VALUES (?, ?, ?, ?, ?, ?)
""", productos_ejemplo)


# --- Info de la empresa ---
info_empresa = [
    ("nombre", "Stone Creek Coffee"),
    ("mision", "Ofrecer la esencia auténtica del café y cacao peruano."),
    ("vision", "Ser la marca latinoamericana líder en experiencias de cata consciente."),
    ("telefono", "+51 1 445 1234"), 
    ("email", "contacto@cata-consciente.com"),
    ("direccion", "Av. Larco 123, Miraflores, Lima, Perú"), 
    ("chatbot_nombre", "Mocca"),
    ("empresa_descripcion", "Somos Stone Creek Coffee, especialistas en experiencias sensoriales con café y chocolate de origen peruano. Nuestro sommelier digital, Mocca, te guiará para encontrar tu caja ideal.")
]


cursor.executemany("""
INSERT OR REPLACE INTO empresa_info (clave, valor) VALUES (?, ?)
""", info_empresa)

conn.commit()
conn.close()
print(" Base de datos actualizada con productos reales y contexto de la empresa.")