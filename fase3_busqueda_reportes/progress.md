# Checklist de Tareas - Fase 3: Búsqueda y Reportes

## Tareas Completadas
- [x] Diseñar esquema de búsquedas con filtros
- [x] Implementar módulo src/buscador.py completo:
  - [x] buscar_personas() - Búsqueda unificada con paginación
  - [x] buscar_por_cuil() - Búsqueda exacta CUIL
  - [x] buscar_por_nombre() - Búsqueda LIKE/exacta
  - [x] buscar_por_fecha() - Rango de fechas
  - [x] busqueda_avanzada() - Multi-campo combinado
  - [x] buscar_duplicados_cuil() - Detección duplicados
  - [x] sugerir_busqueda() - Sugerencias autocompletado
- [x] Implementar módulo src/reportes.py completo:
  - [x] reporte_personas_por_fecha() - Agrupado por día
  - [x] reporte_duplicados_cuil() - Detalle duplicados
  - [x] reporte_estadisticas_generales() - Métricas globales
  - [x] reporte_resumen_mensual() - Resumen por mes
  - [x] generar_reporte_completo() - Función unificada
- [x] Implementar módulo src/exportadores.py completo:
  - [x] exportar_a_csv() - CSV UTF-8, comillas
  - [x] exportar_a_xlsx() - Excel via pandas/openpyxl
  - [x] exportar_a_json() - JSON con fechas serializadas
  - [x] exportar_a_pdf() - PDF tabular via ReportLab
  - [x] obtener_exportador() - Factory function
  - [x] validar_formato_archivo() - Validación extensiones
- [x] Actualizar src/__init__.py (exponer funciones Fase 3)
- [x] Crear tests unitarios de Fase 3:
  - [x] tests/test_buscador.py (7 tests)
  - [x] tests/test_reportes.py (10 tests)
  - [x] tests/test_exportadores.py (15 tests)
- [x] Actualizar requirements.txt (reportlab)
- [x] Actualizar pyproject.toml (dependencias pd, all)
- [x] Crear guía instalación Fase 3 (fase3/instalacion.md)
- [x] Actualizar AGENTS.md con estado Fase 3
- [x] Actualizar README.md con ejemplos Fase 3

## Tareas Pendientes (Usuario)
- [ ] Probar búsquedas con DB real
- [ ] Probar reportes con datos reales
- [ ] Probar exportación CSV/XLSX/JSON/PDF
- [ ] Ejecutar tests unitarios: `pytest tests/test_*.py -v`
- [ ] Verificar cobertura: `pytest --cov=src`
- [ ] Documentar ejemplos de uso en README si es necesario

## Notas
Fase 3 completada en código. Requiere validación manual con base de datos real y tests.
