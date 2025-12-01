```markdown
# 🧬 BioLoop Agents
### *Autonomous Circular-Care System for Sustainable Hospitals*  
Built with **Gemini**, **Google Agent Developer Kit (ADK)**, **Vertex AI Agent Engine**, **A2A Protocol**, **MCP**, and **NotebookLM**.

---

# 🌍 Overview

**BioLoop Agents** is a modular multi-agent platform designed to help hospitals simultaneously:

1. **Improve clinical efficiency**  
2. **Reduce environmental footprint**  
3. **Automate operational sustainability reporting**

It uses an ecosystem of AI-driven agents—built on **Gemini** and deployed on **Google Cloud**—that continuously monitor a hospital’s workflows, supplies, energy use, and climate risks.

Each agent collaborates via an **Agent-to-Agent (A2A)** protocol and a **Multi-Agent Control Plane (MCP)** that coordinates global decisions.

---

# 🧠 Agent Ecosystem

### **1. CareFlow Agent**
Optimizes patient flow, predicts bottlenecks, and reduces unnecessary material use.  
Receives: `patient-flow` telemetry (Pub/Sub)  
Sends: staffing + routing suggestions, load signals to EnerSense.

---

### **2. MedCycler Agent**
Monitors supply usage, anticipates shortages, recommends lower-footprint alternatives, and reduces expiration waste.  
Uses NotebookLM to reference sustainability and clinical guidelines.

---

### **3. EnerSense Agent**
Optimizes HVAC, lighting, sterilization cycles, and energy schedules without risking patient safety.

---

### **4. GreenRisk Agent**
Analyzes weather + climate forecasts, predicts clinically relevant surges, and triggers staff/supply preparation.

---

# 🧩 Core Technologies

| Component | Purpose |
|----------|---------|
| **Gemini 2.0 (Pro / Flash)** | AI reasoning + sustainability-aware decision-making |
| **ADK (Agent Developer Kit)** | Agent lifecycle, messaging, observability |
| **Vertex AI Agent Engine** | Orchestration of agent tools + policies |
| **A2A Protocol** | Inter-agent RPC |
| **MCP (Multi-Agent Control Plane)** | Event broadcasting & global coordination |
| **NotebookLM** | Evidence-backed recommendations for clinical + sustainability topics |
| **Pub/Sub** | Hospital telemetry ingestion |
| **Cloud Run** | Serverless agent runtime |
| **Firestore & Cloud Storage** | State tracking + supply logs |

---

# 🏗 Architecture Diagram

```

NotebookLM — evidence + guidelines
▲
│
┌───────┴────────────────┐
│      MCP Control Plane │
└───────┬─────┬─────────┘
│     │
▼     ▼
CareFlow ←→ MedCycler ←→ EnerSense ←→ GreenRisk
▲         ▲            ▲            ▲
│         │            │            │
Patient Flow   │       HVAC + IoT        Climate API
Supply Logs    │
│
Hospital EHR / Telemetry

```

---

# 📦 Repository Structure

```

bioloop/
├── agents/
│   ├── careflow/
│   ├── medcycler/
│   ├── enersense/
│   ├── greenrisk/
│   └── shared/
├── infra/
│   ├── cloudrun_deploy.sh
│   ├── pubsub_topics.sh
│   └── terraform/ (optional)
└── README.md

````

---

# 🚀 Quick Start

## 1. Clone Repository
```bash
git clone https://github.com/YOUR_ORG/bioloop-agents.git
cd bioloop-agents
````

---

# 🛠 Prerequisites

* **Google Cloud Project** (billing enabled)
* **gcloud** CLI installed
* **Python 3.10+**
* Vertex AI API enabled:

```bash
gcloud services enable aiplatform.googleapis.com \
                       run.googleapis.com \
                       pubsub.googleapis.com
```

---

# 📡 Set Up Pub/Sub Topics

From `infra/`:

```bash
bash pubsub_topics.sh
```

Creates:

* `patient-flow`
* `supply-events`
* `energy-events`
* `climate-events`

---

# 🧪 Local Development

Run any agent locally:

```bash
cd agents/careflow
pip install -r requirements.txt
uvicorn agent:app --reload --port 8081
```

Test A2A messaging:

```bash
curl -X POST http://localhost:8081/a2a \
   -H "Content-Type: application/json" \
   -d '{
        "type":"patient_flow_update",
        "payload":{"current_load":72}
       }'
```

---

# ☁️ Deployment to Cloud Run

Deploy all agents:

```bash
cd infra
bash cloudrun_deploy.sh
```

This will:

1. Build container images
2. Deploy agents to Cloud Run
3. Output agent URLs (required for A2A)

---

# 🤖 Register with Vertex AI Agent Engine

Update `vertex_agent.yaml` with Cloud Run URLs, then:

```bash
gcloud alpha agent-engines deploy bioloop-system --config vertex_agent.yaml
```

---

# 📘 NotebookLM Integration

Each agent can call NotebookLM for knowledge-backed decision-making.

```python
notebook = NotebookLMClient(project_id="YOUR_PROJECT")
```

NotebookLM stores:

* Clinical guidelines
* Sustainability research
* Material carbon footprint tables
* Waste reduction literature

---

# 🔗 Agent-to-Agent Messaging (A2A)

Agents send structured messages:

```json
{
  "type": "care_load_update",
  "payload": { "load": 72 }
}
```

All agents expose:

```
POST /a2a
```

Protocol implementation:

```
agents/shared/a2a_protocol.py
```

---

# 🛰 Multi-Agent Control Plane (MCP)

Agents broadcast higher-level events:

* `CARE_DECISION`
* `SUPPLY_OPTIMIZATION`
* `ENERGY_DECISION`
* `RISK_ALERT`

Hospitals may subscribe dashboards, reporting systems, or automation to MCP channels.

---

# 📊 Dashboards (Optional)

Integrate with:

* **Grafana** (telemetry + energy)
* **Looker** (sustainability, waste, carbon)
* **Chronicle** (audit logs + compliance)

---

# 🔒 Security & Compliance

* Cloud Run sandbox isolation
* HTTPS-only communication
* Per-agent IAM service accounts
* Firestore audit logs
* PHI-safe by design (no logs containing patient identifiers)

HIPAA/GDPR support available through:

* VPC-SC
* Cloud DLP
* CMEK encryption

---

# 🧩 Extending the Platform

Create new agents:

```
agents/newagent/
    agent.py
    config.yaml
```

Then:

1. Add Pub/Sub topics as needed
2. Add A2A endpoints
3. Register tools in Vertex AI Agent Engine
4. Connect to MCP events

Examples:

* **SterileCycle Agent** — improve OR sterilization efficiency
* **WaterSense Agent** — reduce hospital water consumption
* **GHG Reporter Agent** — auto-generate ESG compliance reports

---

# 🧪 Testing

Run unit tests:

```bash
pytest agents/
```

Integration testing:

```bash
bash tests/test_a2a.sh
```

