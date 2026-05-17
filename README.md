<p align="center">
  <img src="https://raw.githubusercontent.com/Arc-Cyber-Arsenal/Agentic-Blue-Team/master/agentic%20blue%20team.png" alt="403-Killchain Banner" width="600">
</p>


# 🛡️ Agentic Blue Team

### AI-Powered Autonomous Security Operations

**Agentic Blue Team** is a powerful, flexible, open-source, and agent-centric
automated security operations platform. It combines AI-driven intelligence
with a built-in SIRP to deliver autonomous alert triage, enrichment, and
response — all from a single, self-hosted deployment.

---

## 🧠 How It Works

The platform processes security alerts through a streamlined multi-stage pipeline:

1. **Alert Ingestion** – SIEM platforms (Splunk, Kibana/ELK) forward alerts via
   Webhook into the platform's built-in receiver.
2. **Stream Processing** – Alerts are pushed to Redis Streams, serving as
   persistent message queues. Each alert type has its own dedicated stream.
3. **AI Agent Analysis** – Modular AI agents consume alerts, perform deep
   analysis using local LLMs, enrich data with threat intelligence, and
   determine outcomes.
4. **SIRP Integration** – Outputs are formatted into standardized security
   records and sent to the built-in Security Incident Response Platform,
   where cases, alerts, and artifacts are created or updated.
5. **Automated Response** – Analysts trigger playbooks from the SIRP interface
   to perform further actions such as threat hunting, remediation, or
   notification.

---

## ⚡ Core Features

- **AI-Driven Intelligence** – Built-in AI Agent templates (Langgraph, Dify)
  supporting local LLMs for alert analysis and automated response.
- **Built-in SIRP** – Ready-to-use Security Incident Response Platform built
  on Nocoly, with rapid customization of UIs, data models, reports, and
  workflows.
- **Powerful Automation Workflow** – Efficient alert processing via
  Webhook + Redis Stream, natively supporting Splunk and Kibana (ELK).
- **Highly Extensible** – Rich library of Python modules and plugins for
  integration with security devices and APIs.
- **Local Deployment & Data Control** – Fully self-hosted. All data, models,
  and operations stay within your environment.
- **Streaming + Batch Processing** – Real-time alert analysis (modules) and
  event-driven automation (playbooks) for user-triggered tasks.

---

## 🚀 Installation

### Prerequisites
- Python 3.10+
- Redis
- Docker (optional, for containerized deployment)

### Quick Start
```bash
git clone https://github.com/Arc-Cyber-Arsenal/Agentic-Blue-Team
cd Agentic-Blue-Team
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
