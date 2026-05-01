"""
Módulo de formularios para entrada de datos validados.
Fase 4: Menú e Interfaz de Usuario - Formularios CRUD.
"""

from typing import Optional, Dict, Any
from datetime import datetime

# Importar validaciones desde CRUD
from src.crud_personas import validar_nombre_apellido, validar_cuil, ValidacionError

# Importar vistas
from src.vistas import (
    input_text,
    input_cuil,
    confirm,
    print_message,
    clear_screen,
    waiting_key,
    RICH_AVAILABLE
)


def formulario_alta_persona() -> Optional[Dict[str, Any]]:
    """
    Formulario para crear una nueva persona.

    Returns:
        dict | None: Datos de la persona o None si se cancela.
    """
    clear_screen()
    print_header("Alta de Persona", "Complete los datos")

    try:
        nombre = input_text("Nombre", required=True, min_length=2, max_length=100)
        if nombre is None:
            return None

        apellido = input_text("Apellido", required=True, min_length=2, max_length=100)
        if apellido is None:
            return None

        cuil = input_cuil("CUIL (XX-XXXXXXXX-X)")
        if cuil is None:
            return None

        # Confirmación
        print()
        print_message(f"¿Crear persona: {nombre} {apellido}, CUIL: {cuil}?", "info")
        if not confirm("¿Confirma?", default=False):
            print_message("Operación cancelada.", "warning")
            return None

        return {
            'nombre': nombre.strip(),
            'apellido': apellido.strip(),
            'cuil': cuil.strip()
        }

    except KeyboardInterrupt:
        print()
        print_message("Operación cancelada por el usuario.", "warning")
        return None
    except Exception as e:
        print_message(f"Error inesperado: {e}", "error")
        return None


def formulario_busqueda() -> Dict[str, Any]:
    """
    Formulario de búsqueda con múltiples filtros.

    Returns:
        dict: Filtros ingresados.
    """
    clear_screen()
    print_header("Búsqueda de Personas", "Ingrese los criterios (dejar vacío para omitir)")

    filtros = {}

    # Nombre
    nombre = input_text("Nombre (opcional)", required=False)
    if nombre:
        filtros['nombre'] = nombre.strip()

    # Apellido
    apellido = input_text("Apellido (opcional)", required=False)
    if apellido:
        filtros['apellido'] = apellido.strip()

    # CUIL
    cuil = input_text("CUIL exacto (opcional)", required=False)
    if cuil:
        try:
            validar_cuil(cuil)
            filtros['cuil'] = cuil.strip()
        except ValidacionError as e:
            print_message(str(e), "error")
            waiting_key()
            return formulario_busqueda()  # Recursión para reintentar

    # Fechas
    from datetime import datetime
    fecha_desde_str = input_text("Fecha desde (YYYY-MM-DD, opcional)", required=False)
    if fecha_desde_str:
        try:
            filtros['fecha_desde'] = datetime.strptime(fecha_desde_str, '%Y-%m-%d')
        except ValueError:
            print_message("Formato de fecha inválido. Use YYYY-MM-DD", "error")
            waiting_key()
            return formulario_busqueda()

    fecha_hasta_str = input_text("Fecha hasta (YYYY-MM-DD, opcional)", required=False)
    if fecha_hasta_str:
        try:
            filtros['fecha_hasta'] = datetime.strptime(fecha_hasta_str, '%Y-%m-%d')
        except ValueError:
            print_message("Formato de fecha inválido. Use YYYY-MM-DD", "error")
            waiting_key()
            return formulario_busqueda()

    # Paginación
    limit_str = input_text("Límite de resultados (max 1000, default 50)", required=False, default="50")
    try:
        limit = int(limit_str)
        limit = max(1, min(limit, 1000))
        filtros['limit'] = limit
    except ValueError:
        filtros['limit'] = 50

    offset_str = input_text("Offset (desde dónde empezar, default 0)", required=False, default="0")
    try:
        offset = int(offset_str)
        offset = max(0, offset)
        filtros['offset'] = offset
    except ValueError:
        filtros['offset'] = 0

    return filtros


