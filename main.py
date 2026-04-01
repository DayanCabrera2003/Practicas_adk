import asyncio
import logging
from google import adk
from google.adk.sessions import InMemorySessionService
from google.genai import types

from router import router_agente

APP_NAME = "asistente_app"
USER_ID = "usuario_1"

logging.getLogger("google_genai.types").setLevel(logging.ERROR)


async def main():
    print("Iniciando sesion con sistema orquestado...")

    session_service = InMemorySessionService()

    session = await session_service.create_session(
        app_name=APP_NAME,
        user_id=USER_ID,
    )

    runner = adk.Runner(
        app_name=APP_NAME,
        agent=router_agente,
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

            async for event in runner.run_async(
                user_id=USER_ID,
                session_id=session.id,
                new_message=message,
            ):
                if event.is_final_response() and event.content and event.content.parts:
                    for part in event.content.parts:
                        if part.text:
                            print(f"\nAgente: {part.text.strip()}")

        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"Error en la ejecucion: {e}")


if __name__ == "__main__":
    asyncio.run(main())
