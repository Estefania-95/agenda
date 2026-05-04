"""
Tests unitarios para src/exportadores.py - Fase 3.
Pruebas de exportación a CSV, XLSX, JSON, PDF.
"""

import sys
import os
import csv
import json
import pytest
from datetime import datetime
from unittest.mock import patch, MagicMock, mock_open

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from src.exportadores import (
    exportar_a_csv,
    exportar_a_xlsx,
    exportar_a_json,
    exportar_a_pdf,
    obtener_exportador,
    validar_formato_archivo,
    _formatear_fila_csv
)


@pytest.fixture
def datos_prueba():
    """Datos de ejemplo para exportar."""
    return [
        {
            'id': 1,
            'nombre': 'Juan Pérez',
            'cuil': '20-12345678-9',
            'fecha_registro': datetime(2024, 1, 1, 10, 30, 0)
        },
        {
            'id': 2,
            'nombre': 'María Gómez',
            'cuil': '27-87654321-0',
            'fecha_registro': datetime(2024, 1, 2, 14, 0, 0)
        }
    ]


# ==============================================
# Tests de _formatear_fila_csv
# ==============================================
def test_formatear_fila_csv_datetime():
    """Test: formatea datetime a string."""
    fila = {'fecha': datetime(2024, 1, 1, 10, 30)}
    cabeceras = ['fecha']
    resultado = _formatear_fila_csv(fila, cabeceras)

    assert '2024-01-01 10:30:00' in resultado['fecha']


def test_formatear_fila_csv_varios_campos():
    """Test: formatea múltiples campos."""
    fila = {
        'id': 1,
        'nombre': 'Juan',
        'activo': True
    }
    cabeceras = ['id', 'nombre', 'activo']
    resultado = _formatear_fila_csv(fila, cabeceras)

    assert resultado['id'] == '1'
    assert resultado['nombre'] == 'Juan'
    assert resultado['activo'] == 'True'


# ==============================================
# Tests de exportar_a_csv
# ==============================================
def test_exportar_csv_exito(datos_prueba):
    """Test: exportación CSV exitosa."""
    ruta = "test_export.csv"

    with patch('builtins.open', mock_open()) as mock_file:
        filas = exportar_a_csv(datos_prueba, ruta)

        assert filas == 2
        mock_file.assert_called_once_with(ruta, 'w', newline='', encoding='utf-8')
        # Verificar que se escribió cabecera + 2 filas
        handle = mock_file()
        assert handle.write.call_count > 2


def test_exportar_csv_sin_datos():
    """Test: error al exportar CSV sin datos."""
    with pytest.raises(ValueError, match="No hay datos para exportar"):
        exportar_a_csv([], "vacio.csv")


def test_exportar_csv_cabeceras_personalizadas(datos_prueba):
    """Test: CSV con columnas personalizadas."""
    ruta = "test_custom.csv"
    cabeceras = ['id', 'nombre']  # Solo subconjunto

    with patch('builtins.open', mock_open()):
        # Con menos columnas, DictWriter debe manejar solo cabeceras dadas
        # Esto debería funcionar porque DictWriter escribe campos especificados
        # Solo incluiremos las columnas que existen en ambas listas
        datos_filtrados = []
        for d in datos_prueba:
            datos_filtrados.append({k: d[k] for k in cabeceras if k in d})

        exportar_a_csv(datos_filtrados, ruta, cabeceras=cabeceras)


# ==============================================
# Tests de exportar_a_xlsx
# ==============================================
def test_exportar_xlsx_exito(datos_prueba):
    """Test: exportación XLSX exitosa."""
    with patch('src.exportadores.pandas') as mock_pd:
        mock_df = MagicMock()
        mock_pd.DataFrame.return_value = mock_df
        mock_df.to_excel = MagicMock()

        filas = exportar_a_xlsx(datos_prueba, "test.xlsx")

        assert filas == 2
        mock_pd.DataFrame.assert_called_once_with(datos_prueba)
        mock_df.to_excel.assert_called_once_with(
            "test.xlsx",
            sheet_name="Datos",
            index=False,
            engine='openpyxl'
        )


def test_exportar_xlsx_sin_datos():
    """Test: error al exportar XLSX sin datos."""
    with pytest.raises(ValueError, match="No hay datos para exportar"):
        exportar_a_xlsx([], "vacio.xlsx")


def test_exportar_xlsx_pandas_no_instalado():
    """Test: error cuando pandas no está disponible."""
    with patch.dict('sys.modules', {'pandas': None}):
        with pytest.raises(ImportError, match="Pandas es requerido"):
            exportar_a_xlsx([{'id': 1}], "test.xlsx")


def test_exportar_xlsx_hoja_personalizada(datos_prueba):
    """Test: nombre de hoja personalizado."""
    with patch('src.exportadores.pandas') as mock_pd:
        mock_df = MagicMock()
        mock_pd.DataFrame.return_value = mock_df

        exportar_a_xlsx(datos_prueba, "test.xlsx", hoja_nombre="MiHoja")

        mock_df.to_excel.assert_called_with(
            "test.xlsx",
            sheet_name="MiHoja",
            index=False,
            engine='openpyxl'
        )


