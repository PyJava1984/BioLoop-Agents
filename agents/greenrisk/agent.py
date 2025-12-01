from fastapi import FastAPI, Request
from vertexai.generative_models import GenerativeModel
from agents.shared.mcp_client import MCPClient

app = FastAPI()
gemini = GenerativeModel("gemini-2.0-pro")
mcp = MCPClient()

@app.post("/a2a")
async def a2a(req: Request):
    body = await req.json()
    if body["type"] == "climate_forecast":
        return assess_risk(body["payload"])
    return {"status": "ignored"}

def assess_risk(data):
    prompt = f"""
    Climate forecast:
    {data}

    Provide:
    - predicted patient surges
    - vulnerable departments
    - staffing + supply pre-positioning strategy
    """
    result = gemini.generate_content(prompt).text
    mcp.broadcast_event("RISK_ALERT", result)
    return {"risk_analysis": result}
