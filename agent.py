from google import adk
from google.adk import Agent

def multiplicar_numeros(a: float, b: float) -> float:
    """Multiplica dos números de forma exacta.
    
    Usa esta herramienta cuando el usuario te pida multiplicar cifras
    o resolver cálculos matemáticos que involucren multiplicación.
    
    Args:
        a: El primer número.
        b: El segundo número.
    """
    return a * b

#Empezar definiendo el agente y su comportamiento base.
mi_primer_agente = Agent (
    #Para que el nombre del agente sea valido no debe tener espacios, caracteres especiales o acentos
    name="Asistente_Personal",
    instruction = ("Eres un asistente de IA muy amable y experto en tecnología. "
        "Ayuda al usuario a resolver sus dudas de manera concisa."),
    model="gemini-2.5-flash-lite",
    #Estas serian herramientas que le damos al modelo, el ejemplo es claramente super basico,
    #pero puedes agregarle herramientas de todo tipo, desde calculadoras, 
    # hasta acceso a bases de datos o APIs externas.
    tools=[multiplicar_numeros]
)
#Importante: Puedes obtener una API key gratuita de gemini en: https://aistudio.google.com/apikey
#Para probar es mas que suficiente con la API key gratuita.
