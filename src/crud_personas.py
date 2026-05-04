"""
Módulo CRUD para operaciones sobre la tabla Personas.
Fase 2: CRUD Core - Implementación completa con validaciones.
"""

import re
import logging
import pyodbc
from typing import Optional, Dict, List, Any
from datetime import datetime

# Módulos propios
from src.database import conectar_db, DatabaseConnectionError

# Configurar logging
logger = logging.getLogger(__name__)
handler = logging.FileHandler('logs/operaciones.log', encoding='utf-8')
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.INFO)


# ==============================================
# Excepciones personalizadas
# ==============================================
class ValidacionError(Exception):
    """Excepción para errores de validación de datos."""
    pass


class DuplicadoError(Exception):
    """Excepción para datos duplicados (CUIL ya existe)."""
    pass


# ==============================================
# Validaciones
# ==============================================
def validar_cuil(cuil: str) -> bool:
    """
    Valida el formato del CUIL: XX-XXXXXXXX-X (2-8-1 dígitos).

    Args:
        cuil: CUIL a validar.

    Returns:
        bool: True si es válido.

    Raises:
        ValidacionError: Si el formato es incorrecto.
    """
    patron = r'^\d{2}-\d{8}-\d{1}$'
    if not re.match(patron, cuil):
        raise ValidacionError(
            f"CUIL '{cuil}' formato inválido. "
            "Formato esperado: XX-XXXXXXXX-X (ej: 20-12345678-9)"
        )
    return True


def validar_nombre_apellido(nombre: str, campo: str = "nombre") -> bool:
    """
    Valida que nombre/apellido contenga solo letras y espacios.

    Args:
        nombre: Valor a validar.
        campo: Nombre del campo para mensajes de error.

    Returns:
        bool: True si es válido.

    Raises:
        ValidacionError: Si contiene caracteres no permitidos o longitud incorrecta.
    """
    if not nombre or not nombre.strip():
        raise ValidacionError(f"El campo '{campo}' no puede estar vacío.")

    nombre = nombre.strip()

    if len(nombre) < 2 or len(nombre) > 100:
        raise ValidacionError(
            f"El campo '{campo}' debe tener entre 2 y 100 caracteres. "
            f"Actual: {len(nombre)}"
        )

    # Solo letras y espacios
    if not re.match(r'^[a-zA-ZáéíóúÁÉÍÓÚñÑüÜ\s]+$', nombre):
        raise ValidacionError(
            f"El campo '{campo}' solo puede contener letras y espacios. "
            f"Valor: '{nombre}'"
        )

    return True


# ==============================================
# Operaciones CRUD
# ==============================================
def crear_persona(nombre: str, apellido: str, cuil: str) -> bool:
    """
    Crea una nueva persona en la base de datos.

    Args:
        nombre: Nombre de la persona.
        apellido: Apellido de la persona.
        cuil: CUIL (formato XX-XXXXXXXX-X, único).

    Returns:
        bool: True si se creó exitosamente.

    Raises:
        ValidacionError: Si los datos no pasan la validación.
        DuplicadoError: Si el CUIL ya existe.
        DatabaseConnectionError: Si hay error de base de datos.
    """
    # Validaciones
    validar_nombre_apellido(nombre, "nombre")
    validar_nombre_apellido(apellido, "apellido")
    validar_cuil(cuil)

    # Limpiar espacios
    nombre = nombre.strip()
    apellido = apellido.strip()
    cuil = cuil.strip()

    query = """
        INSERT INTO Personas (nombre, apellido, cuil)
        VALUES (?, ?, ?)
    """

    conn = None
    try:
        # No usar context manager: facilita mocking en unit tests.
        conn = conectar_db()
        cursor = conn.cursor()
        try:
            cursor.execute(query, (nombre, apellido, cuil))
            conn.commit()

            logger.info(
                f"Persona creada: {nombre} {apellido}, CUIL: {cuil}"
            )
            return True

        except pyodbc.IntegrityError as e:
            try:
                conn.rollback()
            except Exception:
                pass
            # Verificar si es violación de UNIQUE (CUIL duplicado)
            if 'UNIQUE' in str(e).upper() or 'DUPLICATE' in str(e).upper():
                raise DuplicadoError(
                    f"Ya existe una persona con CUIL '{cuil}'."
                ) from e
            raise

    except pyodbc.Error as e:
        logger.error(f"Error DB al crear persona: {e}")
        raise DatabaseConnectionError(f"Error de base de datos: {e}") from e
    finally:
        try:
            if conn is not None:
                conn.close()
        except Exception:
            pass


