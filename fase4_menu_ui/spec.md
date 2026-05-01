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

## Entregables Completados
1. **Módulo `src/menu_principal.py`** - Bucle principal y controladores de pantalla
2. **Módulo `src/formularios.py`** - Formularios validados para CRUD, búsqueda y exportación
3. **Módulo `src/vistas.py`** - Renderizado de tablas, menús y componentes CLI
4. **Archivos de entrada**:
   - `main.py` - Punto de entrada principal
   - `menu_principal.py` - Script alternativo de entrada

## Funcionalidades Implementadas

### Pantallas
- **Alta de Persona** - formulario con validación CUIL, nombre, apellido
- **Búsqueda** - filtros múltiples + resultados paginados
- **Modificación** - selección por ID/CUIL + edición selectiva de campos
- **Eliminación** - doble confirmación para seguridad
- **Reportes** - menú con 4 tipos de reportes
- **Exportación** - selector de formato (CSV/XLSX/JSON/PDF) con filtros opcionales

### Librerías Utilizadas
- `rich` - Tablas formateadas, colores, prompts, progreso
- Fallback a stdlib si `rich` no disponible (modo consola simple)

### Validaciones
- CUIL: formato XX-XXXXXXXX-X con regex
- Nombre/Apellido: 2-100 caracteres, solo letras
- Fechas: formato YYYY-MM-DD
- Números: enteros positivos

## Criterios de Éxito
- [x] Menú navegable con flujo completo
- [x] Validaciones funcionan (tiempo real)
- [x] Interfaz clara con tablas y colores
- [x] Manejo de errores amigable
