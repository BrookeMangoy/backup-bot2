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

# --- LISTA DE PRODUCTOS CON NOMBRES SIMPLIFICADOS ---
productos_ejemplo = [
    # --- Cafés (Bebidas) ---
    ("Espresso", 
     "Café corto e intenso, 2oz.",
     "Café", 7.0, 1,
     "Un shot concentrado de café, la base de todo. Fuerte y aromático."),

    ("Americano", 
     "Café clásico de 10oz.",
     "Café", 8.0, 1,
     "Un espresso diluido con agua caliente. Perfecto para cualquier momento."),

    ("Cappuccino", 
     "Café con leche espumosa, 8oz.",
     "Café", 12.0, 1,
     "Partes iguales de espresso, leche vaporizada y espuma de leche. Decorado con cacao."),

    ("Latte", 
     "Café con más leche, 10oz.",
     "Café", 13.0, 1,
     "Un shot de espresso con abundante leche vaporizada y una ligera capa de espuma."),
     
    ("Mocaccino", 
     "El balance perfecto de café y chocolate.",
     "Café", 14.0, 1,
     "Un latte con un toque de nuestro chocolate de la casa y crema batida."),

    # --- Chocolates (Postres y Bebidas) ---
    ("Chocolate Caliente", 
     "Espeso y cremoso, estilo de la casa.",
     "Chocolate", 15.0, 1,
     "Nuestra receta especial de chocolate espeso, perfecto para días fríos. Se sirve con marshmallows."),

    ("Torta de Chocolate", 
     "Tajada de torta húmeda con fudge.",
     "Chocolate", 16.0, 1,
     "Keke húmedo de chocolate, relleno y cubierto con nuestro fudge de la casa."),

    ("Brownie con Helado", 
     "Brownie tibio con helado de vainilla.",
     "Chocolate", 18.0, 1,
     "Brownie denso de chocolate, servido tibio con una bola de helado de vainilla y salsa de fudge."),

    ("Caja de Bombones", # <-- CAMBIO DE NOMBRE
     "Bombones de chocolate surtidos (6 unidades).",
     "Chocolate", 30.0, 1,
     "Una caja con 6 bombones artesanales rellenos de manjar, menta y praliné."),

    ("Galleta de Chocolate", # <-- CAMBIO DE NOMBRE
     "Galleta grande y suave con chispas de chocolate.",
     "Chocolate", 9.0, 1,
     "Recién horneada, suave por dentro y crujiente por fuera."),

    # --- Combos (Actualizados) ---
    ("Combo Clásico", 
     "Un Americano (10oz) y una Torta de Chocolate.",
     "Combo", 22.0, 1,
     "El maridaje perfecto: la acidez del café con el dulce de nuestra torta de fudge."),
    
    ("Combo Dulce", 
     "Un Chocolate Caliente y un Brownie.",
     "Combo", 30.0, 1,
     "Ideal para los amantes del chocolate. Nuestro chocolate espeso con un brownie tibio."),
    
    ("Combo de Tarde", 
     "Un Cappuccino (8oz) y Galleta de Chocolate.", # <-- CAMBIO DE NOMBRE
     "Combo", 19.0, 1,
     "La pausa perfecta para la tarde. Un cappuccino espumoso y una galleta recién horneada.")
]

cursor.executemany("""
INSERT OR IGNORE INTO productos (nombre, descripcion, categoria, precio, disponible, detalles)
VALUES (?, ?, ?, ?, ?, ?)
""", productos_ejemplo)


# --- Info de la empresa (Dirección en Lima) ---
info_empresa = [
    ("nombre", "Stone Creek Coffee"),
    ("mision", "Ofrecer tecnología accesible y de calidad para todos."),
    ("vision", "Ser líder en innovación tecnológica en Latinoamérica para 2030."),
    ("telefono", "+51 1 445 1234"), # Teléfono de Lima
    ("email", "contacto@cata-consciente.com"),
    ("direccion", "Av. Larco 123, Miraflores, Lima, Perú"), # Dirección en Lima
    ("chatbot_nombre", "Mocca"),
    ("empresa_descripcion", "Somos Stone Creek Coffee, una cafetería de especialidad en el corazón de Miraflores. Nuestro sommelier digital, Mocca, te ayudará a elegir tu bebida o postre ideal.")
]


cursor.executemany("""
INSERT OR REPLACE INTO empresa_info (clave, valor) VALUES (?, ?)
""", info_empresa)

conn.commit()
conn.close()
print(" Base de datos actualizada con productos reales y contexto de la empresa.")