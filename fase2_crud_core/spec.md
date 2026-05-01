# Especificaciones Técnicas - Fase 2: CRUD Core

## Objetivo
Implementar las operaciones CRUD (Create, Read, Update, Delete) sobre la tabla Personas.

## Requerimientos Técnicos

### Funciones CRUD a implementar
- `crear_persona(nombre, apellido, cuil)` → bool
- `obtener_persona(persona_id)` → dict | None
- `actualizar_persona(persona_id, **datos)` → bool
- `eliminar_persona(persona_id)` → bool
- `listar_personas(filtros=None)` → list[dict]

### Validaciones
- CUIL: formato XX-XXXXXXXX-X (validar con regex)
- Nombre/Apellido: máx 100 caracteres, solo letras y espacios
- Prevenir duplicados por CUIL

### Manejo de Errores
- Capturar excepciones pyodbc específicas
- Logging operacional (logs/operaciones.log)
- Rollback en transacciones fallidas

### Transacciones
- Cada operación CRUD en su propia transacción
- Commit explícito tras éxito
- Rollback automático en excepciones

## Entregables
1. Módulo `crud_personas.py` con todas las operaciones
2. Tests unitarios para cada función (pytest)
3. Logging configurado

## Criterios de Éxito
- [ ] Todas las operaciones CRUD funcionan
- [ ] Validaciones implementadas
- [ ] Transacciones manejadas correctamente
- [ ] Tests pasan >90%
