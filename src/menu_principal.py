"""
Módulo de menú principal e interfaz de usuario.
Fase 4: Menú e Interfaz de Usuario - Loop principal y controladores.
"""

import sys
from typing import Optional

# Módulos propios
from src.vistas import (
    clear_screen,
    print_header,
    print_menu,
    print_message,
    confirm,
    waiting_key,
    paginar_resultados
)
from src.formularios import (
    formulario_alta_persona,
    formulario_busqueda,
    formulario_modificacion,
    formulario_confirmacion_eliminacion,
    formulario_exportacion
)
from src.crud_personas import (
    crear_persona,
    obtener_persona,
    actualizar_persona,
    eliminar_persona
)
from src.buscador import buscar_personas, buscar_por_cuil
from src.reportes import (
    reporte_personas_por_fecha,
    reporte_duplicados_cuil,
    reporte_estadisticas_generales,
    generar_reporte_completo
)
from src.exportadores import exportar_a_csv, exportar_a_xlsx, exportar_a_json, exportar_a_pdf


# Definición del menú principal
MENU_PRINCIPAL = [
    {'key': 'alta', 'label': '1. Alta de Persona'},
    {'key': 'buscar', 'label': '2. Búsqueda de Personas'},
    {'key': 'modificar', 'label': '3. Modificación de Persona'},
    {'key': 'eliminar', 'label': '4. Baja de Persona'},
    {'key': 'reportes', 'label': '5. Reportes'},
    {'key': 'exportar', 'label': '6. Exportar Datos'},
    {'key': 'salir', 'label': '0. Salir'}
]


def PantallaAlta() -> None:
    """Controlador de pantalla de alta de persona."""
    datos = formulario_alta_persona()
    if datos:
        try:
            if crear_persona(**datos):
                print_message("Persona creada exitosamente.", "success")
            else:
                print_message("No se pudo crear la persona.", "error")
        except Exception as e:
            print_message(f"Error al crear: {e}", "error")
    waiting_key()


def PantallaBusqueda() -> None:
    """Controlador de pantalla de búsqueda."""
    filtros = formulario_busqueda()
    if not filtros:
        return

    try:
        resultado = buscar_personas(**filtros)

        if resultado['total'] == 0:
            print_message("No se encontraron personas.", "info")
            waiting_key()
            return

        # Mostrar resultados paginados
        columnas = [
            {'key': 'id', 'header': 'ID'},
            {'key': 'nombre', 'header': 'Nombre'},
            {'key': 'apellido', 'header': 'Apellido'},
            {'key': 'cuil', 'header': 'CUIL'},
            {'key': 'fecha_registro', 'header': 'Fecha Registro'}
        ]

        paginar_resultados(resultado['resultados'], columns=columnas)

    except Exception as e:
        print_message(f"Error en búsqueda: {e}", "error")
        waiting_key()


def PantallaModificacion() -> None:
    """Controlador de pantalla de modificación."""
    # Primero buscar persona a modificar
    print_header("Modificación - Buscar Persona")

    # Búsqueda por ID o CUIL
    criterio = input("Ingrese ID o CUIL de la persona: ").strip()
    if not criterio:
        return

    persona = None

    # Intentar por ID
    if criterio.isdigit():
        persona = obtener_persona(int(criterio))

    # Si no se encuentra, intentar por CUIL
    if not persona:
        from src.crud_personas import listar_personas
        try:
            resultados = listar_personas(cuil=criterio)
            if resultados:
                persona = resultados[0]
        except Exception:
            pass

    if not persona:
        print_message("Persona no encontrada.", "error")
        waiting_key()
        return

    # Mostrar datos actuales
    print()
    print_message(f"Encontrada: {persona['nombre']} {persona['apellido']}, CUIL: {persona['cuil']}", "info")

    # Formulario de modificación
    cambios = formulario_modificacion(persona)
    if cambios:
        try:
            if actualizar_persona(persona['id'], **cambios):
                print_message("Persona actualizada exitosamente.", "success")
            else:
                print_message("No se pudo actualizar (ID no encontrado).", "error")
        except Exception as e:
            print_message(f"Error al actualizar: {e}", "error")

    waiting_key()


