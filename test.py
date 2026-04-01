from google.adk import Agent

# Esto nos imprimirá la firma exacta que espera el constructor de Agent
print(Agent.__pydantic_fields__.keys())