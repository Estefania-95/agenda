# AGENTS.md - Instrucciones para Agentes Kilo

## Contexto del Proyecto
Sistema de Gestión Modular con SQL Server y Python. Metodología por fases estrictas.

## Reglas CRÍTICAS

### 1. Flujo de Trabajo por Fases
- **NO** avanzar a fase siguiente sin completar checklist de la fase actual
- Cada fase tiene: spec.md (especificaciones) + progress.md (checklist)
- Marcar tareas en progress.md al completarlas

### 2. Fase 1 Actual (Estado: Implementando)
**Objetivo**: Conexión confiable a SQL Server

**Archivos críticos**:
- `src/database.py` - Módulo de conexión (YA CREADO)
- `fase1_db_infra/init_db.sql` - Script SQL (YA CREADO)
- `.env.example` - Configuración referencia (YA CREADO)

**Acciones pendientes Fase 1**:
- [ ] Probar conexión con servidor SQL Server real
- [ ] Ejecutar init_db.sql
- [ ] Verificar tabla Personas creada
- [ ] documentar connection string específico

### 3. Estructura de Commits
```
feat: agregar conexión pyodbc con variables de entorno
fix: corregir validación de variables .env
docs: actualizar README con instrucciones instalación
```

### 4. Código Python
- Seguir PEP 8 estrictamente
- Type hints obligatorios en funciones públicas
- Docstrings en formato Google Style
- Manejo de excepciones específico (no except: pass)
- Logging configurado desde Fase 2

### 5. Base de Datos
- Usar consultas parametrizadas SIEMPRE (evitar SQL injection)
- Transacciones explícitas (BEGIN/COMMIT/ROLLBACK)
- Índices en columnas de búsqueda
- NVARCHAR para texto (compatibilidad Unicode)

### 6. Variables de Entorno
- NO committear .env (ya en .gitignore)
- Usar python-dotenv load_dotenv()
- Validar TODAS las variables al inicio

### 7. Pruebas
- Tests unitarios mínimos 80% cobertura
- Tests de integración para conexión DB
- Tests de CLI con mocking (fase 4)

## Comandos Útiles
```bash
# Probar conexión Fase 1
python src/database.py

# Crear BD
sqlcmd -S localhost\SQLEXPRESS -i fase1_db_infra/init_db.sql

# Linting
ruff check src/
black src/

# Testing
pytest tests/ -v
```

## Recordatorio
**NO AVANZAR** a Fase 2 sin:
- Conexión probada en servidor real
- Tabla Personas verificada
- Progress.md actualizado
- Documentación de troubleshooting en README
