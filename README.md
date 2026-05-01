# Sistema de Gestión Modular - SQL Server

Sistema de gestión模块ar con SQL Server y Python, siguiendo metodología por fases.

## Stack Técnico

- **Lenguaje**: Python 3.9+
- **Base de Datos**: SQL Server (Local/Remoto)
- **Conexión**: pyodbc
- **Driver**: ODBC Driver 17/18 for SQL Server
- **Variables de Entorno**: python-dotenv

## Estructura del Proyecto

```
agenda/
├── main.py                 # Punto de entrada principal (Fase 4)
├── menu_principal.py       # Script alternativo (Fase 4)
├── src/
│   ├── __init__.py         # Exports de todas las fases
│   ├── database.py         # Fase 1: Conexión SQL Server
│   ├── crud_personas.py    # Fase 2: Operaciones CRUD
│   ├── buscador.py         # Fase 3: Búsquedas avanzadas
│   ├── reportes.py         # Fase 3: Reportes predefinidos
│   ├── exportadores.py     # Fase 3: Exportación CSV/XLSX/JSON/PDF
│   ├── menu_principal.py   # Fase 4: Bucle principal (src/)
│   ├── formularios.py      # Fase 4: Formularios validados
│   └── vistas.py           # Fase 4: Renderizado CLI
├── fase1_db_infra/         # Infraestructura DB
│   ├── spec.md
│   ├── progress.md
│   └── init_db.sql
├── fase2_crud_core/        # CRUD Core
│   ├── spec.md
│   └── progress.md
├── fase3_busqueda_reportes/ # Búsqueda y Reportes
│   ├── spec.md
│   └── progress.md
├── fase4_menu_ui/          # Interfaz CLI
│   ├── spec.md
│   └── progress.md
├── fase5_entrega_final/    # Entrega Final (pendiente)
│   ├── spec.md
│   └── progress.md
├── tests/                  # Tests unitarios
│   ├── test_database.py        (Fase 1)
│   ├── test_crud_personas.py   (Fase 2)
│   ├── test_buscador.py        (Fase 3)
│   ├── test_reportes.py        (Fase 3)
│   ├── test_exportadores.py    (Fase 3)
│   └── conftest.py
├── logs/                   # Logs operacionales
├── .env.example            # Variables de entorno
├── .gitignore
├── AGENTS.md               # Instrucciones agentes Kilo
├── COMMANDS.md             # Comandos útiles
├── pyproject.toml          # Configuración empaquetado
├── README.md               # Este archivo
└── requirements.txt        # Dependencias
```

## Instalación Rápida

### Prerrequisitos

1. **SQL Server** (Local o Remoto)
   - SQL Server Express (gratuito) o superior
   - Habilitar autenticación SQL Server (modo mixto)

