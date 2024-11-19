from app.schemas.response_general import ResponseGeneral

class SaludoSimpleService:
    def __init__(self):
        pass
    
    def generar_saludo_simple(self) -> ResponseGeneral:
        response = ResponseGeneral(
            mensaje="Se genero bien el saludo",
            status=200,
            data={"message": "Hola, bienvenido al sistema!"}
        )
        
        return response