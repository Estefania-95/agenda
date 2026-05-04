"""
Script para ejecutar la suite completa de pruebas y verificar cobertura.
"""

import subprocess
import sys
import os

def run_tests():
    """Ejecuta pytest con cobertura."""
    print("--- EJECUTANDO SUITE DE PRUEBAS ---")
    
    # Comprobar si estamos en venv
    python_exe = sys.executable
    
    cmd = [
        python_exe, "-m", "pytest", 
        "tests/", 
        "--cov=src", 
        "--cov-report=term-missing",
        "-v"
    ]
    
    try:
        result = subprocess.run(cmd, check=True)
        print("\n[OK] Todos los tests pasaron exitosamente.")
        return True
    except subprocess.CalledProcessError:
        print("\n[ERROR] Algunos tests fallaron.")
        return False
    except Exception as e:
        print(f"\n[ERROR] No se pudo ejecutar pytest: {e}")
        return False

if __name__ == "__main__":
    if run_tests():
        sys.exit(0)
    else:
        sys.exit(1)
