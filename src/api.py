"""
API REST para el Sistema de Gestión de Agenda - Fase 6 (Web Bridge).
Exprime la lógica de negocio a través de FastAPI.
"""

import os
from typing import List, Optional
from fastapi import FastAPI, HTTPException, Query, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field
from datetime import datetime

# Módulos del proyecto
from src.crud_personas import (
    crear_persona, 
    obtener_persona, 
    actualizar_persona, 
    eliminar_persona,
    ValidacionError,
    DuplicadoError
)
from src.buscador import buscar_personas, busqueda_avanzada
from src.reportes import reporte_estadisticas_generales
from src.exportadores import obtener_exportador

app = FastAPI(
    title="Agenda API",
    description="API para la gestión modular de personas con SQL Server",
    version="1.0.0"
)

# Configuración de CORS para Next.js
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, restringir a la URL del frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Modelos de Datos (Pydantic) ---

class PersonaSchema(BaseModel):
    nombre: str = Field(..., min_length=2, max_length=100)
    apellido: str = Field(..., min_length=2, max_length=100)
    cuil: str = Field(..., pattern=r'^\d{2}-\d{8}-\d{1}$')

class PersonaUpdateSchema(BaseModel):
    nombre: Optional[str] = Field(None, min_length=2, max_length=100)
    apellido: Optional[str] = Field(None, min_length=2, max_length=100)
    cuil: Optional[str] = Field(None, pattern=r'^\d{2}-\d{8}-\d{1}$')

# --- Endpoints ---

@app.get("/", tags=["General"])
def read_root():
    return {"message": "Agenda API is running", "status": "online"}

@app.get("/personas", tags=["Personas"])
def get_personas(
    q: Optional[str] = Query(None, description="Término de búsqueda unificada"),
    limit: int = 50,
    offset: int = 0
):
    """Lista personas con búsqueda opcional."""
    try:
        if q:
            resultados = busqueda_avanzada(q)
            return {"resultados": resultados, "total": len(resultados)}
        else:
            return buscar_personas(limit=limit, offset=offset)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/personas/{persona_id}", tags=["Personas"])
def get_persona(persona_id: int):
    """Obtiene una persona específica."""
    persona = obtener_persona(persona_id)
    if not persona:
        raise HTTPException(status_code=404, detail="Persona no encontrada")
    return persona

@app.post("/personas", status_code=status.HTTP_201_CREATED, tags=["Personas"])
def post_persona(persona: PersonaSchema):
    """Crea una nueva persona."""
    try:
        if crear_persona(persona.nombre, persona.apellido, persona.cuil):
            return {"message": "Creado con éxito", "cuil": persona.cuil}
    except DuplicadoError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except ValidacionError as e:
        raise HTTPException(status_code=422, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno: {e}")

@app.put("/personas/{persona_id}", tags=["Personas"])
def put_persona(persona_id: int, datos: PersonaUpdateSchema):
    """Actualiza una persona existente."""
    update_data = {k: v for k, v in datos.dict().items() if v is not None}
    if not update_data:
        raise HTTPException(status_code=400, detail="No se enviaron datos para actualizar")
    
    try:
        if actualizar_persona(persona_id, **update_data):
            return {"message": "Actualizado con éxito"}
        else:
            raise HTTPException(status_code=404, detail="Persona no encontrada")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.delete("/personas/{persona_id}", tags=["Personas"])
def delete_persona(persona_id: int):
    """Elimina una persona."""
    if eliminar_persona(persona_id):
        return {"message": "Eliminado con éxito"}
    else:
        raise HTTPException(status_code=404, detail="Persona no encontrada o ya eliminada")

@app.get("/stats", tags=["Reportes"])
def get_stats():
    """Obtiene estadísticas generales."""
    try:
        return reporte_estadisticas_generales()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/exportar/{formato}", tags=["Exportar"])
def export_data(formato: str):
    """Genera y descarga un archivo de exportación."""
    formatos_validos = ['csv', 'xlsx', 'json', 'pdf']
    if formato not in formatos_validos:
        raise HTTPException(status_code=400, detail="Formato no soportado")
    
    try:
        resp = buscar_personas(limit=1000)
        datos = resp['resultados']
        filename = f"export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.{formato}"
        filepath = os.path.join("exports", filename)
        
        # Asegurar directorio de exportación
        os.makedirs("exports", exist_ok=True)
        
        exportador = obtener_exportador(formato)
        exportador(datos, filepath)
        
        return FileResponse(
            path=filepath, 
            filename=filename, 
            media_type='application/octet-stream'
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