def formulario_modificacion(persona: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """
    Formulario para modificar una persona existente.

    Args:
        persona: Datos actuales de la persona.

    Returns:
        dict | None: Campos a actualizar o None si se cancela.
    """
    clear_screen()
    print_header(f"Modificación - Persona ID {persona['id']}")
    print_message(f"Actual: {persona['nombre']} {persona['apellido']}, CUIL: {persona['cuil']}", "info")
    print()

    cambios = {}

    # Nombre
    nuevo_nombre = input_text(
        f"Nombre (actual: {persona['nombre']}, Enter para mantener)",
        required=False
    )
    if nuevo_nombre:
        try:
            validar_nombre_apellido(nuevo_nombre, "nombre")
            cambios['nombre'] = nuevo_nombre.strip()
        except ValidacionError as e:
            print_message(str(e), "error")
            waiting_key()

    # Apellido
    nuevo_apellido = input_text(
        f"Apellido (actual: {persona['apellido']}, Enter para mantener)",
        required=False
    )
    if nuevo_apellido:
        try:
            validar_nombre_apellido(nuevo_apellido, "apellido")
            cambios['apellido'] = nuevo_apellido.strip()
        except ValidacionError as e:
            print_message(str(e), "error")
            waiting_key()

    # CUIL
    nuevo_cuil = input_text(
        f"CUIL (actual: {persona['cuil']}, Enter para mantener)",
        required=False
    )
    if nuevo_cuil:
        try:
            validar_cuil(nuevo_cuil)
            cambios['cuil'] = nuevo_cuil.strip()
        except ValidacionError as e:
            print_message(str(e), "error")
            waiting_key()

    if not cambios:
        print_message("No se realizaron cambios.", "info")
        waiting_key()
        return None

    # Confirmación
    print()
    print_message("¿Aplicar los siguientes cambios?", "warning")
    for campo, valor in cambios.items():
        print(f"  {campo}: {valor}")

    if not confirm("¿Confirma?", default=False):
        print_message("Operación cancelada.", "warning")
        return None

    return cambios


def formulario_confirmacion_eliminacion(persona: Dict[str, Any]) -> bool:
    """
    Formulario de confirmación para eliminar.

    Args:
        persona: Datos de la persona a eliminar.

    Returns:
        bool: True si se confirma la eliminación.
    """
    clear_screen()
    print_header("Eliminación de Persona", "¡ATENCIÓN! Esta acción no se puede deshacer")

    print_message(f"ID: {persona['id']}", "info")
    print_message(f"Nombre: {persona['nombre']} {persona['apellido']}", "info")
    print_message(f"CUIL: {persona['cuil']}", "info")
    print()

    if not confirm("¿Está SEGURO de eliminar esta persona?", default=False):
        print_message("Operación cancelada.", "warning")
        return False

    # Doble confirmación para operación crítica
    if not confirm("¿ES CRÍTICO? Confirmar nuevamente para eliminar", default=False):
        print_message("Operación cancelada.", "warning")
        return False

    return True


def formulario_exportacion() -> Optional[Dict[str, Any]]:
    """
    Formulario para exportar datos.

    Returns:
        dict | None: Opciones de exportación.
    """
    clear_screen()
    print_header("Exportación de Datos")

    # Formato
    formatos = ['csv', 'xlsx', 'json', 'pdf']
    if RICH_AVAILABLE:
        from rich.prompt import Prompt
        formato = Prompt.ask(
            "Formato",
            choices=formatos,
            default='csv'
        )
    else:
        print("Formatos disponibles:", ", ".join(formatos))
        formato = input("Formato: ").strip().lower()
        if formato not in formatos:
            print_message(f"Formato no válido. Opciones: {', '.join(formatos)}", "error")
            return None

    # Ruta
    import os
    nombre_default = f"personas_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.{formato}"
    ruta = input_text(
        f"Ruta de salida (default: {nombre_default})",
        required=False,
        default=nombre_default
    )
    if not ruta:
        ruta = nombre_default

    # Verificar extensión
    if not ruta.lower().endswith(f'.{formato}'):
        ruta = f"{ruta}.{formato}"

    # Filtros opcionales
    print()
    print_message("¿Desea aplicar filtros antes de exportar?", "info")
    aplicar_filtros = confirm("¿Exportar solo datos filtrados?", default=False)

    filtros = {}
    if aplicar_filtros:
        # Reutilizar lógica simple de búsqueda
        from src.buscador import buscar_personas

        # Pedir filtros básicos
        nombre = input_text("Nombre (opcional)", required=False)
        if nombre:
            filtros['nombre'] = nombre

        apellido = input_text("Apellido (opcional)", required=False)
        if apellido:
            filtros['apellido'] = apellido

        limit = input_text("Límite (max 10000, default 1000)", required=False, default="1000")
        try:
            filtros['limit'] = min(int(limit), 10000)
        except ValueError:
            filtros['limit'] = 1000

    return {
        'formato': formato,
        'ruta': ruta,
        'filtros': filtros
    }
