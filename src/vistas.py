"""
Módulo de vistas para interfaz CLI.
Fase 4: Menú e Interfaz de Usuario - Renderizado de tablas y pantallas.
"""

from typing import List, Dict, Any, Optional
from datetime import datetime

try:
    from rich.console import Console
    from rich.table import Table
    from rich.panel import Panel
    from rich.progress import Progress, SpinnerColumn, TextColumn
    from rich.prompt import Prompt, Confirm
    from rich import box
    RICH_AVAILABLE = True
except ImportError:
    RICH_AVAILABLE = False
    print("Advertencia: 'rich' no instalado. Ejecutar: pip install rich")

# Consola global
console = Console()

# Exportar símbolos públicos
__all__ = [
    'clear_screen',
    'print_header',
    'print_menu',
    'print_table',
    'print_message',
    'confirm',
    'input_text',
    'input_cuil',
    'mostrar_loading',
    'paginar_resultados',
    'waiting_key',
    'console',
    'RICH_AVAILABLE'
]


def clear_screen():
    """Limpia la pantalla de la consola."""
    import os
    os.system('cls' if os.name == 'nt' else 'clear')


def print_header(title: str, subtitle: Optional[str] = None):
    """
    Imprime un encabezado con estilo.

    Args:
        title: Título principal.
        subtitle: Subtítulo opcional.
    """
    if RICH_AVAILABLE:
        console.print()
        console.print(f"[bold cyan]{title}[/bold cyan]")
        if subtitle:
            console.print(f"[dim]{subtitle}[/dim]")
        console.print()
    else:
        print()
        print(f"=== {title} ===")
        if subtitle:
            print(subtitle)
        print()


def print_menu(options: List[Dict[str, Any]], title: str = "Menú") -> int:
    """
    Imprime un menú numerado y retorna la opción seleccionada.

    Args:
        options: Lista de opciones, cada una con 'key' y 'label'.
        title: Título del menú.

    Returns:
        int: Índice de la opción seleccionada (0-based).
    """
    if RICH_AVAILABLE:
        console.print(f"[bold yellow]{title}[/bold yellow]")
        console.print()
        for i, opt in enumerate(options, 1):
            console.print(f"  [green]{i}[/green]. {opt['label']}")
        console.print()
        while True:
            resp = Prompt.ask("Seleccione una opción", choices=[str(i) for i in range(1, len(options)+1)])
            return int(resp) - 1
    else:
        print(f"\n{title}")
        print("-" * len(title))
        for i, opt in enumerate(options, 1):
            print(f"  {i}. {opt['label']}")
        print()
        while True:
            resp = input("Seleccione una opción: ").strip()
            if resp.isdigit() and 1 <= int(resp) <= len(options):
                return int(resp) - 1
            print("Opción inválida.")


def print_table(
    data: List[Dict[str, Any]],
    columns: List[Dict[str, str]],
    title: Optional[str] = None
):
    """
    Imprime una tabla formateada.

    Args:
        data: Lista de filas (dicts).
        columns: Lista de columnas con 'key' y 'header'.
        title: Título opcional de la tabla.
    """
    if not data:
        if RICH_AVAILABLE:
            console.print("[yellow]No hay datos para mostrar.[/yellow]")
        else:
            print("No hay datos para mostrar.")
        return

    if RICH_AVAILABLE:
        table = Table(title=title, box=box.ROUNDED, show_header=True, header_style="bold magenta")

        for col in columns:
            table.add_column(col['header'], justify=col.get('justify', 'left'), style=col.get('style', ''))

        for row in data:
            valores = []
            for col in columns:
                key = col['key']
                valor = row.get(key, '')
                # Formatear fechas
                if isinstance(valor, datetime):
                    valor = valor.strftime('%Y-%m-%d %H:%M')
                valores.append(str(valor))
            table.add_row(*valores)

        console.print(table)
    else:
        # Fallback simple
        headers = [c['header'] for c in columns]
        print("\t".join(headers))
        print("-" * 80)
        for row in data:
            valores = [str(row.get(c['key'], '')) for c in columns]
            print("\t".join(valores))


def print_message(text: str, style: str = "info"):
    """
    Imprime un mensaje con estilo.

    Args:
        text: Mensaje a imprimir.
        style: Estilo: 'info', 'success', 'warning', 'error'.
    """
    styles = {
        'info': '[blue]ℹ[/blue]',
        'success': '[green]✔[/green]',
        'warning': '[yellow]⚠[/yellow]',
        'error': '[red]✖[/red]'
    }

    prefix = styles.get(style, '')

    if RICH_AVAILABLE:
        console.print(f"{prefix} {text}", style=style)
    else:
        print(f"{prefix} {text}")


