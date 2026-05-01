# Checklist de Tareas - Fase 1: Infraestructura SQL Server

## Tareas Pendientes
- [ ] Probar conexión con servidor SQL Server real
- [ ] Ejecutar init_db.sql en instancia
- [ ] Verificar tabla Personas creada correctamente
- [ ] Documentar connection string específico en README
- [ ] Actualizar progress.md con tareas completadas

## Tareas Completadas
- [x] Crear estructura de carpetas phase1-5
- [x] Crear spec.md de fase 1
- [x] Crear script SQL init_db.sql (create DB + tabla + índices)
- [x] Crear archivo .env.example
- [x] Crear archivo .gitignore
- [x] Crear README.md con instrucciones generales
- [x] Crear requirements.txt con dependencias
- [x] Crear pyproject.toml para empaquetado
- [x] Implementar módulo src/database.py con:
  - [x] Función conectar_db() con manejo de excepciones
  - [x] Función test_connection() para verificar conexión
  - [x] Funciones auxiliares ejecutar_query/ejecutar_non_query
  - [x] Uso de variables de entorno con python-dotenv
  - [x] Clase DatabaseConnectionError personalizada

## Notas
- Asegurar password segura para usuario DB
- Documentar configuración específica de entorno
- Validar que el driver ODBC esté en PATH
