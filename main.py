"""
Punto de Entrada Principal - Sistema de Gestión de Agenda.
"""

import sys
import os
from dotenv import load_dotenv

# Asegurar que el directorio 'src' esté en el path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))

# Cargar variables de entorno
load_dotenv()

from src.menu_principal import menu_principal
from src.vistas import mostrar_mensaje, limpiar_pantalla

def check_dependencies():
    """Verifica que las librerías necesarias estén instaladas."""
    try:
        import pyodbc
        import prompt_toolkit
        import rich
        import pandas
        return True
    except ImportError as e:
        print(f"Error: Falta la dependencia '{e.name}'.")
        print("Por favor, ejecuta: pip install -r requirements.txt")
        return False

def main():
    """Inicialización y arranque."""
    if not check_dependencies():
        sys.exit(1)
        
    try:
        menu_principal()
    except KeyboardInterrupt:
        limpiar_pantalla()
        mostrar_mensaje("\nAplicación cerrada por el usuario.", "info")
    except Exception as e:
        mostrar_mensaje(f"\nError crítico de la aplicación: {e}", "error")
        sys.exit(1)

if __name__ == "__main__":
    main()
