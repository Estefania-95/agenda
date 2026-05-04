# Guía de Uso - Interfaz CLI (Fase 4)

La interfaz de usuario basada en consola permite gestionar la agenda de personas de forma interactiva.

## Requisitos
Asegúrate de tener instaladas las dependencias:
```bash
pip install -r requirements.txt
```

## Cómo Iniciar
Desde la raíz del proyecto, ejecuta:
```bash
python main.py
```

## Navegación
- **Flechas Arriba/Abajo**: Navegar entre las opciones del menú.
- **Enter**: Seleccionar una opción o confirmar entrada.
- **Ctrl+C**: Cancelar la operación actual y volver al menú anterior.
- **ESC**: En algunos diálogos, permite salir.

## Funcionalidades
1. **Alta de Persona**: Formulario con validación de nombre, apellido y CUIL.
2. **Listado / Búsqueda**: 
   - Deja el campo vacío para ver todos (limitado a 50).
   - Ingresa un nombre, apellido o CUIL para buscar.
3. **Modificación**: Requiere el ID de la persona (puedes obtenerlo en la búsqueda).
4. **Baja**: Eliminación permanente con confirmación previa.
5. **Reportes**: Resumen estadístico de la base de datos.
6. **Exportar**: Genera archivos CSV, XLSX, JSON o PDF con los datos actuales.

---
*Nota: Si la base de datos está vacía, usa `python src/seed_db.py` para cargar datos de prueba.*