def confirm(message: str, default: bool = False) -> bool:
    """
    Pide confirmación al usuario.

    Args:
        message: Mensaje de confirmación.
        default: Valor por defecto.

    Returns:
        bool: True si el usuario confirma.
    """
    if RICH_AVAILABLE:
        return Confirm.ask(message, default=default)
    else:
        resp = input(f"{message} (s/N): ").strip().lower()
        return resp in ('s', 'si', 'y', 'yes')


def input_text(
    prompt: str,
    default: Optional[str] = None,
    required: bool = True,
    min_length: int = 2,
    max_length: int = 100
) -> str:
    """
    Solicita entrada de texto con validación.

    Args:
        prompt: Mensaje para el usuario.
        default: Valor por defecto.
        required: Si es obligatorio.
        min_length: Longitud mínima.
        max_length: Longitud máxima.

    Returns:
        str: Valor ingresado.
    """
    while True:
        if RICH_AVAILABLE:
            valor = Prompt.ask(prompt, default=default)
        else:
            valor = input(f"{prompt}: ").strip()
            if default and not valor:
                valor = default

        if required and not valor:
            print_message("Este campo es obligatorio.", "warning")
            continue

        if valor and (len(valor) < min_length or len(valor) > max_length):
            print_message(f"Longitud incorrecta: {min_length}-{max_length} caracteres.", "warning")
            continue

        return valor


def input_cuil(prompt: str = "CUIL") -> str:
    """
    Solicita un CUIL con formato válido.

    Args:
        prompt: Mensaje para el usuario.

    Returns:
        str: CUIL formateado (XX-XXXXXXXX-X).
    """
    import re
    patron = r'^\d{2}-\d{8}-\d{1}$'

    while True:
        valor = input_text(prompt, required=True)

        if re.match(patron, valor):
            return valor
        else:
            print_message("Formato inválido. Use XX-XXXXXXXX-X (ej: 20-12345678-9)", "error")


def mostrar_loading(mensaje: str = "Procesando..."):
    """
    Context manager para mostrar animación de carga.

    Usage:
        with mostrar_loading("Guardando..."):
            operacion_larga()
    """
    if RICH_AVAILABLE:
        return Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
            transient=True
        )
    else:
        # Fallback simple
        class DummyProgress:
            def __enter__(self):
                print(mensaje)
                return self
            def __exit__(self, *args):
                pass
            def add_task(self, *args, **kwargs):
                pass
            def update(self, *args, **kwargs):
                pass
        return DummyProgress()


def paginar_resultados(
    data: List[Dict[str, Any]],
    page_size: int = 10,
    columns: Optional[List[Dict[str, str]]] = None
):
    """
    Muestra resultados paginados.

    Args:
        data: Lista completa de datos.
        page_size: Elementos por página.
        columns: Columnas para mostrar en tabla.
    """
    total = len(data)
    total_pages = (total + page_size - 1) // page_size

    if total == 0:
        print_message("No hay resultados.", "info")
        return

    page = 0
    while True:
        start = page * page_size
        end = min(start + page_size, total)
        pagina_data = data[start:end]

        clear_screen()
        print_header(f"Resultados - Página {page + 1} de {total_pages}")

        # Columnas por defecto si no se especifican
        if columns is None:
            columns = [
                {'key': 'id', 'header': 'ID'},
                {'key': 'nombre', 'header': 'Nombre'},
                {'key': 'apellido', 'header': 'Apellido'},
                {'key': 'cuil', 'header': 'CUIL'}
            ]

        print_table(pagina_data, columns)

        print()
        print(f"Mostrando {start + 1}-{end} de {total}")

        # Opciones de navegación
        opciones = []
        if page > 0:
            opciones.append({'key': 'prev', 'label': '← Página anterior'})
        if end < total:
            opciones.append({'key': 'next', 'label': 'Página siguiente →'})
        opciones.append({'key': 'back', 'label': 'Volver al menú'})

        if RICH_AVAILABLE:
            console.print()
            for opt in opciones:
                console.print(f"  [green]{opt['key']}[/green]. {opt['label']}")
            console.print()
            resp = Prompt.ask("Opción", choices=[o['key'] for o in opciones])
        else:
            print()
            for i, opt in enumerate(opciones, 1):
                print(f"  {i}. {opt['label']}")
            while True:
                resp = input("Opción: ").strip().lower()
                if resp in [o['key'] for o in opciones]:
                    break
                if resp.isdigit() and 1 <= int(resp) <= len(opciones):
                    resp = opciones[int(resp)-1]['key']
                    break

        if resp == 'prev':
            page -= 1
        elif resp == 'next':
            page += 1
        elif resp == 'back':
            break


def waiting_key(message: str = "Presione una tecla para continuar..."):
    """Espera a que el usuario presione una tecla."""
    if RICH_AVAILABLE:
        console.input(message)
    else:
        input(message)
