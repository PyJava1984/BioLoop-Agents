from fastapi import FastAPI, Request
from vertexai.generative_models import GenerativeModel
from agents.shared.mcp_client import MCPClient

app = FastAPI()
gemini = GenerativeModel("gemini-2.0-pro")
mcp = MCPClient()

@app.post("/a2a")
async def a2a(req: Request):
    body = await req.json()
    if body["type"] == "care_load_update":
        return optimize_energy(load=body["payload"]["load"])
    return {"status": "noop"}

def optimize_energy(load):
    prompt = f"""
    You are EnerSense Agent.

    Predict HVAC + lighting adjustments based on:
    - Clinical load: {load}
    - Safety constraints: no risk to patients

    Provide:
    - energy reduction steps
    - off-peak shifts
    - sterilization cycle timing improvements
    """
    result = gemini.generate_content(prompt).text
    mcp.broadcast_event("ENERGY_DECISION", result)
    return {"energy_plan": result}
