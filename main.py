"""
Punto de entrada principal - Sistema de Gestión Modular.
Fase 4: Menú e Interfaz de Usuario - CLI.

Ejecutar: python -m src.main o python main.py
"""

import sys
import os

# Asegurar que el directorio raíz esté en sys.path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Importar el bucle principal desde src.menu_principal
from src.menu_principal import BuclePrincipal


def main():
    """
    Función principal que inicia la aplicación.
    Maneja excepciones globales y limpieza.
    """
    try:
        BuclePrincipal()
    except KeyboardInterrupt:
        print("\n\nSaliendo...")
        sys.exit(0)
    except Exception as e:
        from src.vistas import print_message, RICH_AVAILABLE
        if RICH_AVAILABLE:
            print_message(f"Error crítico: {e}", "error")
        else:
            print(f"ERROR: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