2. **ODBC Driver** para SQL Server
   - Windows: [Descargar ODBC Driver](https://learn.microsoft.com/en-us/sql/connect/odbc/download-odbc-driver-for-sql-server)
   - Linux: `sudo apt-get install msodbcsql17`

3. **Python 3.9+**

### Pasos de Instalación

```bash
# 1. Clonar repositorio
git clone <repo-url>
cd agenda

# 2. Crear entorno virtual
python -m venv venv

# 3. Activar entorno
# Windows:
venv\Scripts\Activate.ps1
# Linux/Mac:
source venv/bin/activate

# 4. Instalar dependencias básicas + CLI
pip install -r requirements.txt
# O instalar con extras:
pip install -e ".[all]"

# 5. Configurar variables de entorno
cp .env.example .env
# Editar .env con valores de tu servidor SQL Server

# 6. Inicializar base de datos
# Ejecutar init_db.sql en SQL Server Management Studio o via sqlcmd:
# sqlcmd -S localhost\SQLEXPRESS -i fase1_db_infra/init_db.sql

# 7. Verificar instalación
python main.py
```

## Configuración de Variables

Editar archivo `.env`:

```env
DB_SERVER=localhost\SQLEXPRESS   # ServidorSQL
DB_NAME=GestionDB                # Nombre de la base de datos
DB_UID=gestion_user              # Usuario SQL
DB_PWD=TuPasswordSegura123!      # Password del usuario
```

## Prueba de Conexión

```bash
# Ejecutar prueba de conexión Fase 1
python src/database.py
```

Salida esperada:
```
✓ Estado: True
✓ Mensaje: Conexión exitosa a SQL Server
✓ SQL Server: Microsoft SQL Server 2019...
¡Conexión exitosa!
```

## Desarrollo por Fases

- **Fase 1**: Infraestructura SQL Server (completada)
- **Fase 2**: CRUD Core (completada)
- **Fase 3**: Búsqueda y Reportes (completada)
- **Fase 4**: Menú e Interfaz de Usuario (completada)
- **Fase 5**: Entrega Final (pendiente)

Ver `faseX_*/spec.md` para detalles de cada fase.

## Uso - Interfaz CLI (Fase 4)

### Inicio de la Aplicación

```bash
# Opción 1: Ejecutar main.py (recomendado)
python main.py

# Opción 2: Ejecutar menu_principal.py
python menu_principal.py

# Opción 3: Usar módulo -m
python -m src.menu_principal
```

### Flujo de Navegación

```
┌─ Menú Principal ──────────────────────┐
│ 1. Alta de Persona                    │
│ 2. Búsqueda de Personas               │
│ 3. Modificación de Persona            │
│ 4. Baja de Persona                    │
│ 5. Reportes                           │
│ 6. Exportar Datos                     │
│ 0. Salir                              │
└───────────────────────────────────────┘
```

### Pantallas de Reportes

```
┌─ Reportes ────────────────────────────┐
│ 1. Estadísticas Generales             │
│ 2. Personas por Rango de Fechas       │
│ 3. Detectar DUPLICADOS de CUIL        │
│ 4. Resumen Mensual                    │
│ 0. Volver                             │
└───────────────────────────────────────┘
```

### Características Visuales

- **Colores**: Usa `rich` para tablas con colores y bordes redondeados
- **Paginación**: Navegación con ← (anterior) y → (siguiente)
- **Validación en tiempo real**: CUIL, fechas, longitud
- **Confirmaciones**: Doble confirmación para eliminar
- **Fallback modo simple**: Si `rich` no instalado, funciona en consola básica

### Ejemplos de Uso

**Alta de persona**:
```
Nombre: Juan Pérez
Apellido: Pérez
CUIL: 20-12345678-9
¿Confirma? (s/N): s
✓ Persona creada exitosamente.
```

**Búsqueda**:
```
Nombre (opcional): Juan
Apellido (opcional): Pérez
Límite (max 1000): 50
→ Mostrando 1-10 de 15 resultados
[prev] Página anterior | [next] Página siguiente | [back] Volver
```

**Exportación**:
```
Formato: csv
Ruta de salida: personas.csv
¿Aplicar filtros? (s/N): n
✓ Exportación completada: 150 filas a 'personas.csv'
```

### Búsquedas Avanzadas (Python REPL)

```python
from src.buscador import buscar_personas, buscar_por_cuil, busqueda_avanzada

# Búsqueda con filtros y paginación
resultados = buscar_personas(
    nombre="Juan",
    apellido=None,
    cuil=None,
    limit=50,
    offset=0
)
print(f"Total encontrados: {resultados['total']}")
print(f"Página: {resultados['pagina_actual']} de {resultados['total_paginas']}")

# Búsqueda exacta por CUIL
persona = buscar_por_cuil("20-12345678-9")

# Búsqueda unificada (nombre, apellido o CUIL)
coincidencias = busqueda_avanzada("Juan", buscar_en="ambos")
```

### Reportes (Python REPL)

```python
from src.reportes import reporte_personas_por_fecha, reporte_estadisticas_generales

# Reporte por rango de fechas
reporte = reporte_personas_por_fecha()
print(f"Total últimos 30 días: {reporte['total']}")
print(f"Promedio diario: {reporte['promedio_diario']}")
for dia in reporte['por_dia']:
    print(f"  {dia['fecha']}: {dia['cantidad']} registros")

# Estadísticas generales
stats = reporte_estadisticas_generales()
print(f"Total absoluto: {stats['total']}")
print(f"Primer registro: {stats['primer_registro']}")
print(f"Top 10 apellidos: {stats['top_apellidos']}")
```

### Exportación de Datos

```python
from src.exportadores import exportar_a_csv, exportar_a_xlsx, obtener_exportador
from src.buscador import buscar_personas

# Obtener datos
datos = buscar_personas(limit=100)['resultados']

# Exportar formatos soportados
exportar_a_csv(datos, "personas.csv")
exportar_a_xlsx(datos, "personas.xlsx")
exportar_a_json(datos, "personas.json")
exportar_a_pdf(datos, "personas.pdf", titulo="Listado")

# O usar factory
exportador = obtener_exportador('xlsx')
exportador(datos, "salida.xlsx")
```

### Tests de Fase 3

```bash
# Tests unitarios búsqueda y reportes
pytest tests/test_buscador.py tests/test_reportes.py tests/test_exportadores.py -v

# Tests de integración completos
pytest tests/ -v --integration

# Cobertura
pytest tests/ --cov=src --cov-report=html
```

## Troubleshooting

### Error: "Driver not found"
- Verificar instalación de ODBC Driver
- En Windows: Revisar en "ODBC Data Sources" (odbcad32.exe)

### Error: "Login failed for user"
- Verificar credenciales en .env
- Asegurar que SQL Server permite autenticación SQL
- Crear login en SQL Server si no existe

### Error: "Timeout expired"
- Verificar que SQL Server esté corriendo
- Revisar firewall (puerto 1433)
- Probar conexión con SQL Server Management Studio

### Error: "ImportError: No module named 'pandas'"
```bash
pip install pandas openpyxl
```

### Error: "ImportError: No module named 'reportlab'"
```bash
pip install reportlab
```

### Error exportación PDF: UnicodeEncodeError
- Instalar fuentes Unicode o configurar ReportLab
- Verificar `reportlab.lib.fonts` cargando `Helvetica`

## Licencia

Proyecto educativo - Uso libre.
