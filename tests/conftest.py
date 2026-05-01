"""
Configuración compartida para tests con pytest.
Fixtures comunes para mocking de base de datos.
"""

import pytest
from unittest.mock import MagicMock, patch
import os
import sys

# Añadir src al path para todos los tests
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))


@pytest.fixture(scope="session")
def mock_db_connection():
    """
    Fixture: conexión mockeada a base de datos.
    Retorna un mock de conexión pyodbc reutilizable.
    """
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value = mock_cursor
    mock_cursor.rowcount = 1
    return mock_conn


def pytest_configure(config):
    """Configuración personalizada de pytest."""
    # Registrar markers personalizados
    config.addinivalue_line(
        "markers", "integration: marks tests as integration (requires real DB)"
    )


def pytest_collection_modifyitems(config, items):
    """Saltar tests de integración si no se pasa --integration."""
    if not config.getoption("--integration", default=False):
        skip_integ = pytest.mark.skip(reason="need --integration option to run")
        for item in items:
            if "integration" in item.keywords:
                item.add_marker(skip_integ)


def pytest_addoption(parser):
    """Agregar opción --integration a pytest."""
    parser.addoption(
        "--integration",
        action="store_true",
        default=False,
        help="run integration tests with real database"
    )
