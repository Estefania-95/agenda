"""
Módulo de vistas y renderizado - Fase 4.
Maneja la presentación de datos en consola usando Rich.
"""

from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from typing import List, Dict, Any, Optional

console = Console()

def mostrar_encabezado(titulo: str, subtitulo: Optional[str] = None):
    """Muestra un encabezado estilizado."""
    texto = Text(titulo, style="bold cyan")
    if subtitulo:
        texto.append(f"\n{subtitulo}", style="dim white")
    
    console.print(Panel(texto, expand=False, border_style="cyan"))

def mostrar_mensaje(mensaje: str, tipo: str = "info"):
    """Muestra un mensaje con color según el tipo."""
    colores = {
        "info": "blue",
        "exito": "green",
        "error": "bold red",
        "alerta": "yellow"
    }
    color = colores.get(tipo, "white")
    console.print(f"[{color}]{mensaje}[/{color}]")

def mostrar_tabla_personas(personas: List[Dict[str, Any]], titulo: str = "Resultados"):
    """Renderiza una lista de personas en una tabla de Rich."""
    if not personas:
        mostrar_mensaje("No hay resultados para mostrar.", "alerta")
        return

    table = Table(title=titulo, show_header=True, header_style="bold magenta")
    table.add_column("ID", style="dim", width=6)
    table.add_column("Nombre", min_width=20)
    table.add_column("Apellido", min_width=20)
    table.add_column("CUIL", justify="center")
    table.add_column("Fecha Registro", justify="right")

    for p in personas:
        fecha = p.get('fecha_registro')
        fecha_str = fecha.strftime("%Y-%m-%d %H:%M") if hasattr(fecha, 'strftime') else str(fecha)
        
        table.add_row(
            str(p.get('id', '')),
            p.get('nombre', ''),
            p.get('apellido', ''),
            p.get('cuil', ''),
            fecha_str
        )

    console.print(table)

def limpiar_pantalla():
    """Limpia la consola."""
    console.clear()
