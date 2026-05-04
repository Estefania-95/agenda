"""
Script de inicialización automática de la base de datos.
Lee el archivo SQL y lo ejecuta en el servidor configurado.
"""

import sys
import os
import pyodbc
from dotenv import load_dotenv

# Agregar raíz al path para importar src
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.database import build_connection_string

def initialize_database():
    """Ejecuta el script SQL de inicialización."""
    load_dotenv()
    
    sql_file_path = os.path.join('fase1_db_infra', 'init_db.sql')
    if not os.path.exists(sql_file_path):
        print(f"Error: No se encuentra el archivo {sql_file_path}")
        return

    print("--- INICIALIZACIÓN DE BASE DE DATOS ---")
    
    # Intentar conexión inicial al servidor (base de datos 'master' para crear la nuestra)
    try:
        # Modificamos el connection string para apuntar a master inicialmente
        conn_str = build_connection_string()
        # Reemplazar base de datos por master para la creación inicial
        conn_str = conn_str.replace(f"DATABASE={os.getenv('DB_NAME')}", "DATABASE=master")
        
        print(f"Conectando al servidor {os.getenv('DB_SERVER')}...")
        conn = pyodbc.connect(conn_str, autocommit=True)
        cursor = conn.cursor()
        
        print(f"Leyendo script: {sql_file_path}")
        with open(sql_file_path, 'r', encoding='utf-8') as f:
            sql_script = f.read()

        # Separar el script por 'GO' (SQL Server standard)
        commands = sql_script.split('GO')
        
        print("Ejecutando comandos SQL...")
        for cmd in commands:
            if cmd.strip():
                try:
                    cursor.execute(cmd)
                except Exception as e:
                    # Algunos errores (como si el usuario ya existe) son esperables
                    if "already exists" in str(e).lower() or "ya existe" in str(e).lower():
                        continue
                    print(f"Nota en comando: {e}")
        
        print("\n¡Base de datos inicializada correctamente!")
        conn.close()
        
    except Exception as e:
        print(f"\nError crítico durante la inicialización: {e}")
        print("\nSugerencias:")
        print("1. Asegúrate de que SQL Server esté en modo de autenticación mixta.")
        print("2. Verifica que las credenciales en .env tengan permisos de sysadmin o dbcreator.")
        sys.exit(1)

if __name__ == "__main__":
    initialize_database()
