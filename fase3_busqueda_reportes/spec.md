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

## Entregables
1. Módulo `buscador.py` con filtros
2. Módulo `reportes.py` con reportes predefinidos
3. Módulo `exportadores.py`
4. Tests de búsquedas y reportes

## Criterios de Éxito
- [ ] Búsquedas funcionan con multiples filtros
- [ ] Reportes generan datos correctos
- [ ] Exportación a CSV/XLSX operativa
- [ ] Paginación implementada
