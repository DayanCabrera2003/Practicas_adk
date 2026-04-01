from google.adk import Agent

# Este agente es el maestro de orquesta se encarga de  recibir la consulta del usuario
# e identificar a que agente especialista debe derivar la consulta.
router_agente = Agent(
    name="Router_Agent",
    instruction=(
        "Eres un agente orquestador. Tu trabajo no es responder en detalle, "
        "sino identificar la intención del usuario y dirigir la consulta al "
        "agente especialista correcto. Si el tema es matematico, deriva al "
        "agente matematico. Si es una duda general, deriva al agente general. "
        "Si no entiendes, pide aclaracion."
    ),
    model="gemini-2.5-flash-lite",
)