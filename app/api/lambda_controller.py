from typing import Union
from fastapi import APIRouter, HTTPException
from app.core.dynamo_db_connection import DynamoDBConnection
from app.schemas.estudiantes import Estudiantes
from app.schemas.response_general import ResponseGeneral
from app.service.guardar_estudiante_service import GuardarEstudianteService
from app.service.consultar_estudiante_service import ConsultarEstudianteService

# Crear instancia de router para manejar las rutas de DynamoDB
router = APIRouter(
    tags=["DynamoDB Operations"]
)

@router.post("/crear-estudiante", response_model=ResponseGeneral)
def crear_estudiante_dynamo(estudiante: Estudiantes):
    service = GuardarEstudianteService()
    response = service.guardar_estudiante(estudiante)

    if response.status != 201:
        raise HTTPException(status_code=response.status, detail=response.mensaje)

    return response



@router.get("/consultar-estudiante-id", response_model=ResponseGeneral)
def consultar_estudiante_dynamo(idEstudiante: str):
    service = ConsultarEstudianteService()
    response = service.consultar_estudiante_id(idEstudiante)

    if response.status != 200:
        raise HTTPException(status_code=response.status, detail=response.mensaje)

    return response

