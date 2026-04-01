import asyncio
from google import adk
from google.adk.sessions import InMemorySessionService
from google.genai import types
from agent import mi_primer_agente

APP_NAME = "asistente_app"
USER_ID = "usuario_1"

async def main():
    print("Iniciando sesión con el agente de ADK...")

    session_service = InMemorySessionService()
    session = await session_service.create_session(app_name=APP_NAME, user_id=USER_ID)

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

            message = types.Content(
                role="user",
                parts=[types.Part(text=user_input)],
            )

            response_text = ""
            async for event in runner.run_async(
                user_id=USER_ID,
                session_id=session.id,
                new_message=message,
            ):
                if event.content and event.content.parts:
                    for part in event.content.parts:
                        if part.text:
                            response_text += part.text

            if response_text:
                print(f"\nAgente: {response_text}")

        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"Error en la ejecución: {e}")


if __name__ == "__main__":
    asyncio.run(main())