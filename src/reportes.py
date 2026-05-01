"""
Módulo de generación de reportes.
Fase 3: Búsqueda y Reportes - Reportes predefinidos y estadísticas.
"""

from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
from collections import Counter

# Módulos propios
from src.database import conectar_db, DatabaseConnectionError
from src.crud_personas import listar_personas, contar_personas


def reporte_personas_por_fecha(
    fecha_desde: Optional[datetime] = None,
    fecha_hasta: Optional[datetime] = None
) -> Dict[str, Any]:
    """
    Reporte de personas registradas en un rango de fechas.

    Args:
        fecha_desde: Fecha inicio (si es None, usa últimos 30 días).
        fecha_hasta: Fecha fin (si es None, usa fecha actual).

    Returns:
        dict: {
            'total': int,
            'por_dia': list[dict],
            'rango': dict,
            'promedio_diario': float
        }
    """
    # Valores por defecto
    if fecha_hasta is None:
        fecha_hasta = datetime.now()
    if fecha_desde is None:
        fecha_desde = fecha_hasta - timedelta(days=30)

    # Obtener todas las personas en rango
    personas = listar_personas(fecha_desde=fecha_desde, fecha_hasta=fecha_hasta, limit=10000)

    # Agrupar por día
    registros_por_dia = Counter()
    for p in personas:
        fecha = p['fecha_registro']
        # Si es datetime, extraer fecha; si es string/date, convertir
        if isinstance(fecha, datetime):
            dia = fecha.date()
        else:
            dia = fecha
        registros_por_dia[dia] += 1

    # Formatear por_dia
    por_dia = []
    current = fecha_desde.date()
    while current <= fecha_hasta.date():
        por_dia.append({
            'fecha': current.isoformat(),
            'cantidad': registros_por_dia.get(current, 0)
        })
        current += timedelta(days=1)

    total = sum(d['cantidad'] for d in por_dia)

    # Calcular promedio diario
    dias = (fecha_hasta.date() - fecha_desde.date()).days + 1
    promedio_diario = total / dias if dias > 0 else 0

    return {
        'total': total,
        'por_dia': por_dia,
        'rango': {
            'desde': fecha_desde.isoformat(),
            'hasta': fecha_hasta.isoformat(),
            'dias': dias
        },
        'promedio_diario': round(promedio_diario, 2)
    }


def reporte_duplicados_cuil() -> List[Dict[str, Any]]:
    """
    Reporte de CUILs duplicados en la base de datos.

    Returns:
        list[dict]: Para cada CUIL duplicado: {cuil, cantidad, personas: [...]}.
    """
    query = """
        SELECT cuil, COUNT(*) as cantidad
        FROM Personas
        GROUP BY cuil
        HAVING COUNT(*) > 1
        ORDER BY cantidad DESC
    """

    try:
        with conectar_db() as conn:
            cursor = conn.cursor()
            cursor.execute(query)
            rows = cursor.fetchall()

            columns = [column[0] for column in cursor.description]
            duplicados_basicos = [dict(zip(columns, row)) for row in rows]

            # Para cada CUIL duplicado, obtener las personas completas
            resultado = []
            for dup in duplicados_basicos:
                cuil = dup['cuil']
                personas = listar_personas(cuil=cuil)

                # Formatear fechas a string para serialización
                for p in personas:
                    if isinstance(p.get('fecha_registro'), datetime):
                        p['fecha_registro'] = p['fecha_registro'].isoformat()

                resultado.append({
                    'cuil': cuil,
                    'cantidad': dup['cantidad'],
                    'personas': personas
                })

            return resultado

    except Exception as e:
        raise DatabaseConnectionError(f"Error al generar reporte de duplicados: {e}") from e


def reporte_estadisticas_generales() -> Dict[str, Any]:
    """
    Reporte de estadísticas generales de la tabla Personas.

    Returns:
        dict: Varias métricas (total, primeros registros, distribución, etc.).
    """
    # Total de registros
    total = contar_personas()

    if total == 0:
        return {'total': 0, 'mensaje': 'No hay datos para generar estadísticas'}

    # Obtener todas las personas (limitado para no saturar)
    personas = listar_personas(limit=min(total, 10000))

    # Distribución por apellido inicial
    apellidos_iniciales = Counter()
    for p in personas:
        inicial = p['apellido'][0].upper() if p['apellido'] else '?'
        apellidos_iniciales[inicial] += 1

    # Distribución por mes de registro
    registros_por_mes = Counter()
    for p in personas:
        fecha = p['fecha_registro']
        if isinstance(fecha, datetime):
            mes = fecha.strftime('%Y-%m')
        else:
            mes = str(fecha)[:7]  # asumir YYYY-MM
        registros_por_mes[mes] += 1

    # Primera y última persona registrada
    personas_ordenadas = sorted(
        personas,
        key=lambda x: x['fecha_registro'] if isinstance(x['fecha_registro'], datetime) else datetime.fromisoformat(str(x['fecha_registro']))
    )
    primera = personas_ordenadas[0] if personas_ordenadas else None
    ultima = personas_ordenadas[-1] if personas_ordenadas else None

    # Formatear fechas para serialización
    def formatear_persona(p):
        return {
            'id': p['id'],
            'nombre': p['nombre'],
            'apellido': p['apellido'],
            'cuil': p['cuil'],
            'fecha_registro': p['fecha_registro'].isoformat() if isinstance(p['fecha_registro'], datetime) else str(p['fecha_registro'])
        }

    return {
        'total': total,
        'primer_registro': formatear_persona(primera) if primera else None,
        'ultimo_registro': formatear_persona(ultima) if ultima else None,
        'distribucion_apellido_inicial': dict(sorted(apellidos_iniciales.items())),
        'registros_por_mes': dict(sorted(registros_por_mes.items())),
        'top_apellidos': Counter(p['apellido'] for p in personas).most_common(10)
    }


