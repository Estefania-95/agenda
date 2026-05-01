"""
Tests unitarios para src/reportes.py - Fase 3.
Pruebas de generación de reportes y estadísticas.
"""

import sys
import os
from datetime import datetime, timedelta
from unittest.mock import patch, MagicMock

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from src.reportes import (
    reporte_personas_por_fecha,
    reporte_duplicados_cuil,
    reporte_estadisticas_generales,
    reporte_resumen_mensual,
    generar_reporte_completo
)


@pytest.fixture
def mock_personas_mes():
    """Personas de prueba para reportes mensuales."""
    base = datetime(2024, 1, 1)
    return [
        {'id': 1, 'fecha_registro': base + timedelta(days=1)},
        {'id': 2, 'fecha_registro': base + timedelta(days=2)},
        {'id': 3, 'fecha_registro': base + timedelta(days=3)},
    ]


# ==============================================
# Tests de reporte_personas_por_fecha
# ==============================================
def test_reporte_personas_por_fecha_rango_default():
    """Test: reporte sin fechas usa últimos 30 días."""
    with patch('src.reportes.listar_personas') as mock_list:
        # Simular datos: 3 personas en días distintos
        mock_list.return_value = [
            {'fecha_registro': datetime(2024, 1, 1)},
            {'fecha_registro': datetime(2024, 1, 1)},
            {'fecha_registro': datetime(2024, 1, 3)},
        ]

        resultado = reporte_personas_por_fecha()

        assert resultado['total'] == 3
        assert len(resultado['por_dia']) <= 31  # Max 31 días
        assert 'promedio_diario' in resultado
        assert resultado['promedio_diario'] > 0


def test_reporte_personas_por_fecha_rango_personalizado():
    """Test: reporte con fechas específicas."""
    with patch('src.reportes.listar_personas') as mock_list:
        fi = datetime(2024, 1, 1)
        ff = datetime(2024, 1, 5)
        mock_list.return_value = [
            {'fecha_registro': fi + timedelta(days=1)},
            {'fecha_registro': ff - timedelta(days=1)},
        ]

        resultado = reporte_personas_por_fecha(fecha_desde=fi, fecha_hasta=ff)

        assert resultado['total'] == 2
        assert len(resultado['por_dia']) == 5  # 1-5 enero
        assert resultado['rango']['desde'] == fi.isoformat()
        assert resultado['rango']['hasta'] == ff.isoformat()


def test_reporte_personas_por_fecha_sin_datos():
    """Test: reporte con rango pero sin datos."""
    with patch('src.reportes.listar_personas', return_value=[]):
        resultado = reporte_personas_por_fecha()

        assert resultado['total'] == 0
        assert resultado['promedio_diario'] == 0.0


# ==============================================
# Tests de reporte_duplicados_cuil
# ==============================================
def test_reporte_duplicados_cuil_con_duplicados(mock_personas_mes):
    """Test: detecta y detalla CUILs duplicados."""
    duplicados = [
        {
            'cuil': '20-12345678-9',
            'cantidad': 2,
            'personas': [
                {'id': 1, 'cuil': '20-12345678-9', 'nombre': 'Juan', 'apellido': 'Pérez'},
                {'id': 2, 'cuil': '20-12345678-9', 'nombre': 'Juan', 'apellido': 'Otro'}
            ]
        }
    ]

    with patch('src.reportes.listar_personas', side_effect=lambda cuil=None, **kw: [
        {'id': 1, 'cuil': '20-12345678-9', 'nombre': 'Juan', 'apellido': 'Pérez'},
        {'id': 2, 'cuil': '20-12345678-9', 'nombre': 'Juan', 'apellido': 'Otro'}
    ] if cuil else []), \
         patch('src.reportes.conectar_db') as mock_conn:

        mock_cursor = MagicMock()
        mock_cursor.fetchall.return_value = [('20-12345678-9', 2)]
        mock_cursor.description = [('cuil',), ('cantidad',)]
        mock_conn.return_value.cursor.return_value = mock_cursor

        resultado = reporte_duplicados_cuil()

        assert len(resultado) == 1
        assert resultado[0]['cantidad'] == 2


def test_reporte_duplicados_cuil_sin_duplicados():
    """Test: sin duplicados devuelve lista vacía."""
    with patch('src.reportes.conectar_db') as mock_conn:
        mock_cursor = MagicMock()
        mock_cursor.fetchall.return_value = []
        mock_conn.return_value.cursor.return_value = mock_cursor

        resultado = reporte_duplicados_cuil()
        assert resultado == []


# ==============================================
# Tests de reporte_estadisticas_generales
# ==============================================
def test_reporte_estadisticas_con_datos(mock_personas_mes):
    """Test: estadísticas con datos."""
    with patch('src.reportes.listar_personas', return_value=mock_personas_mes), \
         patch('src.reportes.contar_personas', return_value=3):
        stats = reporte_estadisticas_generales()

        assert stats['total'] == 3
        assert 'primer_registro' in stats
        assert 'ultimo_registro' in stats
        assert 'distribucion_apellido_inicial' in stats
        assert 'top_apellidos' in stats


def test_reporte_estadisticas_sin_datos():
    """Test: estadísticas sin datos."""
    with patch('src.reportes.contar_personas', return_value=0):
        stats = reporte_estadisticas_generales()

        assert stats['total'] == 0
        assert 'mensaje' in stats


# ==============================================
# Tests de reporte_resumen_mensual
# ==============================================
def test_reporte_resumen_mensual(mock_personas_mes):
    """Test: resumen de un mes."""
    with patch('src.reportes.listar_personas', return_value=mock_personas_mes):
        resumen = reporte_resumen_mensual(mes=1, anio=2024)

        assert resumen['mes'] == 1
        assert resumen['anio'] == 2024
        assert resumen['total_registros'] == 3
        assert resumen['promedio_diario'] > 0
        assert 'rango' in resumen


def test_reporte_resumen_mensual_febrero_bisiesto():
    """Test: febrero en año bisiesto."""
    # 2024 es bisiesto, febrero tiene 29 días
    with patch('src.reportes.listar_personas', return_value=[]):
        resumen = reporte_resumen_mensual(mes=2, anio=2024)

        assert resumen['total_registros'] == 0
        assert resumen['rango']['inicio'] == '2024-02-01T00:00:00'
        assert '2024-02-29' in resumen['rango']['fin']


# ==============================================
# Tests de generar_reporte_completo
# ==============================================
def test_generar_reporte_completo_estadisticas():
    """Test: generador unificado de reportes."""
    with patch('src.reportes.reporte_estadisticas_generales') as mock_stats:
        mock_stats.return_value = {'total': 100}
        resultado = generar_reporte_completo(tipo='estadisticas')
        assert resultado['total'] == 100
        mock_stats.assert_called_once()


def test_generar_reporte_completo_invalido():
    """Test: tipo de reporte no reconocido."""
    with pytest.raises(ValueError) as exc:
        generar_reporte_completo(tipo='inexistente')

    assert "Tipo de reporte inválido" in str(exc.value)
    assert "estadisticas" in str(exc.value) or "duplicados" in str(exc.value)
