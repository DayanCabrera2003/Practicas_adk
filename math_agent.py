from google.adk import Agent

def sumar_numeros(a: float, b: float) -> float:
    """Suma dos numeros."""
    return a + b

def restar_numeros(a: float, b: float) -> float:
    """Resta dos numeros."""
    return a - b

def multiplicar_numeros(a: float, b: float) -> float:
    """Multiplica dos numeros."""
    return a * b

def dividir_numeros(a: float, b: float) -> float:
    """Divide dos numeros."""
    if b == 0:
        raise ValueError("No se puede dividir por cero.")
    return a / b

agente_matematico = Agent(
    name="Agente_Matematico",
    instruction=(
        "Eres un agente experto en matematicas. "
        "Resuelves sumas, restas, multiplicaciones, divisiones y otros calculos. "
        "Explicas el procedimiento de forma breve y clara. "
        "Si la consulta no es matematica, indica que debe responder el router."
    ),
    model="gemini-2.5-flash-lite",
    tools=[sumar_numeros, restar_numeros, multiplicar_numeros, dividir_numeros],
)