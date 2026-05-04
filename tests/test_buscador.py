"""
Tests unitarios para src/buscador.py - Fase 3.
Pruebas de búsquedas avanzadas y filtros.
"""

import sys
import os
import pytest
from datetime import datetime
from unittest.mock import patch, MagicMock

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from src.buscador import (
    buscar_personas,
    buscar_por_cuil,
    buscar_por_nombre,
    buscar_por_fecha,
    busqueda_avanzada,
    buscar_duplicados_cuil,
    sugerir_busqueda
)
from src.crud_personas import listar_personas, contar_personas


@pytest.fixture
def mock_personas_data():
    """Datos de prueba de personas."""
    return [
        {
            'id': 1,
            'nombre': 'Juan',
            'apellido': 'Pérez',
            'cuil': '20-12345678-9',
            'fecha_registro': datetime(2024, 1, 1, 10, 30)
        },
        {
            'id': 2,
            'nombre': 'María',
            'apellido': 'Gómez',
            'cuil': '27-87654321-0',
            'fecha_registro': datetime(2024, 1, 2, 14, 0)
        },
        {
            'id': 3,
            'nombre': 'Juan Carlos',
            'apellido': 'Rodríguez',
            'cuil': '20-23456789-1',
            'fecha_registro': datetime(2024, 1, 3, 9, 15)
        }
    ]


@pytest.fixture
def mock_db_crud(mock_personas_data):
    """Mock de las funciones de CRUD."""
    with patch('src.buscador.listar_personas', return_value=mock_personas_data), \
         patch('src.buscador.contar_personas', return_value=3):
        yield


# ==============================================
# Tests de buscar_personas
# ==============================================
def test_buscar_personas_sin_filtros(mock_db_crud, mock_personas_data):
    """Test: búsqueda sin filtros devuelve todos."""
    resultado = buscar_personas()

    assert resultado['total'] == 3
    assert len(resultado['resultados']) == 3
    assert resultado['has_more'] is False
    assert resultado['pagina_actual'] == 1
    assert resultado['total_paginas'] == 1


def test_buscar_personas_con_filtro_nombre(mock_db_crud):
    """Test: búsqueda con filtro nombre."""
    with patch('src.buscador.listar_personas') as mock_list, \
         patch('src.buscador.contar_personas') as mock_count:
        mock_list.return_value = [{'id': 1, 'nombre': 'Juan'}]
        mock_count.return_value = 1

        resultado = buscar_personas(nombre="Juan")

        assert resultado['total'] == 1
        # Verificar que listar_personas recibió el filtro correctamente
        _, kwargs = mock_list.call_args
        assert kwargs['nombre'] == "Juan"


def test_buscar_personas_paginacion(mock_db_crud):
    """Test: paginación con limit/offset."""
    with patch('src.buscador.listar_personas') as mock_list, \
         patch('src.buscador.contar_personas') as mock_count:
        mock_list.return_value = [{'id': 2}]
        mock_count.return_value = 50

        resultado = buscar_personas(limit=10, offset=20)

        assert resultado['limit'] == 10
        assert resultado['offset'] == 20
        assert resultado['pagina_actual'] == 3  # (20//10)+1
        assert resultado['total_paginas'] == 5
        assert resultado['has_more'] is True


def test_buscar_personas_limite_maximo():
    """Test: limite se restringe a 1000."""
    with patch('src.buscador.listar_personas') as mock_list, \
         patch('src.buscador.contar_personas'):
        mock_list.return_value = []

        resultado = buscar_personas(limit=9999)

        assert resultado['limit'] == 1000  # Capado


# ==============================================
# Tests de buscar_por_cuil
# ==============================================
def test_buscar_por_cuil_existente(mock_personas_data):
    """Test: CUIL encontrado."""
    with patch('src.buscador.listar_personas', return_value=[mock_personas_data[0]]):
        resultado = buscar_por_cuil("20-12345678-9")
        assert resultado is not None
        assert resultado['id'] == 1


def test_buscar_por_cuil_no_existente():
    """Test: CUIL no encontrado."""
    with patch('src.buscador.listar_personas', return_value=[]):
        resultado = buscar_por_cuil("99-99999999-9")
        assert resultado is None


# ==============================================
# Tests de buscar_por_nombre
# ==============================================
def test_buscar_por_nombre_exacto(mock_personas_data):
    """Test: búsqueda exacta por nombre."""
    with patch('src.buscador.listar_personas', return_value=mock_personas_data):
        resultados = buscar_por_nombre("Juan", exacto=True)

        # Debe encontrar "Juan" y "Juan Carlos" (nombre exacto "Juan")
        assert len(resultados) >= 1
        nombres = [r['nombre'].lower() for r in resultados]
        assert any('juan' == n for n in nombres) or any('juan carlos' == n for n in nombres)