def obtener_persona(persona_id: int) -> Optional[Dict[str, Any]]:
    """
    Obtiene una persona por su ID.

    Args:
        persona_id: ID de la persona.

    Returns:
        dict | None: Datos de la persona o None si no existe.
    """
    if not isinstance(persona_id, int) or persona_id <= 0:
        return None

    query = """
        SELECT id, nombre, apellido, cuil, fecha_registro
        FROM Personas
        WHERE id = ?
    """

    conn = None
    try:
        conn = conectar_db()
        cursor = conn.cursor()
        cursor.execute(query, (persona_id,))
        row = cursor.fetchone()

        if row:
            desc = getattr(cursor, "description", None)
            if isinstance(desc, (list, tuple)) and desc:
                columns = [column[0] for column in desc]
            else:
                columns = ['id', 'nombre', 'apellido', 'cuil', 'fecha_registro']
            return dict(zip(columns, row))

        return None

    except pyodbc.Error as e:
        logger.error(f"Error DB al obtener persona id={persona_id}: {e}")
        raise DatabaseConnectionError(f"Error de base de datos: {e}") from e
    finally:
        try:
            if conn is not None:
                conn.close()
        except Exception:
            pass


def actualizar_persona(persona_id: int, **datos: Any) -> bool:
    """
    Actualiza datos de una persona existente.

    Args:
        persona_id: ID de la persona a actualizar.
        **datos: Campos a actualizar (nombre, apellido, cuil).

    Returns:
        bool: True si se actualizó al menos 1 fila.

    Raises:
        ValidacionError: Si los datos no son válidos.
        DuplicadoError: Si el nuevo CUIL ya existe en otro registro.
    """
    # Validar que se envíen campos válidos
    campos_permitidos = {'nombre', 'apellido', 'cuil'}
    datos_filtrados = {k: v for k, v in datos.items() if k in campos_permitidos}

    if not datos_filtrados:
        raise ValidacionError("No se especificaron campos para actualizar.")

    # Validar cada campo proporcionado
    if 'nombre' in datos_filtrados:
        validar_nombre_apellido(datos_filtrados['nombre'], "nombre")
        datos_filtrados['nombre'] = datos_filtrados['nombre'].strip()

    if 'apellido' in datos_filtrados:
        validar_nombre_apellido(datos_filtrados['apellido'], "apellido")
        datos_filtrados['apellido'] = datos_filtrados['apellido'].strip()

    if 'cuil' in datos_filtrados:
        validar_cuil(datos_filtrados['cuil'])
        datos_filtrados['cuil'] = datos_filtrados['cuil'].strip()

    # Construir dinámicamente la consulta UPDATE
    set_clause = ", ".join([f"{campo} = ?" for campo in datos_filtrados.keys()])
    query = f"UPDATE Personas SET {set_clause} WHERE id = ?"

    params = list(datos_filtrados.values()) + [persona_id]

    conn = None
    try:
        conn = conectar_db()
        cursor = conn.cursor()
        try:
            cursor.execute(query, tuple(params))
            conn.commit()

            if cursor.rowcount == 0:
                return False  # No se encontró la persona

            logger.info(
                f"Persona actualizada id={persona_id}, campos: {list(datos_filtrados.keys())}"
            )
            return True

        except pyodbc.IntegrityError as e:
            try:
                conn.rollback()
            except Exception:
                pass
            if 'UNIQUE' in str(e).upper() or 'DUPLICATE' in str(e).upper():
                raise DuplicadoError(
                    f"El CUIL '{datos_filtrados.get('cuil')}' ya existe en otro registro."
                ) from e
            raise

    except pyodbc.Error as e:
        logger.error(f"Error DB al actualizar persona id={persona_id}: {e}")
        raise DatabaseConnectionError(f"Error de base de datos: {e}") from e
    finally:
        try:
            if conn is not None:
                conn.close()
        except Exception:
            pass


