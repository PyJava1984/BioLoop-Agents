import json
from fastapi import FastAPI, Request
from vertexai.generative_models import GenerativeModel
from agents.shared.a2a_protocol import A2AClient
from agents.shared.mcp_client import MCPClient
from agents.shared.notebooklm_client import NotebookLMClient

app = FastAPI()

gemini = GenerativeModel("gemini-2.0-pro")
mcp = MCPClient()
notebook = NotebookLMClient(project_id="YOUR_PROJECT")

@app.post("/a2a")
async def handle_a2a(req: Request):
    body = await req.json()
    if body["type"] == "patient_flow_update":
        return optimize_patient_flow(body["payload"])
    return {"status": "ignored"}

def optimize_patient_flow(data):
    prompt = f"""
    You are CareFlow Agent. Analyze patient flow:

    {json.dumps(data, indent=2)}

    Provide:
    - Bottlenecks
    - Resource reallocation
    - Predicted delays
    - Material reduction recommendations
    """
    result = gemini.generate_content(prompt)
    decision = result.text

    # Inform EnerSense Agent
    ener = A2AClient(agent_url="https://enersense-xyz.run.app")
    ener.send("care_load_update", {"load": data["current_load"]})

    mcp.broadcast_event("CARE_DECISION", decision)

    return {"decision": decision}
