# app/database.py
import sqlite3
import os

DATABASE_PATH = "data/empresa.db"

def get_db_connection():
    """Devuelve una conexión a la base de datos SQLite."""
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row 
    return conn