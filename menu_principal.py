"""
Punto de entrada alternativo - Sistema de Gestión Modular.
Ejecutar: python menu_principal.py
"""

import sys
import os

# Asegurar que src esté en el path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.menu_principal import BuclePrincipal


def main():
    try:
        BuclePrincipal()
    except KeyboardInterrupt:
        print("\n\nSaliendo...")
        sys.exit(0)
    except Exception as e:
        from src.vistas import print_message
        print_message(f"Error crítico: {e}", "error")
        sys.exit(1)


if __name__ == "__main__":
    main()