def eliminar_persona(persona_id: int) -> bool:
    """
    Elimina una persona por su ID.

    Args:
        persona_id: ID de la persona a eliminar.

    Returns:
        bool: True si se eliminó (existía), False si no existía.
    """
    if not isinstance(persona_id, int) or persona_id <= 0:
        return False

    query = "DELETE FROM Personas WHERE id = ?"

    conn = None
    try:
        conn = conectar_db()
        cursor = conn.cursor()
        cursor.execute(query, (persona_id,))
        conn.commit()

        if cursor.rowcount == 0:
            logger.warning(f"Intento de eliminar persona inexistente id={persona_id}")
            return False

        logger.info(f"Persona eliminada id={persona_id}")
        return True

    except pyodbc.Error as e:
        logger.error(f"Error DB al eliminar persona id={persona_id}: {e}")
        raise DatabaseConnectionError(f"Error de base de datos: {e}") from e
    finally:
        try:
            if conn is not None:
                conn.close()
        except Exception:
            pass


def listar_personas(
    nombre: Optional[str] = None,
    apellido: Optional[str] = None,
    cuil: Optional[str] = None,
    fecha_desde: Optional[datetime] = None,
    fecha_hasta: Optional[datetime] = None,
    limit: int = 100,
    offset: int = 0
) -> List[Dict[str, Any]]:
    """
    Lista personas con filtros opcionales y paginación.

    Args:
        nombre: Filtrar por nombre (LIKE).
        apellido: Filtrar por apellido (LIKE).
        cuil: Filtrar por CUIL exacto.
        fecha_desde: Fecha de registro desde (inclusive).
        fecha_hasta: Fecha de registro hasta (inclusive).
        limit: Límite de resultados (max 1000).
        offset: Desplazamiento para paginación.

    Returns:
        List[dict]: Lista de personas que coinciden con los filtros.
    """
    # Validar límite
    limit = min(limit, 1000)

    # Construir query dinámicamente
    base_query = "SELECT id, nombre, apellido, cuil, fecha_registro FROM Personas WHERE 1=1"
    params = []

    # Aplicar filtros
    if nombre:
        base_query += " AND nombre LIKE ?"
        params.append(f"%{nombre.strip()}%")

    if apellido:
        base_query += " AND apellido LIKE ?"
        params.append(f"%{apellido.strip()}%")

    if cuil:
        validar_cuil(cuil)
        base_query += " AND cuil = ?"
        params.append(cuil.strip())

    if fecha_desde:
        base_query += " AND fecha_registro >= ?"
        params.append(fecha_desde)

    if fecha_hasta:
        base_query += " AND fecha_registro <= ?"
        params.append(fecha_hasta)

    # Ordenar y paginar
    base_query += " ORDER BY apellido, nombre, id DESC OFFSET ? ROWS FETCH NEXT ? ROWS ONLY"
    params.extend([offset, limit])

    conn = None
    try:
        conn = conectar_db()
        cursor = conn.cursor()
        cursor.execute(base_query, tuple(params))
        rows = cursor.fetchall()

        columns = [column[0] for column in cursor.description]
        resultados = [dict(zip(columns, row)) for row in rows]

        logger.info(
            f"Listado personas: filtros={dict(nombre=nombre, apellido=apellido, cuil=cuil)}, "
            f"total_encontrado={len(resultados)}"
        )
        return resultados

    except pyodbc.Error as e:
        logger.error(f"Error DB al listar personas: {e}")
        raise DatabaseConnectionError(f"Error de base de datos: {e}") from e
    finally:
        try:
            if conn is not None:
                conn.close()
        except Exception:
            pass


def contar_personas(
    nombre: Optional[str] = None,
    apellido: Optional[str] = None,
    cuil: Optional[str] = None
) -> int:
    """
    Cuenta el total de personas que coinciden con los filtros.

    Args:
        nombre, apellido, cuil: Filtros opcionales.

    Returns:
        int: Cantidad total.
    """
    base_query = "SELECT COUNT(*) FROM Personas WHERE 1=1"
    params = []

    if nombre:
        base_query += " AND nombre LIKE ?"
        params.append(f"%{nombre.strip()}%")

    if apellido:
        base_query += " AND apellido LIKE ?"
        params.append(f"%{apellido.strip()}%")

    if cuil:
        base_query += " AND cuil = ?"
        params.append(cuil.strip())

    conn = None
    try:
        conn = conectar_db()
        cursor = conn.cursor()
        cursor.execute(base_query, tuple(params))
        row = cursor.fetchone()
        return row[0] if row else 0

    except pyodbc.Error as e:
        logger.error(f"Error DB al contar personas: {e}")
        raise DatabaseConnectionError(f"Error de base de datos: {e}") from e
    finally:
        try:
            if conn is not None:
                conn.close()
        except Exception:
            pass
