"""
Módulo de exportación de datos.
Fase 3: Búsqueda y Reportes - Exportación a CSV/XLSX/JSON/PDF.
"""

import csv
import json
from datetime import datetime
from typing import List, Dict, Any, Optional

# Módulos propios
from src.database import DatabaseConnectionError


def exportar_a_csv(
    datos: List[Dict[str, Any]],
    ruta_archivo: str,
    cabeceras: Optional[List[str]] = None,
    delimitador: str = ','
) -> int:
    """
    Exporta datos a archivo CSV.

    Args:
        datos: Lista de diccionarios a exportar.
        ruta_archivo: Ruta de salida del archivo CSV.
        cabeceras: Lista de nombres de columnas (si None, usa keys del primer dict).
        delimitador: Carácter separador (default ',').

    Returns:
        int: Número de filas escritas (sin cabecera).

    Raises:
        IOError: Si no se puede escribir el archivo.
        ValueError: Si datos está vacío y no se pueden determinar cabeceras.
    """
    if not datos:
        raise ValueError("No hay datos para exportar")

    # Determinar cabeceras
    if cabeceras is None:
        cabeceras = list(datos[0].keys())

    try:
        with open(ruta_archivo, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=cabeceras, delimiter=delimitador)
            writer.writeheader()

            for fila in datos:
                # Formatear valores especiales
                fila_formateada = _formatear_fila_csv(fila, cabeceras)
                writer.writerow(fila_formateada)

        return len(datos)

    except Exception as e:
        raise IOError(f"Error al exportar CSV: {e}") from e


def exportar_a_xlsx(
    datos: List[Dict[str, Any]],
    ruta_archivo: str,
    hoja_nombre: str = "Datos",
    cabeceras_personalizadas: Optional[Dict[str, str]] = None
) -> int:
    """
    Exporta datos a archivo Excel (XLSX).

    Args:
        datos: Lista de diccionarios.
        ruta_archivo: Ruta de salida del archivo XLSX.
        hoja_nombre: Nombre de la hoja.
        cabeceras_personalizadas: Mapeo {campo: "Nombre Columna"}.

    Returns:
        int: Número de filas exportadas.

    Raises:
        ImportError: Si pandas no está instalado.
        IOError: Si no se puede escribir el archivo.
    """
    try:
        import pandas as pd
    except ImportError:
        raise ImportError(
            "Pandas es requerido para exportar XLSX. "
            "Instalar con: pip install pandas openpyxl"
        )

    if not datos:
        raise ValueError("No hay datos para exportar")

    # Convertir a DataFrame
    df = pd.DataFrame(datos)

    # Renombrar cabeceras si se proporcionan
    if cabeceras_personalizadas:
        df = df.rename(columns=cabeceras_personalizadas)

    # Formatear columnas de fecha
    for col in df.columns:
        if df[col].dtype == 'datetime64[ns]' or col.lower().endswith('fecha'):
            df[col] = pd.to_datetime(df[col], errors='coerce').dt.strftime('%Y-%m-%d %H:%M:%S')

    try:
        df.to_excel(
            ruta_archivo,
            sheet_name=hoja_nombre,
            index=False,
            engine='openpyxl'
        )
        return len(df)
    except Exception as e:
        raise IOError(f"Error al exportar XLSX: {e}") from e


def exportar_a_json(
    datos: List[Dict[str, Any]],
    ruta_archivo: str,
    indent: int = 2,
    fecha_formato: str = "%Y-%m-%d %H:%M:%S"
) -> int:
    """
    Exporta datos a archivo JSON.

    Args:
        datos: Lista de diccionarios.
        ruta_archivo: Ruta de salida del archivo JSON.
        indent: Indentación (espacios). Usar None para sin indentar.
        fecha_formato: Formato strftime para fechas.

    Returns:
        int: Número de registros exportados.

    Raises:
        IOError: Si no se puede escribir el archivo.
    """
    if not datos:
        raise ValueError("No hay datos para exportar")

    # Serializar fechas
    datos_serializables = []
    for item in datos:
        fila = {}
        for key, value in item.items():
            if isinstance(value, datetime):
                fila[key] = value.strftime(fecha_formato)
            else:
                fila[key] = value
        datos_serializables.append(fila)

    try:
        with open(ruta_archivo, 'w', encoding='utf-8') as f:
            json.dump(datos_serializables, f, indent=indent, ensure_ascii=False)

        return len(datos_serializables)

    except Exception as e:
        raise IOError(f"Error al exportar JSON: {e}") from e


