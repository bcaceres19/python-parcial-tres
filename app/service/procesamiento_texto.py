from app.schemas.response_general import ResponseGeneral
from app.schemas.text_input import TextInput
from app.schemas.text_response import TextResponse


class ProcesamientoTextoService:
    """
    Servicio para procesar texto y calcular estadísticas.
    """

    def procesar_texto(self, input: TextInput) -> ResponseGeneral:
        """
        Procesa el texto proporcionado y devuelve estadísticas como número
        de palabras, caracteres y el texto en mayúsculas.

        Args:
            input (TextInput): Objeto que contiene el texto a procesar.

        Returns:
            ResponseGeneral: Respuesta con las estadísticas del texto.
        """
        # Calcular estadísticas del texto
        text_response = self._calcular_estadisticas(input.texto)

        # Crear la respuesta general
        return ResponseGeneral(
            mensaje="Se procesó correctamente el texto",
            status=200,
            data=text_response.model_dump()
        )

    @staticmethod
    def _calcular_estadisticas(texto: str) -> TextResponse:
        """
        Calcula las estadísticas del texto.

        Args:
            texto (str): Texto para procesar.

        Returns:
            TextResponse: Estadísticas calculadas.
        """
        return TextResponse(
            numero_palabras=len(texto.split()),
            numero_caracteres=len(texto),
            texto_mayusculas=texto.upper()
        )
