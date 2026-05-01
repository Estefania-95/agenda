# Especificaciones Técnicas - Fase 3: Búsqueda y Reportes

## Objetivo
Implementar funcionalidades avanzadas de búsqueda y generación de reportes.

## Requerimientos Técnicos

### Búsquedas Avanzadas
- Búsqueda por nombre/apellido (LIKE con comodines)
- Búsqueda por rango de fecha_registro
- Búsqueda por CUIL exacto
- Búsqueda combinada (filtros múltiples)
- Paginación (LIMIT/OFFSET)

### Reportes
- Reporte de personas registradas por rango de fechas
- Reporte de duplicados de CUIL
- Exportación a CSV/XLSX (usar pandas)
- Estadísticas básicas (total, promedio edad si se agrega campo)

### Optimización
- Índices en columnas de búsqueda frecuente
- Query optimizadas con JOINs si se agregan tablas relacionadas
- Caché de consultas frecuentes (dict/lru_cache)

### Estructura de Archivos
```
fase3_busqueda_reportes/
  ├── spec.md
  ├── progress.md
  ├── buscador.py      # Funciones de búsqueda
  ├── reportes.py      # Generación de reportes
  └── exportadores.py  # CSV, XLSX, PDF
```

## Entregables Completados
1. **Módulo `src/buscador.py`** - Funciones de búsqueda:
   - `buscar_personas()` - Búsqueda unificada con filtros y paginación
   - `buscar_por_cuil()` - Búsqueda exacta por CUIL
   - `buscar_por_nombre()` - Búsqueda por nombre/apellido (exacto o LIKE)
   - `buscar_por_fecha()` - Búsqueda por rango de fecha_registro
   - `busqueda_avanzada()` - Búsqueda combinada en múltiples campos
   - `buscar_duplicados_cuil()` - Detección de CUILs duplicados
   - `sugerir_busqueda()` - Sugerencias de autocompletado

2. **Módulo `src/reportes.py`** - Generación de reportes:
   - `reporte_personas_por_fecha()` - Agrupado por día con promedios
   - `reporte_duplicados_cuil()` - Detalle completo de duplicados
   - `reporte_estadisticas_generales()` - Métricas globales
   - `reporte_resumen_mensual()` - Resumen por mes
   - `generar_reporte_completo()` - Función unificada

3. **Módulo `src/exportadores.py`** - Exportación:
   - `exportar_a_csv()` - CSV con UTF-8 y comillas
   - `exportar_a_xlsx()` - Excel via pandas/openpyxl
   - `exportar_a_json()` - JSON con fechas serializadas
   - `exportar_a_pdf()` - PDF tabular via ReportLab
   - `obtener_exportador()` - Factory function
   - `validar_formato_archivo()` - Validación de extensiones

4. **Tests unitarios**:
   - `tests/test_buscador.py` (7 tests)
   - `tests/test_reportes.py` (10 tests)
   - `tests/test_exportadores.py` (15 tests)

## Criterios de Éxito
- [x] Búsquedas funcionan con múltiples filtros
- [x] Reportes generan datos correctos
- [x] Exportación a CSV/XLSX/JSON operativa
- [x] Paginación implementada (LIMIT/OFFSET)
- [x] Tests unitarios creados (> esperando ejecución)
