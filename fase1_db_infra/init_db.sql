-- =====================================================
-- Script de Inicialización - Base de Datos GestionDB
-- Fase 1: Infraestructura SQL Server
-- =====================================================

-- 1. Crear base de datos si no existe
IF NOT EXISTS (SELECT name FROM sys.databases WHERE name = 'GestionDB')
BEGIN
    CREATE DATABASE GestionDB;
    PRINT 'Base de datos GestionDB creada.';
END
ELSE
BEGIN
    PRINT 'Base de datos GestionDB ya existe.';
END
GO

-- 2. Usar la base de datos GestionDB
USE GestionDB;
GO

-- 3. Crear tabla Personas si no existe
IF NOT EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[Personas]') AND type in (N'U'))
BEGIN
    CREATE TABLE [dbo].[Personas] (
        [id] INT IDENTITY(1,1) NOT NULL PRIMARY KEY,
        [nombre] NVARCHAR(100) NOT NULL,
        [apellido] NVARCHAR(100) NOT NULL,
        [cuil] VARCHAR(13) NOT NULL UNIQUE,
        [fecha_registro] DATETIME NOT NULL DEFAULT GETDATE()
    );

    PRINT 'Tabla Personas creada.';

    -- 3.1. Crear índices para optimizar búsquedas
    CREATE NONCLUSTERED INDEX IX_Personas_Cuil ON [dbo].[Personas] (cuil);
    CREATE NONCLUSTERED INDEX IX_Personas_Nombre ON [dbo].[Personas] (nombre, apellido);
    CREATE NONCLUSTERED INDEX IX_Personas_FechaRegistro ON [dbo].[Personas] (fecha_registro DESC);

    PRINT 'Índices creados.';
END
ELSE
BEGIN
    PRINT 'Tabla Personas ya existe.';
END
GO

-- 4. Crear usuario de aplicación (opcional - ejecutar manualmente con password segura)
/*
CREATE LOGIN gestion_user WITH PASSWORD = 'ChangeMe_123!';
USE GestionDB;
CREATE USER gestion_user FOR LOGIN gestion_user;
EXEC sp_addrolemember 'db_datawriter', 'gestion_user';
EXEC sp_addrolemember 'db_datareader', 'gestion_user';
*/

-- 5. Verificación final
SELECT
    DB_NAME() as BaseDeDatos,
    COUNT(*) as TotalTablas
FROM sys.tables
WHERE name = 'Personas';

PRINT 'Script de inicialización completado.';
