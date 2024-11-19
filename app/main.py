from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from mangum import Mangum  # Adaptador para AWS Lambda
from fastapi.middleware.cors import CORSMiddleware

from app.api import lambda_controller
from app.core.config import config


def create_app() -> FastAPI:
    """
    Crea una instancia de la aplicación FastAPI con la configuración adecuada.
    """
    app = FastAPI(
        title=config.APP_NAME,
        debug=config.DEBUG
    )
    
    # TODO: Add these lines
    app.add_middleware(
        CORSMiddleware,
        allow_origins='*',
        allow_credentials=False,
        allow_methods=["GET", "POST", "OPTIONS"],
        allow_headers=["x-apigateway-header", "Content-Type", "X-Amz-Date"],
    )

    # Registrar rutas con prefijos si es necesario
    api_prefix = config.RUTA_BASE if config.RUTA_BASE else ""
    app.include_router(lambda_controller.router, prefix=f"{api_prefix}/lambdas")


    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):  # pylint: disable=unused-argument
        """
        Manejador personalizado para excepciones de validación en FastAPI.
        """
        errors = []
        for error in exc.errors():
            # Obtener el campo que falló en la validación
            field = error.get("loc", ["unknown"])[-1]
            # Obtener el mensaje de error, manejar si no tiene el formato esperado
            raw_message = error.get("msg", "Error de validación desconocido")
            message = raw_message.split(",")[1].strip() if "," in raw_message else raw_message
            # Obtener el valor de entrada si está disponible
            input_value = error.get("input", None)

            # Construir el error personalizado
            custom_error = {
                "type": error.get("type", "unknown"),
                "field": field,
                "message": message,
                "input": input_value,
            }
            errors.append(custom_error)

        # Devolver respuesta personalizada en formato JSON
        return JSONResponse(
            status_code=400,
            content={"detail": errors},
        )


    return app


# Instancia de la aplicación
app = create_app()

# Handler para AWS Lambda
handler = Mangum(app)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",  # Llama directamente a la instancia `app`
        host="127.0.0.1",
        port=8084,
        log_level="debug",
        reload=config.DEBUG  # Habilita reload solo si estás en modo debug
    )
