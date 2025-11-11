
from app.database import get_db_connection
def buscar_productos(palabras_clave: str):
    """Busca productos por nombre o descripción (case-insensitive)."""
    conn = get_db_connection()
    cursor = conn.cursor()
    query = """
    SELECT id, nombre, descripcion, categoria, precio, detalles
    FROM productos
    WHERE disponible = 1
      AND (nombre LIKE ? OR descripcion LIKE ? OR detalles LIKE ?)
    """
    like_pattern = f"%{palabras_clave}%"
    cursor.execute(query, (like_pattern, like_pattern, like_pattern))
    productos = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return productos

def obtener_info_empresa(clave: str = None):
    """Obtiene toda la info de la empresa o una clave específica."""
    conn = get_db_connection()
    cursor = conn.cursor()
    if clave:
        cursor.execute("SELECT valor FROM empresa_info WHERE clave = ?", (clave,))
        row = cursor.fetchone()
        conn.close()
        return row["valor"] if row else None
    else:
        cursor.execute("SELECT clave, valor FROM empresa_info")
        info = {row["clave"]: row["valor"] for row in cursor.fetchall()}
        conn.close()
        return info