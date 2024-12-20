from typing import Union
from fastapi import APIRouter, HTTPException
from app.core.dynamo_db_connection import DynamoDBConnection
from app.schemas.estudiantes import Estudiantes
from app.schemas.response_general import ResponseGeneral
from app.schemas.text_input import TextInput
from app.service.calculadora_basica_service import CalculadoraBasicaService
from app.service.guardar_estudiante_service import GuardarEstudianteService
from app.service.consultar_estudiante_service import ConsultarEstudianteService
from app.service.procesamiento_texto import ProcesamientoTextoService
from app.service.saludo_personalizado_service import SaludoPersonalizadoService
from app.service.saludo_simple_service import SaludoSimpleService

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

@router.get("/calculadora-basica", response_model=ResponseGeneral)
def calculadora_basica(numeroUno: Union[int, float], numeroDos: Union[int, float], operador: str):
    service = CalculadoraBasicaService()
    return service.generar_proceso_calculadora(operador, numeroUno, numeroDos)


@router.post("/procesamiento-texto", response_model=ResponseGeneral)
def procesamiento_texto(input_text: TextInput):
    service = ProcesamientoTextoService()
    return service.procesar_texto(input_text)


@router.get("/saludo-simple", response_model=ResponseGeneral)
def saludo_simple():
    service = SaludoSimpleService()
    return service.generar_saludo_simple()


@router.get("/saludo-personalizado", response_model=ResponseGeneral)
def saludo_personalizado(nombre: str):
    service = SaludoPersonalizadoService()
    return service.generar_saludo_personalizado(nombre)

