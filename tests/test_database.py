"""
Tests unitarios para src/database.py - Fase 1.
Pruebas de conexión y funciones auxiliares.
"""

import sys
import os
import pytest
import pyodbc
from unittest.mock import patch, MagicMock

# Añadir directorio src al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from src.database import (
    conectar_db,
    test_connection as db_test_connection,
    ejecutar_query,
    ejecutar_non_query,
    DatabaseConnectionError,
    _build_connection_string
)


# ==============================================
# Fixtures
# ==============================================
@pytest.fixture
def mock_env_vars():
    """Mock de variables de entorno válidas."""
    env = {
        'DB_SERVER': 'localhost\\SQLEXPRESS',
        'DB_NAME': 'GestionDB',
        'DB_UID': 'test_user',
        'DB_PWD': 'test_pass'
    }
    with patch.dict(os.environ, env, clear=True):
        yield env


@pytest.fixture
def mock_pyodbc_connect():
    """Mock de conexión pyodbc exitosa."""
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value = mock_cursor
    mock_cursor.fetchone.return_value = ['Microsoft SQL Server 2019']
    return mock_conn


# ==============================================
# Tests de _build_connection_string
# ==============================================
def test_build_connection_string_exito(mock_env_vars):
    """Test: construcción exitosa de connection string."""
    with patch('src.database.load_dotenv'):
        conn_str = _build_connection_string()

        assert 'Driver={ODBC Driver 17 for SQL Server}' in conn_str
        assert 'Server=localhost\\SQLEXPRESS' in conn_str
        assert 'Database=GestionDB' in conn_str
        assert 'UID=test_user' in conn_str
        assert 'PWD=test_pass' in conn_str
        assert 'TrustServerCertificate=yes' in conn_str
        assert 'Timeout=30' in conn_str


def test_build_connection_string_faltan_vars():
    """Test: error si faltan variables de entorno."""
    with patch('src.database.load_dotenv'):
        with patch.dict(os.environ, {}, clear=True):
            with pytest.raises(DatabaseConnectionError) as exc:
                _build_connection_string()

            assert "Variables de entorno faltantes" in str(exc.value)


def test_build_connection_string_driver_personalizado(mock_env_vars):
    """Test: uso de driver personalizado desde variable de entorno."""
    os.environ['DB_DRIVER'] = 'ODBC Driver 18 for SQL Server'

    with patch('src.database.load_dotenv'):
        conn_str = _build_connection_string()
        assert 'Driver={ODBC Driver 18 for SQL Server}' in conn_str


# ==============================================
# Tests de conectar_db
# ==============================================
def test_conectar_db_exito(mock_env_vars, mock_pyodbc_connect):
    """Test: conexión exitosa con pyodbc."""
    with patch('src.database.load_dotenv'), \
         patch('pyodbc.connect', return_value=mock_pyodbc_connect):
        conn = conectar_db()
        assert conn is not None
        assert conn.autocommit is False


def test_conectar_db_error_pyodbc(mock_env_vars):
    """Test: error al conectar con pyodbc."""
    with patch('src.database.load_dotenv'), \
         patch('pyodbc.connect', side_effect=pyodbc.Error("Conexión fallida")):
        with pytest.raises(DatabaseConnectionError) as exc:
            conectar_db()

        assert "Error al conectar a SQL Server" in str(exc.value)


# ==============================================
# Tests de test_connection
# ==============================================
def test_test_connection_exito(mock_env_vars, mock_pyodbc_connect):
    """Test: prueba de conexión exitosa."""
    with patch('src.database.load_dotenv'), \
         patch('pyodbc.connect', return_value=mock_pyodbc_connect):
        result = db_test_connection()

        assert result['success'] is True
        assert 'timestamp' in result
        assert 'Microsoft SQL Server' in result['sql_server_version']


def test_test_connection_error(mock_env_vars):
    """Test: prueba de conexión fallida."""
    with patch('src.database.load_dotenv'), \
         patch('pyodbc.connect', side_effect=pyodbc.Error("Servidor no encontrado")):
        with pytest.raises(DatabaseConnectionError):
            db_test_connection()


# ==============================================
# Tests de ejecutar_query
# ==============================================
def test_ejecutar_query_exito(mock_env_vars):
    """Test: ejecución de SELECT con resultados."""
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value = mock_cursor
    mock_cursor.description = [('id',), ('nombre',)]
    mock_cursor.fetchall.return_value = [(1, ' Juan '), (2, ' María ')]

    with patch('src.database.load_dotenv'), \
         patch('pyodbc.connect', return_value=mock_conn):
        result = ejecutar_query("SELECT * FROM Personas")

        assert len(result) == 2
        assert result[0]['id'] == 1
        assert result[0]['nombre'].strip() == 'Juan'


def test_ejecutar_query_parametros(mock_env_vars):
    """Test: ejecución de SELECT con parámetros."""
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value = mock_cursor
    mock_cursor.description = [('id',)]
    mock_cursor.fetchall.return_value = [(1,)]

    with patch('src.database.load_dotenv'), \
         patch('pyodbc.connect', return_value=mock_conn):
        ejecutar_query("SELECT id FROM Personas WHERE cuil = ?", ('20-12345678-9',))

        # Verificar que se llamó con parámetros
        assert mock_cursor.execute.called
        args, _ = mock_cursor.execute.call_args
        assert args[1] == ('20-12345678-9',)


# ==============================================
# Tests de ejecutar_non_query
# ==============================================
def test_ejecutar_non_query_exito(mock_env_vars):
    """Test: ejecución de INSERT/UPDATE/DELETE."""
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value = mock_cursor
    mock_cursor.rowcount = 1

    with patch('src.database.load_dotenv'), \
         patch('pyodbc.connect', return_value=mock_conn):
        rows = ejecutar_non_query(
            "INSERT INTO Personas (nombre) VALUES (?)",
            ('Juan',)
        )

        assert rows == 1
        mock_conn.commit.assert_called_once()


def test_ejecutar_non_query_error(mock_env_vars):
    """Test: rollback en error de non-query."""
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value = mock_cursor
    mock_cursor.execute.side_effect = pyodbc.Error("Error SQL")

    with patch('src.database.load_dotenv'), \
         patch('pyodbc.connect', return_value=mock_conn):
        with pytest.raises(DatabaseConnectionError):
            ejecutar_non_query("INSERT INTO Personas VALUES (?)", ('Juan',))

        mock_conn.rollback.assert_called_once()
