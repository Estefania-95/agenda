# Checklist de Tareas - Fase 2: CRUD Core

## Tareas Completadas
- [x] Crear spec.md de fase 2 con requerimientos CRUD
- [x] Implementar módulo src/crud_personas.py completo:
  - [x] Función crear_persona() con validaciones y transacciones
  - [x] Función obtener_persona() retorna dict | None
  - [x] Función actualizar_persona() con campos dinámicos
  - [x] Función eliminar_persona() con confirmación de rowcount
  - [x] Función listar_personas() con filtros (nombre, apellido, cuil, fechas)
  - [x] Función listar_personas() con paginación (limit/offset)
  - [x] Función contar_personas() auxiliar para paginación
  - [x] Validaciones de CUIL con regex (formato XX-XXXXXXXX-X)
  - [x] Validaciones de nombre/apellido (solo letras, 2-100 chars)
  - [x] Clases de excepción: ValidacionError, DuplicadoError
  - [x] Manejo de transacciones con commit/rollback automático
  - [x] Logging configurado en logs/operaciones.log
  - [x] Captura específica de pyodbc.IntegrityError para duplicados
  - [x] Import pyodbc para capturar excepciones específicas
- [x] Crear tests unitarios en tests/test_crud_personas.py
  - [x] Tests de validaciones (CUIL, nombre, apellido)
  - [x] Tests de CRUD con mocking de DB
  - [x] Tests de integración con flag --integration
- [x] Crear archivos de soporte para tests:
  - [x] tests/__init__.py
  - [x] tests/conftest.py (fixtures compartidos)
  - [x] Actualizar pyproject.toml con pythonpath y markers
- [x] Crear directorio logs/ para archivos de log
- [x] Actualizar requirements.txt con dependencias
- [x] Crear guía de instalación y pruebas (fase2_crud_core/instalacion.md)

## Tareas Pendientes (Usuario)
- [ ] Ejecutar tests unitarios: `pytest tests/test_crud_personas.py -v`
- [ ] Probar CRUD manualmente con DB real
- [ ] Verificar logs en logs/operaciones.log
- [ ] Asegurar cobertura >80%: `pytest --cov=src`

## Notas
Fase 2 completada en código. Requiere validación manual con base de datos real.