def PantallaEliminacion() -> None:
    """Controlador de pantalla de eliminación."""
    print_header("Eliminación - Buscar Persona")

    criterio = input("Ingrese ID o CUIL de la persona: ").strip()
    if not criterio:
        return

    persona = None

    if criterio.isdigit():
        persona = obtener_persona(int(criterio))

    if not persona:
        from src.crud_personas import listar_personas
        try:
            resultados = listar_personas(cuil=criterio)
            if resultados:
                persona = resultados[0]
        except Exception:
            pass

    if not persona:
        print_message("Persona no encontrada.", "error")
        waiting_key()
        return

    # Confirmación
    if formulario_confirmacion_eliminacion(persona):
        try:
            if eliminar_persona(persona['id']):
                print_message("Persona eliminada exitosamente.", "success")
            else:
                print_message("No se pudo eliminar (quizás ya fue eliminada).", "warning")
        except Exception as e:
            print_message(f"Error al eliminar: {e}", "error")

    waiting_key()


def PantallaReportes() -> None:
    """Controlador de pantalla de reportes."""
    while True:
        clear_screen()
        print_header("Reportes")

        opciones_reportes = [
            {'key': 'stats', 'label': '1. Estadísticas Generales'},
            {'key': 'fecha', 'label': '2. Personas por Rango de Fechas'},
            {'key': 'duplicados', 'label': '3. Detectar DUPLICADOS de CUIL'},
            {'key': 'mensual', 'label': '4. Resumen Mensual'},
            {'key': 'back', 'label': '0. Volver al menú principal'}
        ]

        idx = print_menu(opciones_reportes, "Seleccione un reporte")
        opcion = opciones_reportes[idx]['key']

        if opcion == 'back':
            break

        try:
            if opcion == 'stats':
                stats = reporte_estadisticas_generales()
                clear_screen()
                print_header("Estadísticas Generales")
                _mostrar_estadisticas(stats)

            elif opcion == 'fecha':
                clear_screen()
                print_header("Reporte por Fechas")
                print_message("Deje vacío para usar últimos 30 días", "info")
                from datetime import datetime, timedelta
                fecha_desde_str = input("Fecha desde (YYYY-MM-DD): ").strip()
                fecha_hasta_str = input("Fecha hasta (YYYY-MM-DD): ").strip()

                fecha_desde = None
                fecha_hasta = None

                if fecha_desde_str:
                    try:
                        fecha_desde = datetime.strptime(fecha_desde_str, '%Y-%m-%d')
                    except ValueError:
                        print_message("Fecha desde inválida.", "error")
                        waiting_key()
                        continue

                if fecha_hasta_str:
                    try:
                        fecha_hasta = datetime.strptime(fecha_hasta_str, '%Y-%m-%d')
                    except ValueError:
                        print_message("Fecha hasta inválida.", "error")
                        waiting_key()
                        continue

                reporte = reporte_personas_por_fecha(fecha_desde, fecha_hasta)
                _mostrar_reporte_fecha(reporte)

            elif opcion == 'duplicados':
                duplicados = reporte_duplicados_cuil()
                clear_screen()
                print_header("CUILs Duplicados")
                _mostrar_duplicados(duplicados)

            elif opcion == 'mensual':
                clear_screen()
                print_header("Resumen Mensual")
                mes_str = input("Mes (1-12): ").strip()
                anio_str = input("Año (ej: 2024): ").strip()

                try:
                    mes = int(mes_str)
                    anio = int(anio_str)
                    resumen = reporte_resumen_mensual(mes, anio)
                    _mostrar_resumen_mensual(resumen)
                except ValueError:
                    print_message("Mes o año inválido.", "error")

        except Exception as e:
            print_message(f"Error al generar reporte: {e}", "error")

        waiting_key()


def _mostrar_estadisticas(stats: Dict[str, Any]) -> None:
    """Muestra estadísticas generales."""
    from src.vistas import print_table

    print_message(f"Total de personas: {stats['total']}", "info")

    if stats['total'] > 0:
        columnas = [
            {'key': 'letra', 'header': 'Inicial'},
            {'key': 'cantidad', 'header': 'Cantidad'}
        ]
        data = [
            {'letra': k, 'cantidad': v}
            for k, v in stats['distribucion_apellido_inicial'].items()
        ]
        print_table(data, columnas, title="Distribución por Inicial de Apellido")

        print()
        print_message("Top 10 Apellidos:", "info")
        for apellido, cant in stats['top_apellidos']:
            print(f"  {apellido}: {cant}")

    waiting_key()


