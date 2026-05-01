# Comandos Útiles - Proyecto Gestión Modular

## Entorno Virtual

```bash
# Crear venv
python -m venv venv

# Activar (Windows PowerShell)
venv\Scripts\Activate.ps1

# Activar (Linux/Mac)
source venv/bin/activate

# Desactivar
deactivate
```

## Instalación de Dependencias

```bash
# Instalar todas las dependencias básicas
pip install -r requirements.txt

# Instalar con extras (dev + pd + cli)
pip install -e ".[all]"

# Instalar solo dependencias de desarrollo
pip install -e ".[dev]"

# Instalar solo dependencias de pandas/exportación
pip install -e ".[pd]"

# Instalar solo dependencias de CLI
pip install -e ".[cli]"

# Actualizar dependencias
pip install -r requirements.txt --upgrade
```

## Base de Datos - SQL Server

```bash
# Verificar conexión (Fase 1)
python src/database.py

# Conectar con sqlcmd (usar credenciales de .env)
sqlcmd -S localhost\SQLEXPRESS -U gestion_user -P ChangeMe_123! -d GestionDB

# Ejecutar script SQL de inicialización
sqlcmd -S localhost\SQLEXPRESS -i fase1_db_infra/init_db.sql

# Abrir SSMS (SQL Server Management Studio)
start ssms

# Listar bases de datos (query)
SELECT name FROM sys.databases;

# Ver tablas de GestionDB
USE GestionDB;
SELECT * FROM sys.tables;
```

## Testing

```bash
# Tests unitarios básicos
pytest tests/ -v

# Tests con cobertura
pytest tests/ --cov=src --cov-report=term-missing

# Reporte HTML de cobertura
pytest tests/ --cov=src --cov-report=html
# Abrir htmlcov/index.html

# Tests de integración (requiere DB real)
pytest tests/ -v --integration

# Un test específico
pytest tests/test_crud_personas.py::test_crear_persona_exito -v

# Parar en primer error
pytest tests/ -x

# Mostrar prints de debug
pytest tests/ -s
```

## Linting y Formato

```bash
# Instalar ruff (recomendado)
pip install ruff

# Verificar estilo
ruff check src/

# Auto-corregir
ruff check src/ --fix

# Instalar black (alternativa)
pip install black
black src/

# Ver tipos con mypy (opcional)
pip install mypy
mypy src/
```

## Logging

```bash
# Ver logs en vivo (PowerShell)
Get-Content logs/operaciones.log -Wait -Tail 20

# Ver últimos logs (Linux/Mac)
tail -f logs/operaciones.log
```

## Git

```bash
# Inicializar repo
git init

# Agregar archivos (excepto .env)
git add .

# Commit
git commit -m "feat: agregar conexión y CRUD Fase 1-2"

# Status
git status

# Diff
git diff
```

## Empaquetado

```bash
# Instalar en modo desarrollo
pip install -e .

# Desinstalar
pip uninstall gestion-modular

# Construir distribución
python -m build  # requiere 'build' package
```

## Troubleshooting Rápido

| Problema | Solución |
|----------|----------|
| `pyodbc.Error: [Microsoft][ODBC Driver 17 for SQL Server]Login timeout expired` | Verificar SQL Server corriendo y firewall |
| `ModuleNotFoundError: No module named 'pyodbc'` | `pip install pyodbc` (o reinstalar con wheel) |
| `Driver not found` | Instalar ODBC Driver desde Microsoft |
| `Permission denied` (logs) | Ejecutar como Administrador o cambiar permisos |
| `UnicodeEncodeError` en logs | Verificar encoding UTF-8 en handler |

## Variables de Entorno Comunes

```env
# Local (SQL Express)
DB_SERVER=localhost\SQLEXPRESS
DB_NAME=GestionDB
DB_UID=gestion_user
DB_PWD=tu_password

# Remoto (IP)
DB_SERVER=192.168.1.100
DB_PORT=1433  # opcional

# Docker (contenedor SQL Server)
DB_SERVER=localhost,1433
```
