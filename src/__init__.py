# Paquete src - Sistema de Gestión Modular
# Organización de módulos por fases

# Fase 1: Database
from src.database import conectar_db, test_connection, DatabaseConnectionError

# Fase 2: CRUD
from src.crud_personas import (
    crear_persona,
    obtener_persona,
    actualizar_persona,
    eliminar_persona,
    listar_personas,
    contar_personas,
    validar_cuil,
    validar_nombre_apellido,
    ValidacionError,
    DuplicadoError
)

# Fase 3: Búsqueda y Reportes
from src.buscador import (
    buscar_personas,
    buscar_por_cuil,
    buscar_por_nombre,
    buscar_por_fecha,
    busqueda_avanzada,
    buscar_duplicados_cuil,
    sugerir_busqueda
)

from src.reportes import (
    reporte_personas_por_fecha,
    reporte_duplicados_cuil,
    reporte_estadisticas_generales,
    reporte_resumen_mensual,
    generar_reporte_completo
)

from src.exportadores import (
    exportar_a_csv,
    exportar_a_xlsx,
    exportar_a_json,
    exportar_a_pdf,
    obtener_exportador,
    validar_formato_archivo
)

__all__ = [
    # Database
    'conectar_db', 'test_connection', 'DatabaseConnectionError',
    # CRUD
    'crear_persona', 'obtener_persona', 'actualizar_persona', 'eliminar_persona',
    'listar_personas', 'contar_personas', 'validar_cuil', 'validar_nombre_apellido',
    'ValidacionError', 'DuplicadoError',
    # Búsqueda
    'buscar_personas', 'buscar_por_cuil', 'buscar_por_nombre', 'buscar_por_fecha',
    'busqueda_avanzada', 'buscar_duplicados_cuil', 'sugerir_busqueda',
    # Reportes
    'reporte_personas_por_fecha', 'reporte_duplicados_cuil',
    'reporte_estadisticas_generales', 'reporte_resumen_mensual', 'generar_reporte_completo',
    # Exportación
    'exportar_a_csv', 'exportar_a_xlsx', 'exportar_a_json', 'exportar_a_pdf',
    'obtener_exportador', 'validar_formato_archivo'
]
