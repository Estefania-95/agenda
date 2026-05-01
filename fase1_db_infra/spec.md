# Especificaciones Técnicas - Fase 1: Infraestructura SQL Server

## Objetivo
Establecer la conexión confiable con SQL Server y crear el esquema inicial de la base de datos.

## Requerimientos Técnicos

### Driver ODBC
- **Driver**: ODBC Driver 17/18 for SQL Server
- ** Plataforma**: Windows/Linux
- **Instalación**: 
  - Windows: Descargar desde Microsoft Downloads
  - Linux: `sudo apt-get install msodbcsql17` (Ubuntu/Debian)

### Connection String (pyodbc)
```
Driver={ODBC Driver 17 for SQL Server};
Server={SERVER_NAME};
Database={DATABASE_NAME};
UID={USERNAME};
PWD={PASSWORD};
TrustServerCertificate=yes;
Timeout=30;
```

### Configuración de Instancia SQL Server

#### Instancia Local (Desarrollo)
```sql
-- Habilitar autenticación SQL Server y Mixed Mode
-- Crear login y usuario para la aplicación
CREATE LOGIN gestion_user WITH PASSWORD = 'SecurePass123!';
USE GestionDB;
CREATE USER gestion_user FOR LOGIN gestion_user;
EXEC sp_addrolemember 'db_datawriter', 'gestion_user';
EXEC sp_addrolemember 'db_datareader', 'gestion_user';
```

#### Instancia Remota (Producción)
- Usar IP o nombre de servidor DNS
- Configurar firewall para puerto 1433
- Habilitar conexiones remotas en SQL Server Configuration Manager
- Considerar SSL/TLS encryption

### Variables de Entorno Requeridas
```env
DB_SERVER=localhost\SQLEXPRESS o 192.168.1.100
DB_NAME=GestionDB
DB_UID=gestion_user
DB_PWD=tu_password_seguro
```

### Script SQL Inicial
- Creación de base de datos `GestionDB`
- Tabla `Personas` con campos: id, nombre, apellido, cuil (UNIQUE), fecha_registro
- Índices para optimización de búsquedas

## Entregables
1. Script SQL de inicialización (`init_db.sql`)
2. Módulo `database.py` con conexión pyodbc
3. Archivo `.env.example` con configuración de referencia
4. Prueba de conexión implementada

## Criterios de Éxito
- [ ] Conexión exitosa a SQL Server
- [ ] Base de datos y tabla creadas
- [ ] Script ejecutable sin errores
- [ ] Módulo database.py pasa prueba de conexión
