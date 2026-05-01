# Instalación y Pruebas - Fase 2 CRUD

## Prerrequisitos

- [x] Fase 1 completada (BD creada y conexión verificada)
- Archivo `.env` configurado con credenciales reales
- Paquete `pyodbc` y `python-dotenv` instalados

## Instalación

```bash
# 1. Activar entorno virtual (si existe)
# Windows:
venv\Scripts\Activate.ps1
# Linux/Mac:
source venv/bin/activate

# 2. Instalar dependencias de desarrollo
pip install -e ".[dev]"

# 3. Verificar instalación
python -c "import pyodbc; print('pyodbc OK')"
python -c "import dotenv; print('dotenv OK')"
```

## Estructura de Archivos Fase 2

```
agenda/
├── src/
│   ├── __init__.py
│   ├── database.py        (Fase 1)
│   └── crud_personas.py   (Fase 2 - NUEVO)
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   ├── test_database.py   (Fase 1)
│   └── test_crud_personas.py (Fase 2 - NUEVO)
├── fase2_crud_core/
│   ├── spec.md
│   └── progress.md
└── logs/
```

## Tests Unitarios

### Ejecutar todos los tests

```bash
# Tests unitarios normales (sin DB)
pytest tests/ -v

# Con cobertura
pytest tests/ --cov=src --cov-report=html

# Tests de integración ( requieren DB real )
pytest tests/ -v --integration
```

### Tests individuales

```bash
# Solo tests de CRUD
pytest tests/test_crud_personas.py -v

# Solo tests de database
pytest tests/test_database.py -v

# Un test específico
pytest tests/test_crud_personas.py::test_crear_persona_exito -v
```

## Pruebas Manuales

### 1. Probar conexión (Fase 1)

```bash
python src/database.py
```

Esperado: `"¡Conexión exitosa!"`

### 2. Probar CRUD desde REPL

```bash
python
```

```python
from src.crud_personas import crear_persona, obtener_persona, listar_personas

# Crear
crear_persona("Juan", "Pérez", "20-12345678-9")

# Listar
personas = listar_personas()
print(f"Total: {len(personas)}")
for p in personas:
    print(f"  {p['id']}: {p['nombre']} {p['apellido']}")

# Obtener
p = obtener_persona(1)
print(p)
```

## Validaciones Implementadas

| Campo | Regla | Ejemplo Válido | Ejemplo Inválido |
|-------|-------|---------------|------------------|
| CUIL | Formato XX-XXXXXXXX-X | `20-12345678-9` | `20123456789` (sin guiones) |
| Nombre | 2-100 chars, solo letras | `María` | `Juan123`, ` ` (vacío) |
| Apellido | 2-100 chars, solo letras | `González` | `Maria@`, `  ` (espacios) |

## Excepciones

- `ValidacionError` - Datos de entrada inválidos
- `DuplicadoError` - CUIL duplicado (violación UNIQUE)
- `DatabaseConnectionError` - Errores de conexión/consulta

## Logging

Los logs operacionales se guardan en `logs/operaciones.log`:

```
2026-04-30 23:50:12 - src.crud_personas - INFO - Persona creada: Juan Pérez, CUIL: 20-12345678-9
2026-04-30 23:50:15 - src.crud_personas - ERROR - Error DB al crear persona: ...
```

## Troubleshooting Fase 2

### Error: "ModuleNotFoundError: No module named 'src'"
- Verificar que `src/__init__.py` existe
- Ejecutar tests desde la raíz del proyecto

### Error: "logs/ directorio no existe"
- `mkdir logs` o dejar que lo cree automáticamente el logger

### DUPLICATE error en CUIL
- El CUIL ya existe en la BD, usar otro

### Validación de CUIL falla
- Verificar formato: 2 dígitos, guión, 8 dígitos, guión, 1 dígito

## Siguiente Paso

Una vez que los tests pasen y las validaciones funcionen, avanzar a **Fase 3: Búsqueda y Reportes**.
