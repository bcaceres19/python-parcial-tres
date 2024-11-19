from app.schemas.response_general import ResponseGeneral

class SaludoPersonalizadoService:
    def __init__(self):
        pass
    
    def generar_saludo_personalizado(self, nombre) -> ResponseGeneral:
        response = ResponseGeneral(
            mensaje="Se genero bien el saludo",
            status=200,
            data={"message": f"Hola {nombre}"}
        )
        
        return response