# ==============================================
# Tests de exportar_a_json
# ==============================================
def test_exportar_json_exito(datos_prueba, tmp_path):
    """Test: exportación JSON exitosa."""
    archivo = str(tmp_path / "test.json")

    with patch('builtins.open', mock_open()) as mock_file:
        filas = exportar_a_json(datos_prueba, archivo)

        assert filas == 2
        # Verificar que json.dump fue llamado
        mock_file.assert_called()


def test_exportar_json_sin_datos():
    """Test: error JSON sin datos."""
    with pytest.raises(ValueError, match="No hay datos para exportar"):
        exportar_a_json([], "vacio.json")


def test_exportar_json_fechas_serializables(datos_prueba):
    """Test: fechas se convierten a string."""
    archivo = "test_fechas.json"
    with patch('builtins.open', mock_open()) as mock_file:
        with patch('json.dump') as mock_dump:
            exportar_a_json(datos_prueba, archivo, indent=4)

            # Verificar que json.dump recibió datos con fechas formateadas
            args, _ = mock_dump.call_args
            datos_serializados = args[0]
            primer_registro = datos_serializados[0]
            assert 'fecha_registro' in primer_registro
            assert isinstance(primer_registro['fecha_registro'], str)


# ==============================================
# Tests de exportar_a_pdf
# ==============================================
def test_exportar_pdf_exito(datos_prueba):
    """Test: exportación PDF exitosa."""
    with patch('src.exportadores.SimpleDocTemplate') as mock_doc, \
         patch('src.exportadores.Table') as mock_table, \
         patch('src.exportadores.Paragraph') as mock_paragraph:

        mock_doc_instance = MagicMock()
        mock_doc.return_value = mock_doc_instance
        mock_table_instance = MagicMock()
        mock_table.return_value = mock_table_instance

        filas = exportar_a_pdf(datos_prueba, "test.pdf")

        assert filas == 2
        mock_doc_instance.build.assert_called_once()


def test_exportar_pdf_sin_datos():
    """Test: error PDF sin datos."""
    with pytest.raises(ValueError, match="No hay datos para exportar"):
        exportar_a_pdf([], "vacio.pdf")


def test_exportar_pdf_reportlab_no_instalado():
    """Test: error cuando reportlab no está disponible."""
    with patch.dict('sys.modules', {'reportlab': None}):
        with pytest.raises(ImportError, match="ReportLab es requerido"):
            exportar_a_pdf([{'id': 1}], "test.pdf")


# ==============================================
# Tests de obtener_exportador
# ==============================================
def test_obtener_exportador_csv():
    """Test: función exportadora para CSV."""
    func = obtener_exportador('csv')
    assert func == exportar_a_csv


def test_obtener_exportador_xlsx():
    """Test: función exportadora para XLSX."""
    func = obtener_exportador('xlsx')
    assert func == exportar_a_xlsx


def test_obtener_exportador_json():
    """Test: función exportadora para JSON."""
    func = obtener_exportador('json')
    assert func == exportar_a_json


def test_obtener_exportador_pdf():
    """Test: función exportadora para PDF."""
    func = obtener_exportador('pdf')
    assert func == exportar_a_pdf


def test_obtener_exportador_invalido():
    """Test: error con formato no soportado."""
    with pytest.raises(ValueError, match="Formato .* no soportado"):
        obtener_exportador('docx')


# ==============================================
# Tests de validar_formato_archivo
# ==============================================
def test_validar_formato_archivo_csv():
    """Test: validación CSV correcta."""
    assert validar_formato_archivo("data.csv", "csv") is True


def test_validar_formato_archivo_xlsx():
    """Test: validación XLSX correcta."""
    assert validar_formato_archivo("data.xlsx", "xlsx") is True


def test_validar_formato_archivo_json():
    """Test: validación JSON correcta."""
    assert validar_formato_archivo("data.json", "json") is True


def test_validar_formato_archivo_pdf():
    """Test: validación PDF correcta."""
    assert validar_formato_archivo("data.pdf", "pdf") is True


def test_validar_formato_archivo_case_insensitive():
    """Test: validación case-insensitive."""
    assert validar_formato_archivo("data.CSV", "csv") is True
    assert validar_formato_archivo("data.XLSX", "xlsx") is True


def test_validar_formato_archivo_extension_mismatch():
    """Test: error si extensión no coincide."""
    with pytest.raises(ValueError, match="Extensión incorrecta"):
        validar_formato_archivo("data.txt", "csv")


def test_validar_formato_archivo_formato_invalido():
    """Test: error si formato no está en lista."""
    with pytest.raises(ValueError, match="Formato no soportado"):
        validar_formato_archivo("data.docx", "docx")
