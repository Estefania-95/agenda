"""
Tests unitarios para src/crud_personas.py - Fase 2.
Pruebas de operaciones CRUD y validaciones.
"""

import sys
import os
import pytest
from datetime import datetime
from unittest.mock import patch, MagicMock

# Añadir directorio src al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from src.crud_personas import (
    crear_persona,
    obtener_persona,
    actualizar_persona,
    eliminar_persona,
    listar_personas,
    contar_personas,
    validar_cuil,
    validar_nombre_apellido,
    ValidacionError,
    DuplicadoError
)


# ==============================================
# Tests de Validaciones
# ==============================================
def test_validar_cuil_formato_correcto():
    """Test: CUIL con formato válido."""
    assert validar_cuil("20-12345678-9") is True
    assert validar_cuil("27-98765432-1") is True


def test_validar_cuil_formato_incorrecto():
    """Test: CUIL con formatos inválidos."""
    with pytest.raises(ValidacionError):
        validar_cuil("20123456789")  # Sin guiones

    with pytest.raises(ValidacionError):
        validar_cuil("20-1234567-9")  # Solo 7 dígitos en medio

    with pytest.raises(ValidacionError):
        validar_cuil("20-12345678-")  # Sin dígito verificador

    with pytest.raises(ValidacionError):
        validar_cuil("20-12345678-99")  # 2 dígitos verificadores


def test_validar_nombre_apellido_correcto():
    """Test: nombres/apellidos válidos."""
    assert validar_nombre_apellido("Juan", "nombre") is True
    assert validar_nombre_apellido("María", "nombre") is True
    assert validar_nombre_apellido("González", "apellido") is True
    assert validar_nombre_apellido("  Pedro  ", "nombre") is True  # Espacios extremos


def test_validar_nombre_apellido_vacio():
    """Test: nombre/apellido vacío."""
    with pytest.raises(ValidacionError):
        validar_nombre_apellido("", "nombre")

    with pytest.raises(ValidacionError):
        validar_nombre_apellido("   ", "apellido")


def test_validar_nombre_apellido_longitud():
    """Test: longitud fuera de rango."""
    corto = "a"
    with pytest.raises(ValidacionError):
        validar_nombre_apellido(corto, "nombre")

    largo = "a" * 101
    with pytest.raises(ValidacionError):
        validar_nombre_apellido(largo, "apellido")


def test_validar_nombre_apellido_caracteres_invalidos():
    """Test: caracteres no permitidos."""
    with pytest.raises(ValidacionError):
        validar_nombre_apellido("Juan123", "nombre")

    with pytest.raises(ValidacionError):
        validar_nombre_apellido("María@", "apellido")

    with pytest.raises(ValidacionError):
        validar_nombre_apellido("Pedro-Juan", "nombre")


# ==============================================
# Tests de CRUD (con mocking de DB)
# ==============================================
@pytest.fixture
def mock_db_connection():
    """Mock de conexión a base de datos."""
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value = mock_cursor
    return mock_conn


def test_crear_persona_exito(mock_db_connection):
    """Test: creación exitosa de persona."""
    mock_cursor = mock_db_connection.cursor.return_value
    mock_cursor.rowcount = 1

    with patch('src.crud_personas.conectar_db', return_value=mock_db_connection), \
         patch('src.crud_personas.validar_cuil'), \
         patch('src.crud_personas.validar_nombre_apellido'):
        result = crear_persona("Juan", "Pérez", "20-12345678-9")

        assert result is True
        mock_cursor.execute.assert_called_once()
        mock_db_connection.commit.assert_called_once()


def test_crear_persona_cuil_duplicado(mock_db_connection):
    """Test: error al crear persona con CUIL duplicado."""
    mock_cursor = mock_db_connection.cursor.return_value
    # Simular error de integridad (UNIQUE constraint)
    import pyodbc
    mock_cursor.execute.side_effect = pyodbc.IntegrityError("UNIQUE constraint failed")

    with patch('src.crud_personas.conectar_db', return_value=mock_db_connection), \
         patch('src.crud_personas.validar_cuil'), \
         patch('src.crud_personas.validar_nombre_apellido'):
        with pytest.raises(DuplicadoError) as exc:
            crear_persona("Juan", "Pérez", "20-12345678-9")

        assert "Ya existe una persona con CUIL" in str(exc.value)
        mock_db_connection.rollback.assert_called_once()


def test_obtener_persona_existente(mock_db_connection):
    """Test: obtener persona existente."""
    mock_cursor = mock_db_connection.cursor.return_value
    mock_cursor.fetchone.return_value = (1, 'Juan', 'Pérez', '20-12345678-9', datetime(2024, 1, 1))

    with patch('src.crud_personas.conectar_db', return_value=mock_db_connection):
        result = obtener_persona(1)

        assert result is not None
        assert result['id'] == 1
        assert result['nombre'] == 'Juan'
        assert result['apellido'] == 'Pérez'


def test_obtener_persona_no_existente(mock_db_connection):
    """Test: obtener persona que no existe."""
    mock_cursor = mock_db_connection.cursor.return_value
    mock_cursor.fetchone.return_value = None

    with patch('src.crud_personas.conectar_db', return_value=mock_db_connection):
        result = obtener_persona(9999)
        assert result is None


