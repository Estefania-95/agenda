# AGENTS.md - Instrucciones para Agentes Kilo

## Contexto del Proyecto
Sistema de Gestión Modular con SQL Server y Python. Metodología por fases estrictas.

## Reglas CRÍTICAS

### 1. Flujo de Trabajo por Fases
- **NO** avanzar a fase siguiente sin completar checklist de la fase actual
- Cada fase tiene: spec.md (especificaciones) + progress.md (checklist)
- Marcar tareas en progress.md al completarlas

### 2. Fase 2 Actual (Estado: Implementando)
**Objetivo**: Operaciones CRUD con validaciones y transacciones

**Archivos críticos**:
- `src/crud_personas.py` - Módulo CRUD (YA CREADO)
- `tests/test_crud_personas.py` - Tests unitarios (YA CREADO)
- `src/database.py` - Dependencia Fase 1

**Acciones pendientes Fase 2**:
- [ ] Probar funciones CRUD con base de datos real
- [ ] Ejecutar suite de tests unitarios
- [ ] Asegurar cobertura >80%
- [ ] Documentar uso del módulo CRUD

### 3. Estructura de Commits
```
feat: agregar operaciones CRUD con validaciones
fix: corregir manejo de transacciones en actualizar
test: aumentar cobertura test CRUD al 90%
docs: agregar guía instalación Fase 2
```

### 4. Código Python
- Seguir PEP 8 estrictamente
- Type hints obligatorios en funciones públicas
- Docstrings en formato Google Style
- Manejo de excepciones específico (no except: pass)
- Logging ya configurado en Fase 2 (logs/operaciones.log)
- Consultas parametrizadas SIEMPRE (evitar SQL injection)

### 5. Base de Datos
- Transacciones explícitas (BEGIN/COMMIT/ROLLBACK)
- Índices en columnas de búsqueda (creados en Fase 1)
- NVARCHAR para texto (compatibilidad Unicode)
- Validaciones en aplicación (no solo en DB)

### 6. Variables de Entorno
- NO committear .env (ya en .gitignore)
- Usar python-dotenv load_dotenv()
- Validar TODAS las variables al inicio
- Ejemplo en .env.example como referencia

### 7. Pruebas
- Tests unitarios mínimos 80% cobertura (Fase 2 objetivo)
- Tests de integración con DB real (flag --integration)
- Tests de CLI con mocking (fase 4)

## Comandos Útiles
```bash
# Probar conexión Fase 1
python src/database.py

# Crear BD
sqlcmd -S localhost\SQLEXPRESS -i fase1_db_infra/init_db.sql

# Tests Fase 2
pytest tests/test_crud_personas.py -v
pytest tests/ --cov=src --cov-report=html

# Linting
ruff check src/
black src/

# Testing completo
pytest tests/ -v --integration
```

## Recordatorio
**NO AVANZAR** a Fase 3 sin:
- CRUD probado en base de datos real
- Tests unitarios pasando (>80% cobertura)
- Validacionesimplementadas y testeadas
- Logging operacional funcionando
- Progress.md actualizado
