# AGENTS.md - Instrucciones para Agentes Kilo

## Contexto del Proyecto
Sistema de Gestión Modular con SQL Server y Python. Metodología por fases estrictas.

## Reglas CRÍTICAS

### 1. Flujo de Trabajo por Fases
- **NO** avanzar a fase siguiente sin completar checklist de la fase actual
- Cada fase tiene: spec.md (especificaciones) + progress.md (checklist)
- Marcar tareas en progress.md al completarlas

### 2. Fase 3 Actual (Estado: Implementando)
**Objetivo**: Búsqueda avanzada y generación de reportes con exportación

**Archivos críticos**:
- `src/buscador.py` - Funciones de búsqueda (YA CREADO)
- `src/reportes.py` - Generación de reportes (YA CREADO)
- `src/exportadores.py` - Exportación CSV/XLSX/PDF (YA CREADO)
- `tests/test_*.py` - Tests unitarios Fase 3 (YA CREADOS)

**Acciones pendientes Fase 3**:
- [ ] Probar búsquedas con base de datos real
- [ ] Probar reportes con datos reales
- [ ] Probar exportación a CSV/XLSX/JSON
- [ ] Ejecutar tests unitarios Fase 3
- [ ] Verificar cobertura >80%
- [ ] Documentar formatos de exportación

### 3. Estructura de Commits
```
feat: agregar búsqueda avanzada con filtros múltiples
feat: agregar reportes estadísticos y de duplicados
feat: agregar exportación CSV/XLSX/JSON/PDF
test: agregar suite tests Fase 3 (32 tests)
docs: actualizar README con ejemplos de reportes
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
**NO AVANZAR** a Fase 4 sin:
- Búsquedas probadas con DB real
- Reportes generando datos correctos
- Exportación funcionando (CSV/XLSX)
- Tests unitarios pasando (>80% cobertura)
- Progress.md de Fase 3 actualizado
