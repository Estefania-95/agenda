# Checklist de Tareas - Fase 1: Infraestructura SQL Server

## Tareas Completadas
- [x] Crear estructura de carpetas phase1-5
- [x] Crear spec.md de fase 1 con requerimientos ODBC y connection string
- [x] Crear script SQL init_db.sql (create DB + tabla + índices)
- [x] Crear archivo .env.example con variables de entorno
- [x] Crear archivo .gitignore (log, __pycache__, .env)
- [x] Crear README.md con instrucciones generales
- [x] Crear requirements.txt con dependencias
- [x] Crear pyproject.toml para empaquetado
- [x] Implementar módulo src/database.py completo:
  - [x] Función conectar_db() con manejo de excepciones específico
  - [x] Función test_connection() para verificar conexión
  - [x] Funciones auxiliares ejecutar_query/ejecutar_non_query
  - [x] Uso de variables de entorno con python-dotenv
  - [x] Clase DatabaseConnectionError personalizada
  - [x] Bloque __main__ para prueba directa
- [x] Documentar connection string en spec.md
- [x] Crear logs/ para archivos de log operacionales

## Tareas Pendientes (Manuales del Usuario)
- [ ] Instalar ODBC Driver 17/18 for SQL Server
- [ ] Configurar instancia SQL Server (local o remota)
- [ ] Crear archivo .env con credenciales reales
- [ ] Ejecutar init_db.sql en instancia SQL Server
- [ ] Probar conexión con: `python src/database.py`
- [ ] Verificar tabla Personas creada correctamente

## Notas
- Las tareas pendientes requieren acción manual del usuario
- Una vez probada la conexión, avanzar a Fase 2 (CRUD Core)
