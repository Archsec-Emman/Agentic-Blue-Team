<p align="center">
  <img src="https://raw.githubusercontent.com/Arc-Cyber-Arsenal/Agentic-Blue-Team/master/agentic%20blue%20team.png" alt="403-Killchain Banner" width="400">
</p>



# Agentic Blue Team

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Platform](https://img.shields.io/badge/platform-linux%20%7C%20windows%20%7C%20macos-lightgrey)](https://github.com/Archsec-Emman/Agentic-Blue-Team)
[![Docker](https://img.shields.io/badge/docker-support-blue)](https://www.docker.com/)

**An open‑source, agent‑centric platform that fuses AI intelligence with a built‑in Security Incident Response Platform to automate alert triage, enrichment, and response — all within your own infrastructure.**

---

## 📖 Overview

Agentic Blue Team is built to transform how security operations centers (SOCs) handle alerts. Instead of a static dashboard, the platform orchestrates modular AI agents (powered by local LLMs) to continuously ingest alerts, enrich them with threat intelligence, and produce structured security records. A fully integrated SIRP—built on the Nocoly worksheet platform—manages cases, alerts, artifacts, and playbooks, allowing analysts to trigger automated remediation or threat‑hunting workflows with a single click.

The entire system is designed for local deployment: your data, models, and operations never leave your environment, ensuring complete confidentiality and compliance.

---

## ✨ Core Features

| Feature | Description |
|---------|-------------|
| **AI‑Driven Intelligence** | Pre‑built agent templates (LangGraph, Dify) that use local LLMs to analyze alerts, enrich data, and determine outcomes. |
| **Built‑in SIRP** | Full incident response platform on Nocoly with rapid customization of UIs, data models, reports, and workflows. |
| **Powerful Automation Workflow** | Webhook‑based ingestion from Splunk / Kibana → Redis Streams → agent analysis → SIRP → playbooks. |
| **Highly Extensible** | Rich library of Python modules and plugins for integrating with any security device or API. |
| **Local Deployment & Data Control** | Fully self‑hosted; everything stays inside your environment. |
| **Streaming + Batch Processing** | Real‑time alert analysis plus event‑driven automation for user‑triggered tasks. |

---

## 🧠 Architecture

Agentic Blue Team follows a **five‑stage pipeline** that maps directly to the modern SOC workflow:

```
SIEM (Splunk/ELK) → Webhook → Redis Stream → AI Agents → SIRP → Playbooks
```

### 1. Alert Ingestion
Splunk, Kibana/ELK, or any SIEM forwards security alerts via a **webhook** to the platform’s built‑in receiver.

### 2. Stream Processing
Alerts are pushed into dedicated **Redis Streams** (one per alert type), which act as persistent, replayable message queues.

### 3. AI Agent Analysis
Modular AI agents consume alerts from the streams and perform deep analysis using **local LLMs**, threat intelligence enrichment, and rule‑based decision making.

### 4. SIRP Integration
Agent outputs are formatted into standardized security records and sent to the built‑in **Security Incident Response Platform**, where they create or update cases, alerts, and artifacts.

### 5. Automated Response
Analysts trigger **playbooks** directly from the SIRP interface to execute further actions — such as threat hunting, remediation, or notifications — closing the loop.

---

## 🗃️ Core Data Model

The SIRP is built on a **clean, ontology‑driven data model** that separates detection, investigation, and response concerns.

| Entity | Purpose |
|--------|---------|
| **Case** | The primary investigation object; aggregates alerts, artifacts, enrichments, and tickets. |
| **Alert** | Middle‑layer object that retains detection‑source information (OCSF style) and links to artifacts. |
| **Artifact** | The atomic unit: IP, domain, hash, username, etc. – the natural input for any query or enrichment. |
| **Enrichment** | Structured, attachable information (threat intel, CMDB data, logs) that can be independently maintained. |
| **Ticket** | Synchronization with external ticketing systems, linked to a Case. |
| **Playbook** | Automated logic (often LangGraph orchestration) that runs against Cases, Alerts, or Artifacts. |
| **Knowledge** | Shared, high‑currency knowledge base that serves both human analysts and AI agents. |

---

## 🚀 Installation

### Prerequisites
- Python 3.10+
- Redis
- Docker (optional, for containerized deployment)

### Quick Start

```bash
# Clone the repository
git clone https://github.com/Archsec-Emman/Agentic-Blue-Team
cd Agentic-Blue-Team

# Install dependencies
pip install -r requirements.txt

# Run database migrations
python manage.py migrate

# Start the development server
python manage.py runserver
```

The platform will be available at `http://localhost:8000`.

### Docker Deployment (Recommended for Production)

```bash
# Build and start all services
docker-compose up -d

# Services:
# - Web UI (Nocoly SIRP)
# - Redis Streams
# - Uvicorn (ASGI server)
# - Ollama (optional, for local LLMs)
```

---

## ⚙️ Configuration

### Connecting a SIEM (Splunk / ELK)

1. Configure your SIEM to send alerts via webhook to `http://<agentic-blue-team>:8000/api/webhook/siem`
2. Set the appropriate authentication token in `settings.py`.
3. Alerts will automatically be routed to the correct Redis stream based on their type.

### Using Local LLMs

Agentic Blue Team supports any local LLM through the **Ollama** plugin. To integrate:

1. Install Ollama and pull a model (e.g., `ollama pull llama3.2`).
2. In the platform, go to **Plugins → Ollama** and enter the model name.
3. Agents will automatically use the configured LLM for analysis.

### Customizing the SIRP

The built‑in SIRP (Nocoly) allows full customization of:
- **UIs** – Drag‑and‑drop dashboards and forms
- **Data models** – Add custom fields to Cases, Alerts, Artifacts, etc.
- **Reports** – Generate compliance or summary reports
- **Workflows** – Define approval chains or automated transitions

Refer to the `ARCHITECTURE.md` file for a detailed explanation of the data model and extension points.

---

## 🔌 Plugin Ecosystem

Agentic Blue Team includes a growing library of **plug‑and‑play modules** under the `PLUGINS/` directory.

| Plugin | Purpose |
|--------|---------|
| **AlienVaultOTX** | Pull threat intelligence from OTX |
| **ClaudeCode** | Use Anthropic’s Claude for agent reasoning |
| **ELK** | Native integration with Elastic Stack |
| **Embeddings** | Vector embeddings for alert similarity search |
| **Forwarder** | Relay alerts to external systems |
| **Huggingface** | Access Hugging Face models |
| **LLM** | Generic LLM adapter (OpenAI, Gemini, etc.) |
| **MCP** | Model Context Protocol support |
| **Qdrant** | Vector database for artifact correlation |

To activate a plugin, simply add its configuration in `settings.py`; the platform auto‑discovers and loads it.

---

## 📂 Project Structure

```
Agentic-Blue-Team/
├── ABT/                   # Django project configuration
│   ├── settings.py        # Main settings (plugins, LLMs, webhooks)
│   ├── urls.py            # URL routing
│   └── asgi.py / wsgi.py
├── AGENTS/                # Modular AI agents
│   ├── agent_cmdb.py      # CMDB enrichment agent
│   ├── agent_report.py    # Report generation agent
│   ├── agent_siem.py      # SIEM alert processing
│   └── agent_threat_intelligence.py
├── Core/                  # Core data models (Case, Alert, Artifact, etc.)
│   ├── models.py          # SIRP data model
│   ├── serializers.py
│   └── views.py           # REST API endpoints
├── PLAYBOOKS/             # Automated response playbooks
│   ├── ALERT/             # Alert‑specific playbooks
│   ├── ARTIFACT/          # Artifact‑specific playbooks
│   └── CASE/              # Case‑level remediation workflows
├── PLUGINS/               # Extensible plugin library (see list above)
├── Lib/                   # Core libraries (API, base modules, etc.)
├── DATA/                  # Agent‑specific data handlers
├── Docker/                # Docker Compose services (DB, Redis, Ollama, etc.)
├── ARCHITECTURE.md        # Detailed architecture reference
├── manage.py              # Django management script
├── pyproject.toml         # Python project metadata
└── README.md              # This file
```

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository.
2. Create a feature branch (`git checkout -b feature/amazing-feature`).
3. Commit your changes (`git commit -m 'Add some amazing feature'`).
4. Push to the branch (`git push origin feature/amazing-feature`).
5. Open a Pull Request.

Areas where help is especially valuable:
- **New plugins** – Add support for more threat intel sources or SIEMs.
- **Agent improvements** – Enhance the existing agents or create new ones.
- **Playbook examples** – Provide production‑ready playbooks for common threats.
- **Documentation** – Expand examples and how‑to guides.

---

## 📄 License

This project is licensed under the **MIT License** – see the [LICENSE](LICENSE) file for details.

---

## 📬 Contact & Support

- **GitHub Issues**: [https://github.com/Archsec-Emman/Agentic-Blue-Team/issues](https://github.com/Archsec-Emman/Agentic-Blue-Team/issues)
- **Author**: [Archsec-Emman](https://github.com/Archsec-Emman)

---

*If this platform accelerates your security operations, please consider giving the repository a star.* ⭐
```
