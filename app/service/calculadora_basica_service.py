from typing import Union
from fastapi import HTTPException
from app.schemas.response_general import ResponseGeneral
from app.core.logger import log_error


class CalculadoraBasicaService:
    """
    Servicio para realizar operaciones básicas de cálculo.
    """

    def __init__(self):
        pass

    def generar_proceso_calculadora(
        self, operador: str, numero_uno: Union[int, float], numero_dos: Union[int, float]
    ) -> ResponseGeneral:
        """
        Realiza una operación matemática básica entre dos números.

        Args:
            operador (str): Operador matemático (+, -, *, /).
            numero_uno (Union[int, float]): Primer número.
            numero_dos (Union[int, float]): Segundo número.

        Returns:
            ResponseGeneral: Resultado de la operación o error en caso de fallo.
        """
        # Validar el operador
        if operador not in {"+", "-", "*", "/"}:
            raise HTTPException(status_code=400, detail="Operador no válido. Solo se permiten +, -, *, /")

        # Realizar la operación
        try:
            resultado = self._realizar_operacion(operador, numero_uno, numero_dos)
        except ZeroDivisionError as e:
            log_error(e)
            raise HTTPException(status_code=400, detail="División por cero no permitida.")
        except Exception as e:
            log_error(e)
            raise HTTPException(status_code=500, detail=f"Error al realizar la operación: {str(e)}")

        # Crear y devolver la respuesta
        return ResponseGeneral(
            mensaje="Operación realizada correctamente.",
            status=200,
            data={"resultado": resultado}
        )

    def _realizar_operacion(self, operador: str, numero_uno: Union[int, float], numero_dos: Union[int, float]) -> float:
        """
        Realiza la operación matemática según el operador proporcionado.

        Args:
            operador (str): Operador matemático (+, -, *, /).
            numero_uno (Union[int, float]): Primer número.
            numero_dos (Union[int, float]): Segundo número.

        Returns:
            float: Resultado de la operación.
        """
        if operador == "+":
            return numero_uno + numero_dos
        elif operador == "-":
            return numero_uno - numero_dos
        elif operador == "*":
            return numero_uno * numero_dos
        elif operador == "/":
            if numero_dos == 0:
                raise ZeroDivisionError("División por cero no permitida.")
            return numero_uno / numero_dos
