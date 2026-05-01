# Especificaciones Técnicas - Fase 4: Menú e Interfaz de Usuario

## Objetivo
Desarrollar interfaz de consola (CLI) para interacción del usuario.

## Requerimientos Técnicos

### Interfaz CLI
- Menú principal con opciones CRUD y búsqueda
- Menús secundarios para cada operación
- Navegación con teclas (arriba/abajo, Enter, ESC)
- Formularios de ingreso de datos (validación en tiempo real)
- Confirmaciones para operaciones críticas (eliminar)

### Librerías Recomendadas
- `curses` (Unix/Linux/Mac)
- `windows-curses` (Windows)
- `prompt_toolkit` (multi-platforma, más rica)
- `rich` para tablas y formateo bonito

### Flujo de Navegación
```
┌─ Menú Principal ──────────────────────┐
│ 1. Alta de Persona                    │
│ 2. Búsqueda de Personas               │
│ 3. Modificación de Persona            │
│ 4. Baja de Persona                    │
│ 5. Reportes                           │
│ 6. Exportar Datos                     │
│ 0. Salir                              │
└───────────────────────────────────────┘
```

### Pantallas
1. **Alta**: Formulario con campos nombre, apellido, cuil
2. **Búsqueda**: Filtros + tabla de resultados + paginación
3. **Modificación**: Seleccionar persona + editar campos
4. **Baja**: Confirmación antes de eliminar
5. **Reportes**: Lista de reportes disponibles
6. **Exportar**: Seleccionar formato (CSV/XLSX/PDF)

### Validaciones de Entrada
- CUIL: regex `^\d{2}-\d{8}-\d{1}$`
- Nombre/Apellido: solo letras y espacios, 2-100 caracteres
- Evitar campos vacíos

## Entregables
1. Módulo `menu_principal.py` (main loop)
2. Módulo `formularios.py` (inputs validados)
3. Módulo `vistas.py` (renderizado de tablas/menús)
4. Archivo `main.py` (punto de entrada)

## Criterios de Éxito
- [ ] Menú navegable con flujo completo
- [ ] Validaciones funcionan
- [ ] Interfaz clara y usable
- [ ] Manejo de errores amigable
