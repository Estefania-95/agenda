"""
Módulo de búsqueda avanzada de personas.
Fase 3: Búsqueda y Reportes - Funciones de filtrado.
"""

from datetime import datetime
from typing import Optional, List, Dict, Any

# Módulos propios
from src.database import conectar_db, DatabaseConnectionError
from src.crud_personas import listar_personas, contar_personas

# Re-exportar funciones principales para compatibilidad
__all__ = [
    'buscar_personas',
    'buscar_por_cuil',
    'buscar_por_nombre',
    'buscar_por_fecha',
    'busqueda_avanzada'
]


def buscar_personas(
    nombre: Optional[str] = None,
    apellido: Optional[str] = None,
    cuil: Optional[str] = None,
    fecha_desde: Optional[datetime] = None,
    fecha_hasta: Optional[datetime] = None,
    limit: int = 100,
    offset: int = 0
) -> Dict[str, Any]:
    """
    Búsqueda avanzada con filtros múltiples y paginación.

    Args:
        nombre: Filtrar por nombre (LIKE).
        apellido: Filtrar por apellido (LIKE).
        cuil: Filtrar por CUIL exacto.
        fecha_desde: Fecha de registro desde (inclusive).
        fecha_hasta: Fecha de registro hasta (inclusive).
        limit: Máximo de resultados (default 100, max 1000).
        offset: Desplazamiento para paginación.

    Returns:
        dict: {
            'resultados': list[dict],
            'total': int,
            'limit': int,
            'offset': int,
            'has_more': bool
        }
    """
    # Validar límite
    limit = min(max(limit, 1), 1000)

    # Obtener resultados
    resultados = listar_personas(
        nombre=nombre,
        apellido=apellido,
        cuil=cuil,
        fecha_desde=fecha_desde,
        fecha_hasta=fecha_hasta,
        limit=limit,
        offset=offset
    )

    # Contar total (sin paginación)
    total = contar_personas(
        nombre=nombre,
        apellido=apellido,
        cuil=cuil
    )

    # Calcular si hay más páginas
    has_more = (offset + limit) < total

    return {
        'resultados': resultados,
        'total': total,
        'limit': limit,
        'offset': offset,
        'has_more': has_more,
        'pagina_actual': (offset // limit) + 1,
        'total_paginas': (total + limit - 1) // limit
    }


def buscar_por_cuil(cuil: str) -> Optional[Dict[str, Any]]:
    """
    Búsqueda exacta por CUIL. Retorna una persona o None.

    Args:
        cuil: CUIL a buscar (formato XX-XXXXXXXX-X).

    Returns:
        dict | None: Persona encontrada o None.
    """
    resultados = listar_personas(cuil=cuil, limit=1)
    return resultados[0] if resultados else None


def buscar_por_nombre(
    nombre: str,
    apellido: Optional[str] = None,
    exacto: bool = False
) -> List[Dict[str, Any]]:
    """
    Búsqueda por nombre (y opcionalmente apellido).

    Args:
        nombre: Nombre a buscar.
        apellido: Apellido opcional para filtrar.
        exacto: Si True, busca coincidencia exacta; si False, usa LIKE.

    Returns:
        list[dict]: Lista de personas encontradas.
    """
    if exacto:
        # Búsqueda exacta (sin comodines LIKE)
        lista = listar_personas(nombre=nombre, apellido=apellido, limit=1000)
        # Filtrar manualmente por coincidencia exacta (case-insensitive)
        nombre_lower = nombre.strip().lower()
        return [
            p for p in lista
            if p['nombre'].strip().lower() == nombre_lower
            and (not apellido or p['apellido'].strip().lower() == apellido.strip().lower())
        ]
    else:
        # Búsqueda con LIKE (comodines)
        return listar_personas(nombre=nombre, apellido=apellido, limit=1000)


def buscar_por_fecha(
    fecha_desde: datetime,
    fecha_hasta: datetime,
    limit: int = 100,
    offset: int = 0
) -> Dict[str, Any]:
    """
    Búsqueda por rango de fecha de registro.

    Args:
        fecha_desde: Fecha inicio (inclusive).
        fecha_hasta: Fecha fin (inclusive).
        limit: Límite de resultados.
        offset: Desplazamiento.

    Returns:
        dict: Resultados paginados similar a buscar_personas().
    """
    return buscar_personas(
        fecha_desde=fecha_desde,
        fecha_hasta=fecha_hasta,
        limit=limit,
        offset=offset
    )


def busqueda_avanzada(
    termino: str,
    buscar_en: str = "ambos"
) -> List[Dict[str, Any]]:
    """
    Búsqueda unificada por término en nombre, apellido o CUIL.

    Args:
        termino: Término a buscar.
        buscar_en: Dónde buscar - 'nombre', 'apellido', 'cuil', 'ambos'.

    Returns:
        list[dict]: Lista de coincidencias.
    """
    termino = termino.strip()

    if not termino:
        return []

    resultados = []
    limit = 1000  # Para búsqueda general, traer muchos

    if buscar_en in ('nombre', 'ambos'):
        resultados.extend(listar_personas(nombre=termino, limit=limit))

    if buscar_en in ('apellido', 'ambos'):
        # Si ya hay resultados de nombre, evitar duplicados
        ids_existentes = {r['id'] for r in resultados}
        por_apellido = listar_personas(apellido=termino, limit=limit)
        resultados.extend([p for p in por_apellido if p['id'] not in ids_existentes])

    if buscar_en == 'cuil':
        # Búsqueda exacta por CUIL (permite formato con/sin guiones)
        cuil_limpio = termino.replace('-', '')
        if len(cuil_limpio) == 11:
            # Formatear a XX-XXXXXXXX-X
            cuil_formateado = f"{cuil_limpio[:2]}-{cuil_limpio[2:-1]}-{cuil_limpio[-1]}"
            por_cuil = listar_personas(cuil=cuil_formateado, limit=10)
            if por_cuil:
                return por_cuil

    return resultados


def buscar_duplicados_cuil() -> List[Dict[str, Any]]:
    """
    Detecta CUILs duplicados en la base de datos (más de una persona con mismo CUIL).

    Returns:
        list[dict]: Lista de CUILs duplicados con conteo.
    """
    query = """
        SELECT cuil, COUNT(*) as cantidad, MIN(fecha_registro) as primero_registro
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
            return [dict(zip(columns, row)) for row in rows]

    except Exception as e:
        raise DatabaseConnectionError(f"Error al buscar duplicados: {e}") from e


def sugerir_busqueda(termino: str) -> List[str]:
    """
    Sugiere términos de búsqueda basados en datos existentes.

    Args:
        termino: Término parcial ingresado por usuario.

    Returns:
        list[str]: Lista de sugerencias (nombres/apellidos que contienen el término).
    """
    if len(termino) < 2:
        return []

    termino_like = f"%{termino}%"

    query = """
        SELECT DISTINCT TOP 10 nombre, apellido
        FROM Personas
        WHERE nombre LIKE ? OR apellido LIKE ?
        ORDER BY nombre, apellido
    """

    try:
        with conectar_db() as conn:
            cursor = conn.cursor()
            cursor.execute(query, (termino_like, termino_like))
            rows = cursor.fetchall()

            sugerencias = []
            for nombre, apellido in rows:
                sugerencias.append(f"{nombre} {apellido}")

            return sugerencias

    except Exception as e:
        raise DatabaseConnectionError(f"Error al generar sugerencias: {e}") from e
