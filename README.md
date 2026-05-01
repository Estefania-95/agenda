# Sistema de Gestión Modular - SQL Server

Sistema de gestión模块ar con SQL Server y Python, siguiendo metodología por fases.

## Stack Técnico

- **Lenguaje**: Python 3.9+
- **Base de Datos**: SQL Server (Local/Remoto)
- **Conexión**: pyodbc
- **Driver**: ODBC Driver 17/18 for SQL Server
- **Variables de Entorno**: python-dotenv

## Estructura del Proyecto

```
agenda/
├── src/
│   └── database.py          # Módulo de conexión (Fase 1)
├── fase1_db_infra/          # Infraestructura DB
│   ├── spec.md              # Especificaciones técnicas
│   ├── progress.md          # Checklist de tareas
│   └── init_db.sql          # Script de inicialización
├── fase2_crud_core/         # Operaciones CRUD
├── fase3_busqueda_reportes/ # Búsqueda y reportes
├── fase4_menu_ui/           # Interfaz CLI
├── fase5_entrega_final/     # Empaquetado final
├── .env.example             # Variables de entorno de ejemplo
└── .gitignore               # Archivos ignorados por Git
```

## Instalación Rápida

### Prerrequisitos

1. **SQL Server** (Local o Remoto)
   - SQL Server Express (gratuito) o superior
   - Habilitar autenticación SQL Server (modo mixto)

2. **ODBC Driver** para SQL Server
   - Windows: [Descargar ODBC Driver](https://learn.microsoft.com/en-us/sql/connect/odbc/download-odbc-driver-for-sql-server)
   - Linux: `sudo apt-get install msodbcsql17`

3. **Python 3.9+**

### Pasos de Instalación

```bash
# 1. Clonar repositorio
git clone <repo-url>
cd agenda

# 2. Crear entorno virtual
python -m venv venv

# 3. Activar entorno
# Windows:
venv\Scripts\Activate.ps1
# Linux/Mac:
source venv/bin/activate

# 4. Instalar dependencias
pip install pyodbc python-dotenv

# 5. Configurar variables de entorno
cp .env.example .env
# Editar .env con valores de tu servidor SQL Server

# 6. Inicializar base de datos
# Ejecutar init_db.sql en SQL Server Management Studio o via sqlcmd:
# sqlcmd -S localhost\SQLEXPRESS -i fase1_db_infra/init_db.sql
```

## Configuración de Variables

Editar archivo `.env`:

```env
DB_SERVER=localhost\SQLEXPRESS   # ServidorSQL
DB_NAME=GestionDB                # Nombre de la base de datos
DB_UID=gestion_user              # Usuario SQL
DB_PWD=TuPasswordSegura123!      # Password del usuario
```

## Prueba de Conexión

```bash
# Ejecutar prueba de conexión Fase 1
python src/database.py
```

Salida esperada:
```
✓ Estado: True
✓ Mensaje: Conexión exitosa a SQL Server
✓ SQL Server: Microsoft SQL Server 2019...
¡Conexión exitosa!
```

## Desarrollo por Fases

- **Fase 1**: Infraestructura SQL Server (completada)
- **Fase 2**: CRUD Core (pendiente)
- **Fase 3**: Búsqueda y Reportes (pendiente)
- **Fase 4**: Menú e Interfaz de Usuario (pendiente)
- **Fase 5**: Entrega Final (pendiente)

Ver `faseX_*/spec.md` para detalles de cada fase.

## Troubleshooting

### Error: "Driver not found"
- Verificar instalación de ODBC Driver
- En Windows: Revisar en "ODBC Data Sources" (odbcad32.exe)

### Error: "Login failed for user"
- Verificar credenciales en .env
- Asegurar que SQL Server permite autenticación SQL
- Crear login en SQL Server si no existe

### Error: "Timeout expired"
- Verificar que SQL Server esté corriendo
- Revisar firewall (puerto 1433)
- Probar conexión con SQL Server Management Studio

## Licencia

Proyecto educativo - Uso libre.
