"""
Módulo de gestión de conexión a SQL Server.
Fase 1: Infraestructura DB - Conexión pyodbc con variables de entorno.
"""

import os
import sys
from typing import Optional, Any
from datetime import datetime

# Terceros
import pyodbc
from dotenv import load_dotenv

# Cargar variables de entorno desde .env
load_dotenv()


class DatabaseConnectionError(Exception):
    """Excepción personalizada para errores de conexión a la base de datos."""
    pass


def _build_connection_string() -> str:
    """
    Construye la cadena de conexión ODBC desde variables de entorno.

    Returns:
        str: Cadena de conexión completa para pyodbc.

    Raises:
        DatabaseConnectionError: Si faltan variables de entorno obligatorias.
    """
    # Variables requeridas
    server = os.getenv('DB_SERVER')
    database = os.getenv('DB_NAME')
    uid = os.getenv('DB_UID')
    pwd = os.getenv('DB_PWD')

    # Validar que estén definidas
    required_vars = {
        'DB_SERVER': server,
        'DB_NAME': database,
        'DB_UID': uid,
        'DB_PWD': pwd
    }

    missing = [key for key, value in required_vars.items() if not value]
    if missing:
        raise DatabaseConnectionError(
            f"Variables de entorno faltantes: {', '.join(missing)}. "
            "Verificar archivo .env o configuración del sistema."
        )

    # Driver ODBC (permite override vía variable de entorno)
    driver = os.getenv('DB_DRIVER', 'ODBC Driver 17 for SQL Server')

    # Construir connection string
    conn_str = (
        f"Driver={{{driver}}};"
        f"Server={server};"
        f"Database={database};"
        f"UID={uid};"
        f"PWD={pwd};"
        "TrustServerCertificate=yes;"
        "Timeout=30;"
    )

    return conn_str


def conectar_db() -> pyodbc.Connection:
    """
    Establece conexión con la base de datos SQL Server.

    Returns:
        pyodbc.Connection: Objeto de conexión activa.

    Raises:
        DatabaseConnectionError: Si no se puede establecer la conexión.
    """
    try:
        conn_str = _build_connection_string()
        connection = pyodbc.connect(conn_str)
        connection.autocommit = False  # Usar transacciones explícitas
        return connection

    except pyodbc.Error as e:
        # Capturar error específico de pyodbc/SQL Server
        sqlstate = e.args[0] if e.args else 'Unknown'
        error_msg = str(e)

        raise DatabaseConnectionError(
            f"Error al conectar a SQL Server (SQLSTATE: {sqlstate}): {error_msg}"
        ) from e

    except Exception as e:
        # Cualquier otro error inesperado
        raise DatabaseConnectionError(
            f"Error inesperado al conectar: {str(e)}"
        ) from e


def test_connection() -> dict:
    """
    Prueba la conexión ejecutando una consulta simple.

    Returns:
        dict: Resultado de la prueba con timestamp y versión SQL Server.

    Raises:
        DatabaseConnectionError: Si la prueba falla.
    """
    try:
        with conectar_db() as conn:
            cursor = conn.cursor()

            # Consulta simple para verificar conectividad
            cursor.execute("SELECT @@VERSION AS Version")
            row = cursor.fetchone()

            if row:
                return {
                    'success': True,
                    'timestamp': datetime.now().isoformat(),
                    'sql_server_version': row.Version.strip(),
                    'message': 'Conexión exitosa a SQL Server'
                }
            else:
                raise DatabaseConnectionError(
                    "Conexión establecida pero la consulta no retornó resultados."
                )

    except DatabaseConnectionError:
        # Re-lanzar sin modificar
        raise
    except Exception as e:
        raise DatabaseConnectionError(
            f"Error durante prueba de conexión: {str(e)}"
        ) from e


def ejecutar_query(query: str, params: Optional[tuple] = None) -> list:
    """
    Ejecuta una consulta SELECT y retorna todos los resultados.

    Args:
        query: Sentencia SQL a ejecutar.
        params: Tupla de parámetros para consulta parametrizada.

    Returns:
        list: Lista de filas resultantes.
    """
    try:
        with conectar_db() as conn:
            cursor = conn.cursor()
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)

            # Obtener todas las filas
            columns = [column[0] for column in cursor.description]
            results = []
            for row in cursor.fetchall():
                results.append(dict(zip(columns, row)))

            return results

    except pyodbc.Error as e:
        raise DatabaseConnectionError(f"Error en consulta: {e}") from e


def ejecutar_non_query(query: str, params: Optional[tuple] = None) -> int:
    """
    Ejecuta una consulta INSERT, UPDATE o DELETE.

    Args:
        query: Sentencia SQL a ejecutar.
        params: Tupla de parámetros para consulta parametrizada.

    Returns:
        int: Número de filas afectadas.
    """
    try:
        with conectar_db() as conn:
            cursor = conn.cursor()
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)

            conn.commit()
            return cursor.rowcount

    except pyodbc.Error as e:
        conn.rollback()
        raise DatabaseConnectionError(f"Error en operación: {e}") from e


# ==============================================
# Bloque de prueba (se ejecuta solo si se corre directamente)
# ==============================================
if __name__ == "__main__":
    print("=" * 60)
    print("PRUEBA DE CONEXIÓN - Fase 1 DB Infra")
    print("=" * 60)

    try:
        result = test_connection()
        print(f"✓ Estado: {result['success']}")
        print(f"✓ Mensaje: {result['message']}")
        print(f"✓ Timestamp: {result['timestamp']}")
        print(f"✓ SQL Server: {result['sql_server_version'][:80]}...")
        print("\n¡Conexión exitosa!")

    except DatabaseConnectionError as e:
        print(f"✗ ERROR: {e}")
        print("\nRevise:")
        print("  1. Que el archivo .env exista con los valores correctos")
        print("  2. Que SQL Server esté corriendo")
        print("  3. Que el driver ODBC esté instalado")
        print("  4. Que el usuario tenga permisos")
        sys.exit(1)

    except Exception as e:
        print(f"✗ ERROR INESPERADO: {e}")
        sys.exit(1)