def reporte_resumen_mensual(mes: str, anio: int) -> Dict[str, Any]:
    """
    Reporte resumen para un mes específico.

    Args:
        mes: Número de mes (1-12).
        anio: Año (ej: 2024).

    Returns:
        dict: Estadísticas del mes.
    """
    fecha_inicio = datetime(anio, mes, 1)
    if mes == 12:
        fecha_fin = datetime(anio + 1, 1, 1) - timedelta(seconds=1)
    else:
        fecha_fin = datetime(anio, mes + 1, 1) - timedelta(seconds=1)

    personas_mes = listar_personas(fecha_desde=fecha_inicio, fecha_hasta=fecha_fin, limit=10000)
    total_mes = len(personas_mes)

    # Promedio diario
    dias_mes = (fecha_fin - fecha_inicio).days + 1
    promedio_diario = total_mes / dias_mes if dias_mes > 0 else 0

    return {
        'mes': mes,
        'anio': anio,
        'total_registros': total_mes,
        'promedio_diario': round(promedio_diario, 2),
        'rango': {
            'inicio': fecha_inicio.isoformat(),
            'fin': fecha_fin.isoformat()
        }
    }


def exportar_reporte_csv(
    personas: List[Dict[str, Any]],
    ruta_archivo: str
) -> int:
    """
    Exporta lista de personas a CSV.

    Args:
        personas: Lista de personas (dicts).
        ruta_archivo: Ruta donde guardar el archivo CSV.

    Returns:
        int: Número de filas escritas (sin cabecera).

    Raises:
        IOError: Si no se puede escribir el archivo.
    """
    import csv

    if not personas:
        return 0

    # Cabeceras
    fieldnames = ['id', 'nombre', 'apellido', 'cuil', 'fecha_registro']

    try:
        with open(ruta_archivo, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()

            for persona in personas:
                # Formatear fecha_registro si es datetime
                fila = persona.copy()
                if isinstance(fila.get('fecha_registro'), datetime):
                    fila['fecha_registro'] = fila['fecha_registro'].isoformat()
                writer.writerow(fila)

        return len(personas)

    except Exception as e:
        raise IOError(f"Error al escribir CSV: {e}") from e


def exportar_reporte_xlsx(
    personas: List[Dict[str, Any]],
    ruta_archivo: str,
    hoja_nombre: str = "Personas"
) -> int:
    """
    Exporta lista de personas a XLSX (Excel).

    Args:
        personas: Lista de personas (dicts).
        ruta_archivo: Ruta donde guardar el archivo XLSX.
        hoja_nombre: Nombre de la hoja de cálculo.

    Returns:
        int: Número de filas escritas (sin cabecera).

    Raises:
        ImportError: Si pandas/openpyxl no están instalados.
        IOError: Si no se puede escribir el archivo.
    """
    try:
        import pandas as pd
    except ImportError:
        raise ImportError(
            "Pandas y openpyxl son requeridos para exportar XLSX. "
            "Instalar con: pip install pandas openpyxl"
        )

    if not personas:
        return 0

    # Convertir a DataFrame
    df = pd.DataFrame(personas)

    # Formatear fecha_registro si es datetime
    if 'fecha_registro' in df.columns:
        df['fecha_registro'] = pd.to_datetime(df['fecha_registro']).dt.strftime('%Y-%m-%d %H:%M:%S')

    # Escribir a XLSX
    try:
        df.to_excel(ruta_archivo, sheet_name=hoja_nombre, index=False)
        return len(df)
    except Exception as e:
        raise IOError(f"Error al escribir XLSX: {e}") from e


def generar_reporte_completo(
    tipo: str = "estadisticas",
    **params: Any
) -> Dict[str, Any]:
    """
    Función unificada para generar cualquier tipo de reporte.

    Args:
        tipo: Tipo de reporte - 'estadisticas', 'duplicados', 'mensual', 'fecha'.
        **params: Parámetros específicos del reporte.

    Returns:
        dict: Datos del reporte generado.
    """
    tipos_validos = {
        'estadisticas': reporte_estadisticas_generales,
        'duplicados': reporte_duplicados_cuil,
        'fecha': lambda: reporte_personas_por_fecha(
            params.get('fecha_desde'),
            params.get('fecha_hasta')
        ),
        'mensual': lambda: reporte_resumen_mensual(
            params.get('mes', 1),
            params.get('anio', datetime.now().year)
        )
    }

    if tipo not in tipos_validos:
        raise ValueError(f"Tipo de reporte inválido: {tipo}. Opciones: {list(tipos_validos.keys())}")

    # Ejecutar función del reporte
    if tipo in ('estadisticas', 'duplicados'):
        return tipos_validos[tipo]()
    else:
        return tipos_validos[tipo]()