def _mostrar_reporte_fecha(reporte: Dict[str, Any]) -> None:
    """Muestra reporte por fechas."""
    from src.vistas import print_table

    print_message(f"Total: {reporte['total']} personas", "info")
    print_message(f"Promedio diario: {reporte['promedio_diario']}", "info")

    data = [
        {'fecha': d['fecha'], 'cantidad': d['cantidad']}
        for d in reporte['por_dia']
    ]
    columnas = [
        {'key': 'fecha', 'header': 'Fecha'},
        {'key': 'cantidad', 'header': 'Registros', 'justify': 'right'}
    ]
    print_table(data, columnas, title="Registros por Día")

    waiting_key()


def _mostrar_duplicados(duplicados: list) -> None:
    """Muestra CUILs duplicados."""
    if not duplicados:
        print_message("No hay CUILs duplicados.", "success")
        waiting_key()
        return

    print_message(f"Se encontraron {len(duplicados)} CUIL(s) duplicado(s).", "warning")

    for dup in duplicados:
        print()
        print_message(f"CUIL: {dup['cuil']} ({dup['cantidad']} veces)", "error")
        for persona in dup['personas']:
            print(f"  - ID {persona['id']}: {persona['nombre']} {persona['apellido']}")

    waiting_key()


def _mostrar_resumen_mensual(resumen: Dict[str, Any]) -> None:
    """Muestra resumen mensual."""
    print_message(f"Mes: {resumen['mes']}, Año: {resumen['anio']}", "info")
    print_message(f"Total registrados: {resumen['total_registros']}", "info")
    print_message(f"Promedio diario: {resumen['promedio_diario']}", "info")
    waiting_key()


def PantallaExportacion() -> None:
    """Controlador de pantalla de exportación."""
    opciones = formulario_exportacion()
    if not opciones:
        return

    try:
        # Obtener datos según filtros
        from src.buscador import buscar_personas
        filtros = opciones.get('filtros', {})
        resultado = buscar_personas(**filtros)
        datos = resultado['resultados']

        if not datos:
            print_message("No hay datos para exportar.", "warning")
            waiting_key()
            return

        # Exportar según formato
        formato = opciones['formato']
        ruta = opciones['ruta']

        exportadores = {
            'csv': exportar_a_csv,
            'xlsx': exportar_a_xlsx,
            'json': exportar_a_json,
            'pdf': exportar_a_pdf
        }

        exportador = exportadores[formato]
        filas = exportador(datos, ruta)

        print_message(f"Exportación completada: {filas} filas a '{ruta}'", "success")

    except ImportError as e:
        print_message(f"Falta dependencia: {e}", "error")
        print_message("Instale las librerías necesarias (pandas, reportlab, etc.)", "info")
    except Exception as e:
        print_message(f"Error al exportar: {e}", "error")

    waiting_key()


def BuclePrincipal() -> None:
    """
    Bucle principal del menú.

    Maneja la navegación entre pantallas hasta que el usuario salga.
    """
    while True:
        clear_screen()
        print_header("Sistema de Gestión Modular", "SQL Server + Python")

        idx = print_menu(MENU_PRINCIPAL, "Menú Principal")
        opcion = MENU_PRINCIPAL[idx]['key']

        if opcion == 'salir':
            clear_screen()
            print_message("¡Hasta luego!", "info")
            break

        # Dispatch a pantallas correspondientes
        try:
            if opcion == 'alta':
                PantallaAlta()
            elif opcion == 'buscar':
                PantallaBusqueda()
            elif opcion == 'modificar':
                PantallaModificacion()
            elif opcion == 'eliminar':
                PantallaEliminacion()
            elif opcion == 'reportes':
                PantallaReportes()
            elif opcion == 'exportar':
                PantallaExportacion()
        except KeyboardInterrupt:
            print_message("\nOperación interrumpida.", "warning")
            waiting_key()
        except Exception as e:
            print_message(f"Error inesperado: {e}", "error")
            waiting_key()


if __name__ == "__main__":
    try:
        BuclePrincipal()
    except KeyboardInterrupt:
        print("\nSaliendo...")
        sys.exit(0)
