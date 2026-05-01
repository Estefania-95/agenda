# Instalación y Uso - Fase 4: Menú e Interfaz de Usuario

## Prerrequisitos

- [x] Fase 1, 2, 3 completadas y verificadas
- Base de datos operativa
- Dependencias instaladas: `pyodbc`, `python-dotenv`, `pandas`, `reportlab`

## Instalación de Dependencias CLI

```bash
# Instalar librerías de interfaz
pip install rich prompt-toolkit

# O instalar todas las dependencias (incluye Fases 1-3)
pip install -e ".[all]"

# Verificar instalación
python -c "import rich; print('Rich OK:', rich.__version__)"
```

## Estructura de Archivos Fase 4

```
agenda/
├── main.py              # NUEVO - Punto de entrada principal
├── menu_principal.py    # NUEVO - Scriptalternativo entrada
├── src/
│   ├── vistas.py        # NUEVO - Renderizado CLI
│   ├── formularios.py   # NUEVO - Formularios validados
│   ├── menu_principal.py # NUEVO - Bucle principal (dentro de src/)
│   └── ...              # Módulos Fases 1-3
├── fase4_menu_ui/
│   ├── spec.md
│   ├── progress.md
│   └── instalacion.md   # Este archivo
└── requirements.txt
```

## Ejecución

### Método 1: main.py (recomendado)

```bash
python main.py
```

### Método 2: menú como script

```bash
python menu_principal.py
```

### Método 3: módulo -m

```bash
python -m src.menu_principal
```

## Navegación

### Controles Básicos
- `↑/↓` o números: Seleccionar opción
- `Enter`: Confirmar
- `ESC` o `Ctrl+C`: Salir/cancelar

### Flujo Típico

1. **Alta de Persona**
   - Ingresar nombre (2-100 chars, solo letras)
   - Ingresar apellido (2-100 chars, solo letras)
   - Ingresar CUIL (formato XX-XXXXXXXX-X)
   - Confirmar
   - ✓ Mensaje de éxito/error

2. **Búsqueda**
   - Filtros opcionales (nombre, apellido, CUIL, fechas)
   - Límite y offset
   - Resultados en tabla paginada
   - Navegar páginas con `prev`/`next`

3. **Modificación**
   - Buscar por ID o CUIL
   - Editar campos (Enter para mantener)
   - Confirmar cambios

4. **Eliminación**
   - Buscar persona
   - Doble confirmación (seguridad)
   - Eliminar

5. **Reportes**
   - Submenú con 4 opciones
   - Ver resultados en tablas
   - Presionar tecla para volver

6. **Exportación**
   - Seleccionar formato (csv/xlsx/json/pdf)
   - Especificar ruta de archivo
   - Aplicar filtros opcionales
   - Confirmar exportación

## Personalización

### Modificar tiempo de espera entre pantallas
Editar `src/vistas.py` → función `waiting_key()` (cambiar mensaje).

### Cambiar colores
Editar `src/vistas.py` → funciones `print_header`, `print_message` (códigos Rich).

### Ajustar tamaño de página
En `PantallaBusqueda()` y `paginar_resultados()` modificar `page_size` (default 10).

## Troubleshooting Fase 4

### Error: "No module named 'rich'"
```bash
pip install rich
```

### Interfaz no se limpia entre pantallas
- Verificar que el terminal soporte secuencias de escape
- En Windows PowerShell: `$Host.UI.RawUI.WindowTitle` debe estar disponible
- Forzar limpieza manual con `cls` en `clear_screen()`

### Caracteres extraños en tablas
- Asegurar UTF-8 en consola
- Windows: `chcp 65001` en PowerShell antes de ejecutar

### Validación CUIL muy estricta
- Asegurar formato exacto: `20-12345678-9` (2-8-1)
- El formulario `input_cuil()` valida con regex

### No se ven colores
- `rich` detecta automáticamente soporte de color del terminal
- Forzar colores: `export TERM=xterm-256color` (Linux/Mac)
- Windows: usar Windows Terminal o conhost con color soportado

## Tests Fase 4

Aún no hay tests automatizados para interfaz CLI (pendiente Fase 5). Por ahora:

### Pruebas Manuales Recomendadas

1. **Alta**
   ```
   python main.py → 1 → Juan → Pérez → 20-12345678-9 → s
   ```

2. **Búsqueda**
   ```
   → 2 → Juan (filtro) → ver paginación (next/prev)
   ```

3. **Modificación**
   ```
   → 3 → ingresar ID → editar nombre → confirmar
   ```

4. **Eliminación**
   ```
   → 4 → ingresar CUIL → doble confirmación (s,s)
   ```

5. **Reportes**
   ```
   → 5 → 1 (estadísticas) → ver tabla
   → 5 → 3 (duplicados) → ver advertencia si hay
   ```

6. **Exportación**
   ```
   → 6 → csv → personas.csv → n (sin filtros) → ver archivo generado
   ```

## Siguiente Paso

Una vez probada la interfaz y verificado el flujo completo, se puede avanzar a **Fase 5: Entrega Final** (documentación, empaquetado, tests integrales).