from google.adk import Agent
from general_agent import agente_general
from math_agent import agente_matematico

router_agente = Agent(
    name="Router_Agent",
    instruction=(
        "Eres un agente orquestador. Tu trabajo es identificar la intención "
        "del usuario y delegar al agente especialista correcto. "
        "Si el tema es matemático, delega al Agente_Matematico. "
        "Si es una duda general, delega al Agente_General. "
        "No respondas tú directamente — siempre delega."
    ),
    model="gemini-2.5-flash-lite",
    sub_agents=[agente_general, agente_matematico],
)
