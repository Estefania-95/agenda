"""
Script de configuración inicial del servidor - Fase 1/5.
Usa Windows Authentication para crear la DB y el usuario de la aplicación.
"""

import sys
import os
import pyodbc
from dotenv import load_dotenv

# Agregar raíz al path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

def setup_server():
    load_dotenv()
    
    server = os.getenv('DB_SERVER', r'localhost\SQLEXPRESS')
    db_name = os.getenv('DB_NAME', 'GestionDB')
    user = os.getenv('DB_UID', 'gestion_user')
    password = os.getenv('DB_PWD', 'ChangeMe_123!')
    driver = os.getenv('DB_DRIVER', 'ODBC Driver 17 for SQL Server')

    print("=" * 60)
    print("CONFIGURACIÓN INICIAL DE SQL SERVER")
    print("=" * 60)
    
    # Intentar conexión con Windows Authentication (Trusted_Connection)
    conn_str = (
        f"Driver={{{driver}}};"
        f"Server={server};"
        f"Database=master;"
        f"Trusted_Connection=yes;"
        f"TrustServerCertificate=yes;"
    )
    
    try:
        print(f"1. Conectando al servidor '{server}' con Windows Auth...")
        conn = pyodbc.connect(conn_str, autocommit=True)
        cursor = conn.cursor()
        
        # 1. Crear Base de Datos
        print(f"2. Creando base de datos '{db_name}'...")
        cursor.execute(f"IF NOT EXISTS (SELECT * FROM sys.databases WHERE name = '{db_name}') CREATE DATABASE {db_name}")
        
        # 2. Crear Login (Nivel Servidor)
        print(f"3. Configurando login de servidor '{user}'...")
        cursor.execute(f"""
            IF NOT EXISTS (SELECT * FROM sys.server_principals WHERE name = '{user}')
            BEGIN
                CREATE LOGIN {user} WITH PASSWORD = '{password}', CHECK_POLICY = OFF;
            END
            ELSE
            BEGIN
                ALTER LOGIN {user} WITH PASSWORD = '{password}';
            END
        """)
        
        # 3. Configurar Usuario en la DB (Nivel Base de Datos)
        print(f"4. Configurando usuario en la base de datos '{db_name}'...")
        cursor.execute(f"USE {db_name}")
        cursor.execute(f"""
            IF NOT EXISTS (SELECT * FROM sys.database_principals WHERE name = '{user}')
            BEGIN
                CREATE USER {user} FOR LOGIN {user};
            END
            EXEC sp_addrolemember 'db_owner', '{user}';
        """)
        
        # 4. Crear Tabla Personas (si no existe)
        print("5. Creando tablas e índices...")
        sql_path = os.path.join('fase1_db_infra', 'init_db.sql')
        if os.path.exists(sql_path):
            with open(sql_path, 'r', encoding='utf-8') as f:
                # Filtrar el script para que no intente crear la DB de nuevo
                # y ejecutar solo los CREATE TABLE / INDEX
                script = f.read()
                # Separar por GO y ejecutar
                for cmd in script.split('GO'):
                    if cmd.strip() and 'CREATE DATABASE' not in cmd.upper():
                        try:
                            cursor.execute(cmd)
                        except Exception as e:
                            if "already exists" not in str(e).lower():
                                print(f"   Nota: {e}")

        print("\n" + "=" * 60)
        print("¡CONFIGURACIÓN COMPLETADA EXITOSAMENTE!")
        print(f"Base de datos: {db_name}")
        print(f"Usuario: {user}")
        print("=" * 60)
        print("\nAhora puedes ejecutar: python src/seed_db.py")
        
        conn.close()
        
    except Exception as e:
        print(f"\n[ERROR CRÍTICO]: {e}")
        print("\nSugerencias:")
        print("1. Verifica que el nombre del servidor en .env coincida con la captura (SQLEXPRESS).")
        print(f"2. Verifica que el driver '{driver}' esté instalado.")
        print("3. Si el error es 'Login failed', intenta abrir 'SQL Server Configuration Manager'")
        print("   y activa 'SQL Server and Windows Authentication mode' (Mixed Mode).")

if __name__ == "__main__":
    setup_server()
