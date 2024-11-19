from typing import Union
from fastapi import APIRouter, HTTPException
from app.core.dynamo_db_connection import DynamoDBConnection
from app.schemas.estudiantes import Estudiantes
from app.schemas.response_general import ResponseGeneral
from app.service.guardar_estudiante_service import GuardarEstudianteService
from app.service.consultar_estudiante_service import ConsultarEstudianteService


router = APIRouter(
    tags=["lambdas"]
)

# Mejoras en los endpoints de DynamoDB

@router.post("/crear-estudiante", response_model=ResponseGeneral)
def crear_estudiante_dynamo(estudiante: Estudiantes):
    """
    Endpoint para crear un estudiante en DynamoDB.
    """
    service = GuardarEstudianteService()
    return service.guardar_estudiante(estudiante)


@router.get("/consultar-estudiante-id", response_model=ResponseGeneral)
def consultar_estudiante_dynamo(idEstudiante: str):
    """
    Endpoint para consultar un estudiante por ID en DynamoDB.
    """
    service = ConsultarEstudianteService()
    return service.consultar_estudiante_id(idEstudiante)