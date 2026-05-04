"""
Módulo del Menú Principal - Fase 4.
Controlador principal de la interfaz CLI.
"""

import sys
from prompt_toolkit.shortcuts import radiolist_dialog, message_dialog, input_dialog
from prompt_toolkit.styles import Style

# Módulos propios
from src.vistas import mostrar_encabezado, mostrar_mensaje, mostrar_tabla_personas, limpiar_pantalla
from src.formularios import solicitar_datos_persona, confirmar_accion
from src.crud_personas import (
    crear_persona, 
    obtener_persona, 
    actualizar_persona, 
    eliminar_persona,
    ValidacionError,
    DuplicadoError
)
from src.buscador import buscar_personas, busqueda_avanzada
from src.reportes import reporte_estadisticas_generales
from src.exportadores import exportar_a_csv, exportar_a_xlsx, exportar_a_json, exportar_a_pdf

# Estilo personalizado para prompt_toolkit
style = Style.from_dict({
    'dialog': 'bg:#2b2b2b',
    'dialog.body': 'bg:#2b2b2b #ffffff',
    'dialog shadow': 'bg:#000000',
    'frame.label': '#00ffff bold',
    'radiolist.current': '#ff00ff bold',
})

def menu_principal():
    """Bucle principal de la aplicación CLI."""
    while True:
        limpiar_pantalla()
        mostrar_encabezado("SISTEMA DE GESTIÓN MODULAR", "Agenda de Personas - SQL Server")
        
        opcion = radiolist_dialog(
            title="Menú Principal",
            text="Seleccione una operación:",
            values=[
                ('1', '1. Alta de Persona'),
                ('2', '2. Listar / Buscar Personas'),
                ('3', '3. Modificar Persona'),
                ('4', '4. Baja de Persona'),
                ('5', '5. Reportes Estadísticos'),
                ('6', '6. Exportar Datos'),
                ('0', '0. Salir')
            ],
            style=style
        ).run()

        if opcion == '1':
            pantalla_alta()
        elif opcion == '2':
            pantalla_busqueda()
        elif opcion == '3':
            pantalla_modificacion()
        elif opcion == '4':
            pantalla_baja()
        elif opcion == '5':
            pantalla_reportes()
        elif opcion == '6':
            pantalla_exportacion()
        elif opcion == '0' or opcion is None:
            if confirmar_accion("¿Está seguro que desea salir?"):
                break

def pantalla_alta():
    """Pantalla para crear una nueva persona."""
    limpiar_pantalla()
    mostrar_encabezado("ALTA DE PERSONA")
    
    datos = solicitar_datos_persona()
    if datos:
        try:
            if crear_persona(**datos):
                mostrar_mensaje(f"Persona '{datos['nombre']} {datos['apellido']}' creada con éxito.", "exito")
            else:
                mostrar_mensaje("No se pudo crear la persona.", "error")
        except (ValidacionError, DuplicadoError) as e:
            mostrar_mensaje(str(e), "error")
        except Exception as e:
            mostrar_mensaje(f"Error inesperado: {e}", "error")
    
    input("\nPresione Enter para continuar...")

def pantalla_busqueda():
    """Pantalla para listar y buscar personas."""
    limpiar_pantalla()
    mostrar_encabezado("LISTADO Y BÚSQUEDA")
    
    termino = input("Término de búsqueda (deje vacío para ver todos): ").strip()
    
    try:
        if termino:
            resultados = busqueda_avanzada(termino)
            total = len(resultados)
        else:
            resp = buscar_personas(limit=50)
            resultados = resp['resultados']
            total = resp['total']
        
        mostrar_tabla_personas(resultados, titulo=f"Resultados ({total})")
    except Exception as e:
        mostrar_mensaje(f"Error al buscar: {e}", "error")
    
    input("\nPresione Enter para continuar...")

