from fastapi import FastAPI, Request
from vertexai.generative_models import GenerativeModel
from agents.shared.notebooklm_client import NotebookLMClient
from agents.shared.mcp_client import MCPClient

app = FastAPI()
gemini = GenerativeModel("gemini-2.0-flash")
mcp = MCPClient()
notebook = NotebookLMClient(project_id="YOUR_PROJECT")

@app.post("/a2a")
async def a2a(req: Request):
    body = await req.json()
    if body["type"] == "supply_telemetry":
        return handle_supplies(body["payload"])
    return {"status": "skipped"}

def handle_supplies(payload):
    guidelines = notebook.ask("Provide evidence-based guidance on reducing expiration waste for consumables.")

    prompt = f"""
    Supplies incoming:
    {payload}

    Sustainability guidelines:
    {guidelines}

    Suggest:
    - predicted shortages
    - alternative low-footprint materials
    - reorder thresholds
    """
    result = gemini.generate_content(prompt).text
    mcp.broadcast_event("SUPPLY_OPTIMIZATION", result)
    return {"recommendations": result}