def test_buscar_por_nombre_apellido_combinado(mock_personas_data):
    """Test: búsqueda por nombre y apellido."""
    with patch('src.buscador.listar_personas', return_value=[mock_personas_data[0]]):
        resultados = buscar_por_nombre("Juan", apellido="Pérez")

        assert len(resultados) == 1
        assert resultados[0]['apellido'] == 'Pérez'


# ==============================================
# Tests de busqueda_avanzada
# ==============================================
def test_busqueda_avanzada_nombre(mock_personas_data):
    """Test: búsqueda avanzada por nombre."""
    with patch('src.buscador.listar_personas', return_value=mock_personas_data):
        resultados = busqueda_avanzada("Juan", buscar_en="nombre")

        assert len(resultados) == 2  # Juan y Juan Carlos


def test_busqueda_avanzada_cuil(mock_personas_data):
    """Test: búsqueda avanzada por CUIL."""
    with patch('src.buscador.listar_personas', return_value=[mock_personas_data[0]]):
        resultados = busqueda_avanzada("20-12345678-9", buscar_en="cuil")

        assert len(resultados) == 1
        assert resultados[0]['cuil'] == '20-12345678-9'


def test_busqueda_avanzada_vacia():
    """Test: término vacío devuelve lista vacía."""
    resultados = busqueda_avanzada("   ")
    assert resultados == []


def test_busqueda_avanzada_ambos(mock_personas_data):
    """Test: búsqueda en nombre y apellido."""
    with patch('src.buscador.listar_personas', side_effect=[
        [mock_personas_data[0]],  # nombre=Juan
        [mock_personas_data[1]]   # apellido distinto
    ]):
        resultados = busqueda_avanzada("Juan", buscar_en="ambos")

        # Debería tener 2 resultados únicos
        assert len(resultados) == 2


# ==============================================
# Tests de buscar_duplicados_cuil
# ==============================================
def test_buscar_duplicados_cuil_con_duplicados():
    """Test: detecta CUILs duplicados."""
    # Simular resultado de query de duplicados
    duplicados = [
        {'cuil': '20-12345678-9', 'cantidad': 2}
    ]

    mock_personas_duplicadas = [
        {'id': 1, 'cuil': '20-12345678-9', 'nombre': 'Juan', 'apellido': 'Pérez'},
        {'id': 4, 'cuil': '20-12345678-9', 'nombre': 'Juan', 'apellido': 'Otro'}
    ]

    with patch('src.buscador.conectar_db') as mock_conn, \
         patch('src.buscador.listar_personas', return_value=mock_personas_duplicadas):

        mock_cursor = MagicMock()
        mock_cursor.fetchall.return_value = [('20-12345678-9', 2)]
        mock_cursor.description = [('cuil',), ('cantidad',)]
        mock_conn.return_value.cursor.return_value = mock_cursor

        resultados = buscar_duplicados_cuil()

        assert len(resultados) == 1
        assert resultados[0]['cantidad'] == 2
        assert len(resultados[0]['personas']) == 2


def test_buscar_duplicados_cuil_sin_duplicados():
    """Test: sin duplicados devuelve lista vacía."""
    with patch('src.buscador.conectar_db') as mock_conn:
        mock_cursor = MagicMock()
        mock_cursor.fetchall.return_value = []  # Sin duplicados
        mock_cursor.description = [('cuil',), ('cantidad',)]
        mock_conn.return_value.cursor.return_value = mock_cursor

        resultados = buscar_duplicados_cuil()
        assert resultados == []


# ==============================================
# Tests de sugerir_busqueda
# ==============================================
def test_sugerir_busqueda_corta():
    """Test: término muy corto devuelve vacío."""
    sugerencias = sugerir_busqueda("a")
    assert sugerencias == []


def test_sugerir_busqueda_con_resultados():
    """Test: sugerencias con coincidencias."""
    sugerencias_esperadas = ["Juan Pérez", "Juan Carlos"]

    with patch('src.buscador.conectar_db') as mock_conn:
        mock_cursor = MagicMock()
        mock_cursor.fetchall.return_value = [
            ('Juan', 'Pérez'),
            ('Juan', 'Carlos')
        ]
        mock_conn.return_value.cursor.return_value = mock_cursor

        sugerencias = sugerir_busqueda("Juan")

        assert len(sugerencias) == 2
        assert "Juan Pérez" in sugerencias


# ==============================================
# Tests de buscar_por_fecha
# ==============================================
def test_buscar_por_fecha_rango(mock_personas_data):
    """Test: búsqueda por rango de fechas."""
    with patch('src.buscador.buscar_personas') as mock_buscar:
        mock_buscar.return_value = {
            'resultados': [mock_personas_data[0]],
            'total': 1
        }

        resultado = buscar_por_fecha(
            fecha_desde=datetime(2024, 1, 1),
            fecha_hasta=datetime(2024, 1, 31)
        )

        assert resultado['total'] == 1
        # Verificar que se llamó a buscar_personas con filtros de fecha
        args, kwargs = mock_buscar.call_args
        assert 'fecha_desde' in kwargs
        assert 'fecha_hasta' in kwargs
