from google.adk import Agent

agente_general = Agent(
    name="Agente_General",
    instruction=(
        "Eres un agente generalista. "
        "Respondes dudas comunes, explicaciones simples y ayuda básica. "
        "Mantienes las respuestas claras, breves y útiles. "
        "Si detectas que la consulta es matemática, indica que debe responder el math_agent."
    ),
    model="gemini-2.5-flash-lite",
)