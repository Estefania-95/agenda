# AGENTS.md - Instrucciones para Agentes Kilo

## Contexto del Proyecto
Sistema de Gestión Modular con SQL Server y Python. Metodología por fases estrictas.

## Reglas CRÍTICAS

### 1. Flujo de Trabajo por Fases
- **NO** avanzar a fase siguiente sin completar checklist de la fase actual
- Cada fase tiene: spec.md (especificaciones) + progress.md (checklist)
- Marcar tareas en progress.md al completarlas

### 2. Fase 4 Actual (Estado: Completada en código, pendiente validación)
**Objetivo**: Menú e Interfaz de Usuario CLI - LISTO PARA PROBAR

**Archivos críticos** (TODOS CREADOS):
- `src/vistas.py` - Renderizado (tablas, menús, colores)
- `src/formularios.py` - Formularios validados (alta, búsqueda, mod, elim, export)
- `src/menu_principal.py` - Bucle principal y controladores
- `main.py` - Punto de entrada principal
- `menu_principal.py` - Script alternativo en raíz

**Acciones pendientes Fase 4**:
- [ ] Probar interfaz con base de datos real
- [ ] Verificar todos los flujos de usuario (alta, buscar, modificar, eliminar, reportes, exportar)
- [ ] Validar que `rich` esté instalado (`pip install rich`)
- [ ] Documentar atajos de teclado en README
- [ ] Ejecutar tests unitarios Fases 1-3
- [ ] Actualizar progress.md con validaciones manuales

### 3. Estructura de Commits
```
feat: agregar menú CLI con rich para Fase 4
fix: corregir validación de fechas en formulario
docs: actualizar README con pantallas y flujos
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
**NO AVANZAR** a Fase 5 sin:
- Menú probado con DB real
- Flujo completo verificado (alta, buscar, modificar, eliminar, reportes, exportar)
- Rich instalado y funcionando
- Progress.md de Fase 4 actualizado
