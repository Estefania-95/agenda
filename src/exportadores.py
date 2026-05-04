"""
Módulo de exportación de datos.
Fase 3: Búsqueda y Reportes - Exportación a CSV/XLSX/JSON/PDF.
"""

import csv
import json
import sys
from datetime import datetime
from typing import List, Dict, Any, Optional

# Módulos propios
from src.database import DatabaseConnectionError

# Placeholders para permitir patching en tests (sin importar librerías pesadas al cargar el módulo)
pandas = None  # será un módulo cuando esté disponible
SimpleDocTemplate = None
Table = None
TableStyle = None
Paragraph = None
Spacer = None
letter = None
colors = None
getSampleStyleSheet = None


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
    global pandas
    # Si el import está explícitamente “cortado” (tests), debe fallar aunque
    # hayamos cacheado el módulo antes.
    if sys.modules.get('pandas', object()) is None:
        raise ImportError(
            "Pandas es requerido para exportar XLSX. "
            "Instalar con: pip install pandas openpyxl"
        )
    if pandas is None:
        try:
            # Lazy import para soportar entornos sin pandas.
            import pandas as pd  # type: ignore
            pandas = pd
        except Exception:
            raise ImportError(
                "Pandas es requerido para exportar XLSX. "
                "Instalar con: pip install pandas openpyxl"
            )

    if not datos:
        raise ValueError("No hay datos para exportar")

    # Convertir a DataFrame
    df = pandas.DataFrame(datos)  # type: ignore[union-attr]

    # Renombrar cabeceras si se proporcionan
    if cabeceras_personalizadas:
        df = df.rename(columns=cabeceras_personalizadas)

    # Formatear columnas de fecha
    for col in df.columns:
        if df[col].dtype == 'datetime64[ns]' or col.lower().endswith('fecha'):
            df[col] = pandas.to_datetime(df[col], errors='coerce').dt.strftime('%Y-%m-%d %H:%M:%S')  # type: ignore[union-attr]

    try:
        df.to_excel(
            ruta_archivo,
            sheet_name=hoja_nombre,
            index=False,
            engine='openpyxl'
        )
        return len(datos)
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
    global SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, letter, colors, getSampleStyleSheet
    if sys.modules.get('reportlab', object()) is None:
        raise ImportError(
            "ReportLab es requerido para exportar PDF. "
            "Instalar con: pip install reportlab"
        )
    if SimpleDocTemplate is None or Table is None or Paragraph is None:
        try:
            # Lazy import para soportar entornos sin reportlab.
            from reportlab.lib.pagesizes import letter as _letter
            from reportlab.platypus import SimpleDocTemplate as _SimpleDocTemplate, Table as _Table, TableStyle as _TableStyle, Paragraph as _Paragraph, Spacer as _Spacer
            from reportlab.lib import colors as _colors
            from reportlab.lib.styles import getSampleStyleSheet as _getSampleStyleSheet

            letter = _letter
            SimpleDocTemplate = _SimpleDocTemplate
            Table = _Table
            TableStyle = _TableStyle
            Paragraph = _Paragraph
            Spacer = _Spacer
            colors = _colors
            getSampleStyleSheet = _getSampleStyleSheet
        except ImportError:
            raise ImportError(
                "ReportLab es requerido para exportar PDF. "
                "Instalar con: pip install reportlab"
            )

    if not datos:
        raise ValueError("No hay datos para exportar")

    try:
        doc = SimpleDocTemplate(ruta_archivo, pagesize=letter)  # type: ignore[misc]
        if getSampleStyleSheet is not None:
            styles = getSampleStyleSheet()  # type: ignore[misc]
        else:
            # En tests se parchea Paragraph; no necesitamos estilos reales.
            styles = {'Title': None, 'Normal': None}
        story = []

        # Cabecera
        if incluir_cabecera:
            story.append(Paragraph(titulo, styles['Title']))
            story.append(Paragraph(
                f"Generado: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
                styles['Normal']
            ))
            if Spacer is not None:
                story.append(Spacer(1, 12))  # type: ignore[misc]

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
        tabla = Table(tabla_datos)  # type: ignore[misc]
        # En tests se parchea Table/TableStyle y a veces no se provee `colors`.
        if TableStyle is not None and colors is not None:
            tabla.setStyle(TableStyle([  # type: ignore[misc]
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),  # type: ignore[union-attr]
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),  # type: ignore[union-attr]
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 12),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),  # type: ignore[union-attr]
                ('GRID', (0, 0), (-1, -1), 1, colors.black)  # type: ignore[union-attr]
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
