# app/crud.py - VERSIÓN CORREGIDA PARA EXTRAER DATOS CON CLAVES

import sqlite3
from app.database import get_db_connection

# --- FUNCIÓN CORREGIDA PARA GARANTIZAR QUE SE EXTRAIGA EL PRECIO ---
def buscar_productos(busqueda: str):
    """
    Busca productos por nombre, categoría o detalles, y los devuelve como una lista de diccionarios.
    """
    conn = get_db_connection()
    # Usamos row_factory para que los resultados sean diccionarios (con claves) en lugar de tuplas.
    conn.row_factory = sqlite3.Row 
    cursor = conn.cursor()
    
    # La búsqueda ahora es más amplia, buscando el término en nombre, categoría y detalles.
    query = """
        SELECT nombre, descripcion, precio, categoria, detalles
        FROM productos
        WHERE nombre LIKE ? OR categoria LIKE ? OR detalles LIKE ?
    """
    # El término de búsqueda se envuelve con comodines (%) para buscar coincidencias parciales.
    termino = f"%{busqueda}%"
    
    cursor.execute(query, (termino, termino, termino))
    
    productos_db = cursor.fetchall()
    conn.close()
    
    # Convertimos los resultados (que son objetos sqlite3.Row) en diccionarios para el AI Engine
    productos_list = []
    for row in productos_db:
        productos_list.append(dict(row))
        
    return productos_list

# --- FUNCIÓN DE INFO DE LA EMPRESA (Se mantiene) ---
def obtener_info_empresa():
    """
    Obtiene toda la información clave de la empresa.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT clave, valor FROM empresa_info")
    info_db = cursor.fetchall()
    conn.close()
    
    info_dict = {clave: valor for clave, valor in info_db}
    return info_dict