import asyncio
import logging
import os
from google import adk
from google.adk.sessions import InMemorySessionService
from google.genai import types
from agent import mi_primer_agente

APP_NAME = "asistente_app"
USER_ID = "usuario_1"

# Evita el warning de partes no textuales cuando el modelo emite function_call.
logging.getLogger("google_genai.types").setLevel(logging.ERROR)

DEBUG_TOOLS = os.getenv("ADK_DEBUG_TOOLS", "1") == "1"

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
            tool_result = None
            tool_calls = []

            # Ejecuta el agente en streaming:
            async for event in runner.run_async(
                user_id=USER_ID,
                session_id=session.id,
                new_message=message,
            ):
                if event.content and event.content.parts:
                    for part in event.content.parts:
                        if part.function_call:
                            call = part.function_call
                            tool_calls.append(call.name or "tool_desconocida")
                            if DEBUG_TOOLS:
                                print(
                                    f"\n[TOOL CALL] {call.name} args={call.args}"
                                )

                        if part.function_response and part.function_response.response:
                            tool_result = part.function_response.response.get("result")
                            if DEBUG_TOOLS:
                                print(
                                    "[TOOL RESPONSE] "
                                    f"{part.function_response.name} -> "
                                    f"{part.function_response.response}"
                                )

                # Nos interesa solo el evento de respuesta final del agente, hay otros eventos
                # intermedios que tienen usos pero no en este ejemplo.
                if event.is_final_response() and event.content and event.content.parts:
                    for part in event.content.parts:
                        if part.text:
                            response_text += part.text
            # Si hubo texto, lo mostramos en consola.
            if response_text:
                print(f"\nAgente: {response_text}")
            elif tool_result is not None:
                print(f"\nAgente: El resultado es {tool_result}")
            else:
                print("\nAgente: No se recibio una respuesta de texto.")

            if DEBUG_TOOLS and tool_calls:
                tools_usadas = ", ".join(sorted(set(tool_calls)))
                print(f"[TRACE] Herramientas usadas en este turno: {tools_usadas}")

        except KeyboardInterrupt:
            break
        except Exception as e:
            # Captura generica de errores para que el loop no explote
            print(f"Error en la ejecución: {e}")


if __name__ == "__main__":
    asyncio.run(main())