def exportar_a_pdf(
    datos: List[Dict[str, Any]],
    ruta_archivo: str,
    titulo: str = "Reporte",
    incluir_cabecera: bool = True
) -> int:
    """
    Exporta datos a archivo PDF (tabla simple).

    Args:
        datos: Lista de diccionarios.
        ruta_archivo: Ruta de salida del PDF.
        titulo: Título del reporte.
        incluir_cabecera: Si incluir título y fecha.

    Returns:
        int: Número de filas exportadas.

    Raises:
        ImportError: Si reportlab no está instalado.
        IOError: Si no se puede escribir el archivo.
    """
    try:
        from reportlab.lib.pagesizes import letter
        from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
        from reportlab.lib import colors
        from reportlab.lib.styles import getSampleStyleSheet
    except ImportError:
        raise ImportError(
            "ReportLab es requerido para exportar PDF. "
            "Instalar con: pip install reportlab"
        )

    if not datos:
        raise ValueError("No hay datos para exportar")

    try:
        doc = SimpleDocTemplate(ruta_archivo, pagesize=letter)
        styles = getSampleStyleSheet()
        story = []

        # Cabecera
        if incluir_cabecera:
            story.append(Paragraph(titulo, styles['Title']))
            story.append(Paragraph(
                f"Generado: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
                styles['Normal']
            ))
            story.append(Spacer(1, 12))

        # Preparar datos de tabla
        cabeceras = list(datos[0].keys())
        tabla_datos = [cabeceras]

        for fila in datos:
            fila_formateada = []
            for col in cabeceras:
                valor = fila.get(col, '')
                if isinstance(valor, datetime):
                    valor = valor.strftime('%Y-%m-%d %H:%M:%S')
                fila_formateada.append(str(valor))
            tabla_datos.append(fila_formateada)

        # Crear tabla
        tabla = Table(tabla_datos)
        tabla.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))

        story.append(tabla)
        doc.build(story)

        return len(datos)

    except Exception as e:
        raise IOError(f"Error al exportar PDF: {e}") from e


def _formatear_fila_csv(
    fila: Dict[str, Any],
    cabeceras: List[str]
) -> Dict[str, str]:
    """
    Formatea una fila para CSV, convirtiendo datetime a string.

    Args:
        fila: Diccionario original.
        cabeceras: Lista de campos a incluir.

    Returns:
        dict: Fila formateada con valores string.
    """
    resultado = {}
    for campo in cabeceras:
        valor = fila.get(campo, '')
        if isinstance(valor, datetime):
            resultado[campo] = valor.strftime('%Y-%m-%d %H:%M:%S')
        else:
            resultado[campo] = str(valor) if valor is not None else ''
    return resultado


def validar_formato_archivo(ruta_archivo: str, formato: str) -> bool:
    """
    Valida que la extensión del archivo coincida con el formato.

    Args:
        ruta_archivo: Ruta del archivo.
        formato: Formato esperado (csv, xlsx, json, pdf).

    Returns:
        bool: True si la extensión es correcta.

    Raises:
        ValueError: Si la extensión no coincide.
    """
    extension_map = {
        'csv': '.csv',
        'xlsx': '.xlsx',
        'json': '.json',
        'pdf': '.pdf'
    }

    formato = formato.lower()
    if formato not in extension_map:
        raise ValueError(f"Formato no soportado: {formato}")

    esperada = extension_map[formato]
    real = ruta_archivo.lower().rfind(esperada)

    if not ruta_archivo.lower().endswith(esperada):
        raise ValueError(
            f"Extensión incorrecta. Se esperaba '{esperada}' pero es '{ruta_archivo[-4:]}'"
        )

    return True


def obtener_exportador(formato: str):
    """
    Retorna la función exportadora correspondiente al formato.

    Args:
        formato: 'csv', 'xlsx', 'json', 'pdf'.

    Returns:
        function: Función exportadora.

    Raises:
        ValueError: Si el formato no está soportado.
    """
    exportadores = {
        'csv': exportar_a_csv,
        'xlsx': exportar_a_xlsx,
        'json': exportar_a_json,
        'pdf': exportar_a_pdf
    }

    formato = formato.lower()
    if formato not in exportadores:
        raise ValueError(
            f"Formato '{formato}' no soportado. "
            f"Opciones: {list(exportadores.keys())}"
        )

    return exportadores[formato]
