# Instalación y Pruebas - Fase 3: Búsqueda y Reportes

## Prerrequisitos

- [x] Fase 1 completada (BD creada y conexión verificada)
- [x] Fase 2 completada (CRUD funcionando)
- Archivo `.env` configurado con credenciales reales
- Dependencias instaladas: `pyodbc`, `python-dotenv`, `pytest`

## Instalación de Dependencias Adicionales

```bash
# Instalar pandas y openpyxl (para XLSX)
pip install pandas openpyxl

# Para exportación a PDF
pip install reportlab

# O instalar todo con extras
pip install -e ".[all]"
```

## Estructura de Archivos Fase 3

```
agenda/
├── src/
│   ├── buscador.py      # NUEVO - Búsquedas avanzadas
│   ├── reportes.py      # NUEVO - Reportes predefinidos
│   └── exportadores.py  # NUEVO - Exportación CSV/XLSX/JSON/PDF
├── tests/
│   ├── test_buscador.py   # NUEVO
│   ├── test_reportes.py   # NUEVO
│   └── test_exportadores.py # NUEVO
├── fase2_crud_core/...
├── fase3_busqueda_reportes/
│   ├── spec.md
│   ├── progress.md
│   └── instalacion.md    # Este archivo
└── requirements.txt
```

## Tests Unitarios

```bash
# Tests Fase 3 (buscador, reportes, exportadores)
pytest tests/test_buscador.py -v
pytest tests/test_reportes.py -v
pytest tests/test_exportadores.py -v

# Todos los tests
pytest tests/ -v

# Con cobertura (incluye Fase 2 y 3)
pytest tests/ --cov=src --cov-report=html
# Abrir htmlcov/index.html
```

## Pruebas Manuales

### 1. Búsquedas Avanzadas

```python
from src.buscador import buscar_personas, buscar_por_cuil, busqueda_avanzada

# Búsqueda con filtros múltiples
resultados = buscar_personas(
    nombre="Juan",
    apellido="Pérez",
    limit=10,
    offset=0
)
print(f"Encontrados: {resultados['total']}")

# Búsqueda exacta por CUIL
persona = buscar_por_cuil("20-12345678-9")
if persona:
    print(f"Persona: {persona['nombre']} {persona['apellido']}")

# Búsqueda unificada
coincidencias = busqueda_avanzada("Juan", buscar_en="ambos")
print(f"Coincidencias: {len(coincidencias)}")
```

### 2. Reportes

```python
from src.reportes import (
    reporte_personas_por_fecha,
    reporte_duplicados_cuil,
    reporte_estadisticas_generales
)

# Reporte por fecha (últimos 30 días por defecto)
reporte = reporte_personas_por_fecha()
print(f"Total últimos 30 días: {reporte['total']}")
print(f"Promedio diario: {reporte['promedio_diario']}")

# Estadísticas generales
stats = reporte_estadisticas_generales()
print(f"Primer registro: {stats['primer_registro']}")
print(f"Top 10 apellidos: {stats['top_apellidos']}")

# Duplicados
duplicados = reporte_duplicados_cuil()
for dup in duplicados:
    print(f"CUI duplicado: {dup['cuil']} ({dup['cantidad']} veces)")
```

### 3. Exportación

```python
from src.exportadores import exportar_a_csv, exportar_a_xlsx, exportar_a_json
from src.buscador import buscar_personas

# Obtener datos
datos = buscar_personas(limit=100)['resultados']

# Exportar a CSV
exportar_a_csv(datos, "personas.csv")
print("CSV guardado: personas.csv")

# Exportar a Excel
exportar_a_xlsx(datos, "personas.xlsx", hoja_nombre="MiLista")

# Exportar a JSON
exportar_a_json(datos, "personas.json", indent=4)

# Exportar a PDF
exportar_a_pdf(datos, "personas.pdf", titulo="Listado de Personas")
```

### 4. Factory de Exportadores

```python
from src.exportadores import obtener_exportador

exportador = obtener_exportador('csv')  # 'csv', 'xlsx', 'json', 'pdf'
filas = exportador(datos, "salida.csv")
print(f"Exportadas {filas} filas")
```

## Funcionalidades de Búsqueda

| Función | Descripción | Retorna |
|---------|------------|---------|
| `buscar_personas()` | Búsqueda con filtros y paginación | dict (resultados, total, pagina) |
| `buscar_por_cuil()` | Búsqueda exacta CUIL | dict \| None |
| `buscar_por_nombre()` | Búsqueda por nombre/apellido | list |
| `buscar_por_fecha()` | Búsqueda por rango de fechas | dict paginado |
| `busqueda_avanzada()` | Búsqueda unificada multi-campo | list |
| `buscar_duplicados_cuil()` | Detectar CUILs duplicados | list |
| `sugerir_busqueda()` | Sugerencias autocompletado | list[str] |

## Formatos de Exportación

| Formato | Dependencias | Caso de Uso |
|---------|-------------|-------------|
| CSV | stdlib | Import a Excel, procesamiento batch |
| XLSX | pandas, openpyxl | Reportes formateados, análisis |
| JSON | stdlib | API/Web, integración sistemas |
| PDF | reportlab | Impresión, archivo formal |

## Reportes Disponibles

```python
# 1. Personas registradas por fecha
reporte_personas_por_fecha(
    fecha_desde=datetime(2024, 1, 1),
    fecha_hasta=datetime(2024, 1, 31)
)
# Retorna: {total, por_dia[...], promedio_diario, rango}

# 2. Duplicados de CUIL
reporte_duplicados_cuil()
# Retorna: [{cuil, cantidad, personas:[...]}, ...]

# 3. Estadísticas generales
reporte_estadisticas_generales()
# Retorna: {total, primer_registro, ultimo_registro, top_apellidos, ...}

# 4. Resumen mensual
reporte_resumen_mensual(mes=1, anio=2024)
# Retorna: {total_registros, promedio_diario, rango}
```

## Troubleshooting Fase 3

### Error: "ImportError: No module named 'pandas'"
```bash
pip install pandas openpyxl
```

### Error: "ImportError: No module named 'reportlab'"
```bash
pip install reportlab
```

### Exportación PDF falla con UnicodeEncodeError
- Asegurar fuentes Unicode en ReportLab
- Considerar usar `reportlab.lib.fonts` agregar `Helvetica`

### Búsqueda por CUIL falla con formato
- Validar formato `XX-XXXXXXXX-X`
- Usar `buscar_por_cuil()` que valida internamente

### Reporte duplicados devuelve vacío
- Verificar que haya CUILs repetidos en la BD
- El reporte solo incluye CUILs con COUNT > 1

## Siguiente Paso

Una vez probadas las búsquedas, reportes y exportaciones, avanzar a **Fase 4: Menú e Interfaz de Usuario**.
