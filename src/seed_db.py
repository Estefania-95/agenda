"""
Script de Carga de Datos (Seeding) - Fase 3 Validation.
Genera datos aleatorios para probar búsquedas y reportes.
"""

import random
from datetime import datetime, timedelta
from src.crud_personas import crear_persona, DuplicadoError

NOMBRES = ["Juan", "María", "Carlos", "Ana", "Pedro", "Lucía", "Diego", "Elena", "Luis", "Sonia"]
APELLIDOS = ["Gómez", "Pérez", "Rodríguez", "López", "García", "Martínez", "Sánchez", "Fernández", "Díaz", "Álvarez"]

def generar_cuil():
    """Genera un CUIL aleatorio válido XX-XXXXXXXX-X."""
    prefijo = random.choice(["20", "27", "23", "24"])
    dni = "".join([str(random.randint(0, 9)) for _ in range(8)])
    digito = str(random.randint(0, 9))
    return f"{prefijo}-{dni}-{digito}"

def seed(cantidad: int = 20):
    """Inserta N personas aleatorias en la base de datos."""
    print(f"Iniciando carga de {cantidad} registros...")
    exitos = 0
    duplicados = 0
    errores = 0

    for i in range(cantidad):
        nombre = random.choice(NOMBRES)
        if random.random() > 0.5:
            nombre += " " + random.choice(NOMBRES)
            
        apellido = random.choice(APELLIDOS)
        cuil = generar_cuil()

        try:
            if crear_persona(nombre, apellido, cuil):
                exitos += 1
                if exitos % 5 == 0:
                    print(f"[OK] {exitos} registros insertados...")
        except DuplicadoError:
            duplicados += 1
        except Exception as e:
            print(f"[ERROR] No se pudo insertar a {nombre} {apellido}: {e}")
            errores += 1

    print("\n--- RESUMEN DE CARGA ---")
    print(f"Éxitos: {exitos}")
    print(f"Duplicados omitidos: {duplicados}")
    print(f"Errores: {errores}")
    print("------------------------")

if __name__ == "__main__":
    # Puedes ajustar la cantidad aquí
    seed(30)
