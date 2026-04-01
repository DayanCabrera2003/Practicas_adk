import asyncio
from google import adk
from google.adk.sessions import InMemorySessionService
from google.genai import types
from agent import mi_primer_agente
APP_NAME = "asistente_app"
USER_ID = "usuario_1"

async def main():
    """
    Bucle principal del chat por consola.

    Flujo general:
    1) Crea un servicio de sesión en memoria.
    2) Crea una sesión para el usuario.
    3) Crea un Runner de ADK con el agente.
    4) Lee mensajes desde la terminal.
    5) Envía cada mensaje al agente.
    6) Consume eventos de respuesta y muestra el texto final.
    """
    print("Iniciando sesión con el agente de ADK...")
    # Servicio de sesiones efimero (vive mientras corre el proceso).
    session_service = InMemorySessionService()

    # Se crea una sesión nueva asociada a APP_NAME + USER_ID.
    session = await session_service.create_session(app_name=APP_NAME, user_id=USER_ID)

    # Runner: componente que orquesta el ciclo del agente.
    # Le pasamos el agente, app_name y cómo administrar sesiones.
    runner = adk.Runner(
        app_name=APP_NAME,
        agent=mi_primer_agente,
        session_service=session_service,
    )

    while True:
        try:
            user_input = input("\nTú: ")
            if user_input.lower() in ["salir", "exit", "quit"]:
                break
            
            # Empaqueta el texto del usuario en el formato esperado por Gemini.
            # role="user" indica quien habla.
            message = types.Content(
                role="user",
                parts=[types.Part(text=user_input)],
            )

            response_text = ""

            # Ejecuta el agente en streaming:
            async for event in runner.run_async(
                user_id=USER_ID,
                session_id=session.id,
                new_message=message,
            ):
                # Nos interesa solo el evento de respuesta final del agente, hay otros eventos
                # intermedios que tienen usos pero no en este ejemplo.
                if event.is_final_response() and event.content and event.content.parts:
                    for part in event.content.parts:
                        if part.text:
                            response_text += part.text
            # Si hubo texto, lo mostramos en consola.
            if response_text:
                print(f"\nAgente: {response_text}")

        except KeyboardInterrupt:
            break
        except Exception as e:
            # Captura generica de errores para que el loop no explote
            print(f"Error en la ejecución: {e}")


if __name__ == "__main__":
    asyncio.run(main())