def pantalla_modificacion():
    """Pantalla para editar una persona."""
    limpiar_pantalla()
    mostrar_encabezado("MODIFICACIÓN DE PERSONA")
    
    persona_id_str = input("Ingrese el ID de la persona a modificar: ").strip()
    if not persona_id_str.isdigit():
        mostrar_mensaje("ID inválido.", "error")
    else:
        persona_id = int(persona_id_str)
        persona = obtener_persona(persona_id)
        
        if persona:
            mostrar_tabla_personas([persona], "Datos Actuales")
            nuevos_datos = solicitar_datos_persona(persona)
            
            if nuevos_datos:
                try:
                    if actualizar_persona(persona_id, **nuevos_datos):
                        mostrar_mensaje("Persona actualizada con éxito.", "exito")
                    else:
                        mostrar_mensaje("No se realizaron cambios.", "alerta")
                except Exception as e:
                    mostrar_mensaje(str(e), "error")
        else:
            mostrar_mensaje(f"No se encontró persona con ID {persona_id}", "error")
            
    input("\nPresione Enter para continuar...")

def pantalla_baja():
    """Pantalla para eliminar una persona."""
    limpiar_pantalla()
    mostrar_encabezado("BAJA DE PERSONA")
    
    persona_id_str = input("Ingrese el ID de la persona a eliminar: ").strip()
    if persona_id_str.isdigit():
        persona_id = int(persona_id_str)
        persona = obtener_persona(persona_id)
        
        if persona:
            mostrar_tabla_personas([persona], "Persona a Eliminar")
            if confirmar_accion(f"¿Realmente desea eliminar a {persona['nombre']}?"):
                try:
                    if eliminar_persona(persona_id):
                        mostrar_mensaje("Persona eliminada.", "exito")
                except Exception as e:
                    mostrar_mensaje(str(e), "error")
        else:
            mostrar_mensaje("No se encontró la persona.", "error")
    
    input("\nPresione Enter para continuar...")

def pantalla_reportes():
    """Muestra estadísticas generales."""
    limpiar_pantalla()
    mostrar_encabezado("REPORTES ESTADÍSTICOS")
    
    try:
        stats = reporte_estadisticas_generales()
        console_print = lambda m: mostrar_mensaje(m, "info")
        
        console_print(f"Total de registros: {stats['total']}")
        console_print(f"Primer registro: {stats['primer_registro']}")
        console_print(f"Último registro: {stats['ultimo_registro']}")
        
        if stats['top_apellidos']:
            mostrar_mensaje("\nTop 5 Apellidos comunes:", "alerta")
            for ap, cant in stats['top_apellidos'][:5]:
                console_print(f" - {ap}: {cant}")
                
    except Exception as e:
        mostrar_mensaje(f"Error al generar reporte: {e}", "error")
        
    input("\nPresione Enter para continuar...")

def pantalla_exportacion():
    """Pantalla para exportar datos a archivos."""
    limpiar_pantalla()
    mostrar_encabezado("EXPORTAR DATOS")
    
    formato = radiolist_dialog(
        title="Exportar",
        text="Seleccione el formato:",
        values=[
            ('csv', 'CSV (Texto plano)'),
            ('xlsx', 'Excel (XLSX)'),
            ('json', 'JSON'),
            ('pdf', 'PDF (Tabular)'),
            ('cancel', 'Cancelar')
        ],
        style=style
    ).run()
    
    if formato and formato != 'cancel':
        try:
            resp = buscar_personas(limit=1000)
            datos = resp['resultados']
            filename = f"exportacion_agenda.{formato}"
            
            if formato == 'csv':
                exportar_a_csv(datos, filename)
            elif formato == 'xlsx':
                exportar_a_xlsx(datos, filename)
            elif formato == 'json':
                exportar_a_json(datos, filename)
            elif formato == 'pdf':
                exportar_a_pdf(datos, filename, titulo="Exportación de Agenda")
                
            mostrar_mensaje(f"Datos exportados exitosamente a '{filename}'", "exito")
        except Exception as e:
            mostrar_mensaje(f"Error al exportar: {e}", "error")
            
    input("\nPresione Enter para continuar...")

if __name__ == "__main__":
    menu_principal()