def test_actualizar_persona_exito(mock_db_connection):
    """Test: actualización exitosa."""
    mock_cursor = mock_db_connection.cursor.return_value
    mock_cursor.rowcount = 1

    with patch('src.crud_personas.conectar_db', return_value=mock_db_connection), \
         patch('src.crud_personas.validar_cuil'), \
         patch('src.crud_personas.validar_nombre_apellido'):
        result = actualizar_persona(1, nombre="Juan Carlos", apellido="Perez")

        assert result is True
        mock_cursor.execute.assert_called_once()
        args, _ = mock_cursor.execute.call_args
        # Verificar que los parámetros incluyen los nuevos valores
        assert "Juan Carlos" in args[0]
        mock_db_connection.commit.assert_called_once()


def test_actualizar_persona_no_existente(mock_db_connection):
    """Test: actualizar persona que no existe."""
    mock_cursor = mock_db_connection.cursor.return_value
    mock_cursor.rowcount = 0

    with patch('src.crud_personas.conectar_db', return_value=mock_db_connection), \
         patch('src.crud_personas.validar_cuil'):
        result = actualizar_persona(9999, nombre="Juan")

        assert result is False


def test_eliminar_persona_exito(mock_db_connection):
    """Test: eliminación exitosa."""
    mock_cursor = mock_db_connection.cursor.return_value
    mock_cursor.rowcount = 1

    with patch('src.crud_personas.conectar_db', return_value=mock_db_connection):
        result = eliminar_persona(1)

        assert result is True
        mock_cursor.execute.assert_called_once()
        mock_db_connection.commit.assert_called_once()


def test_eliminar_persona_no_existente(mock_db_connection):
    """Test: eliminar persona que no existe."""
    mock_cursor = mock_db_connection.cursor.return_value
    mock_cursor.rowcount = 0

    with patch('src.crud_personas.conectar_db', return_value=mock_db_connection):
        result = eliminar_persona(9999)
        assert result is False


def test_listar_personas_sin_filtros(mock_db_connection):
    """Test: listar todas las personas."""
    mock_cursor = mock_db_connection.cursor.return_value
    mock_cursor.description = [('id',), ('nombre',), ('apellido',), ('cuil',), ('fecha_registro',)]
    mock_cursor.fetchall.return_value = [
        (1, 'Juan', 'Pérez', '20-12345678-9', datetime(2024, 1, 1)),
        (2, 'María', 'Gómez', '27-87654321-0', datetime(2024, 1, 2))
    ]

    with patch('src.crud_personas.conectar_db', return_value=mock_db_connection):
        result = listar_personas()

        assert len(result) == 2
        assert result[0]['nombre'] == 'Juan'


def test_listar_personas_con_filtro_nombre(mock_db_connection):
    """Test: listar con filtro por nombre."""
    mock_cursor = mock_db_connection.cursor.return_value
    mock_cursor.description = [('id',), ('nombre',)]
    mock_cursor.fetchall.return_value = [(1, 'Juan')]

    with patch('src.crud_personas.conectar_db', return_value=mock_db_connection):
        listar_personas(nombre="Juan")

        # Verificar que la query contiene LIKE %Juan%
        args, _ = mock_cursor.execute.call_args
        assert "%Juan%" in args[0]


def test_listar_personas_paginacion(mock_db_connection):
    """Test: listar con paginación."""
    mock_cursor = mock_db_connection.cursor.return_value
    mock_cursor.description = [('id',)]
    mock_cursor.fetchall.return_value = [(1,)]

    with patch('src.crud_personas.conectar_db', return_value=mock_db_connection):
        listar_personas(limit=50, offset=100)

        args, _ = mock_cursor.execute.call_args
        # Verificar que la query tiene OFFSET y FETCH
        assert "OFFSET ? ROWS FETCH NEXT ? ROWS ONLY" in args[0]
        # Los últimos dos parámetros deben ser offset y limit
        assert args[1][-2] == 100  # offset
        assert args[1][-1] == 50   # limit


def test_contar_personas(mock_db_connection):
    """Test: contar personas con filtros."""
    mock_cursor = mock_db_connection.cursor.return_value
    mock_cursor.fetchone.return_value = (42,)

    with patch('src.crud_personas.conectar_db', return_value=mock_db_connection):
        count = contar_personas(nombre="Juan", apellido="Pérez")

        assert count == 42
        # Verificar que la query usa COUNT(*)
        args, _ = mock_cursor.execute.call_args
        assert "COUNT(*)" in args[0]


def test_listar_personas_cuil_invalido():
    """Test: error al listar con CUIL inválido."""
    with pytest.raises(ValidacionError):
        listar_personas(cuil="invalido")


# ==============================================
# Tests de integración (requieren DB real)
# ==============================================
@pytest.mark.integration
def test_crear_obtener_eliminar_integracion():
    """
    Test de integración completo (solo se ejecuta con flag --integration).
    Requiere base de datos configurada con .env real.
    """
    from src.database import conectar_db

    # 1. Crear
    try:
        crear_persona("Juan", "Pérez", "99-12345678-9")
    except DuplicadoError:
        pytest.skip("Persona ya existe de test anterior")

    # 2. Obtener
    persona = obtener_persona(1)
    assert persona is not None

    # 3. Actualizar
    actualizar_persona(1, nombre="Juan Carlos")
    actualizado = obtener_persona(1)
    assert actualizado['nombre'] == "Juan Carlos"

    # 4. Eliminar
    eliminar_persona(1)
    eliminado = obtener_persona(1)
    assert eliminado is None
