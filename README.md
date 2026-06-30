# AgentOps SDK 🚀

> Lightweight Python SDK for monitoring and evaluating LLM applications.

AgentOps SDK enables developers to instrument AI applications with a simple API for **LLM monitoring**, **response evaluation**, and **report generation**. It is designed as a developer-first SDK with an extensible architecture for future LLM observability features.

---

## ✨ Features

- 📊 **LLM Monitoring**
  - Monitor LLM requests with a single `monitor()` call
  - OpenTelemetry-based instrumentation
  - Automatic latency, token usage, and cost tracking

- 🤖 **LLM Evaluation**
  - Evaluate responses using **Faithfulness** and **Relevance**
  - Lightweight heuristic evaluator (MVP)
  - Designed for future RAGAS integration

- 📈 **Reporting**
  - Generate aggregated monitoring and evaluation summaries
  - Track average latency, cost, and evaluation scores

- ⚡ **Developer Friendly**
  - Published on **PyPI**
  - Simple Python API
  - FastAPI backend
  - Modular architecture

---

# Installation

```bash
pip install agentops
```

### 2. Configure Environment
Set up your local configuration in `.env`:
```env
AGENTOPS_API_URL=https://agent-ops.onrender.com
OPENAI_API_KEY=your-key-here # Optional: Required for active Ragas evaluation
```

# Quick Start

```python
from agentops import AgentOps
from langchain_openai import ChatOpenAI

client = AgentOps()

llm = ChatOpenAI(model="gpt-4o")

prompt = "What is Retrieval-Augmented Generation?"

response = llm.invoke(prompt)

client.monitor(
    prompt=prompt,
    response=response
)

client.evaluate(
    prompt=prompt,
    response=response,
    context=[
        "Retrieval-Augmented Generation (RAG) combines retrieval with LLM generation."
    ]
)

#### Retrieving Reports
```python
import requests
report = requests.get("https://agent-ops.onrender.com/report").json()
print(report)
```

---

# SDK APIs

## Monitor

Instrument an LLM call.

```python
client.monitor(
    prompt=prompt,
    response=response
)
```

Automatically captures:

- Response latency
- Token usage
- Model information
- Estimated cost
- OpenTelemetry traces

---

## Evaluate

Evaluate the generated response.

```python
client.evaluate(
    prompt=prompt,
    response=response,
    context=context
)
```

Returns

```python
{
    "faithfulness": 0.91,
    "relevance": 0.88
}
```

Current MVP uses a lightweight heuristic evaluator.

---

## Report

Generate an aggregated report.

```python
report = client.report()

print(report)
```

Example output

```python
{
    "total_requests": 15,
    "avg_latency": 0.82,
    "avg_cost": 0.00091,
    "avg_faithfulness": 0.90,
    "avg_relevance": 0.89
}
```

---

# Architecture

```
Developer Application
          │
          ▼
     AgentOps SDK
          │
          ▼
 OpenTelemetry Tracing
          │
          ▼
 FastAPI Backend
          │
 ┌────────┴────────┐
 ▼                 ▼
Monitoring     Evaluation
 Engine           Engine
          │
          ▼
     Reporting API
```

---

# Tech Stack

- Python
- FastAPI
- OpenTelemetry
- PyPI
- Render
- LangChain
- LangGraph

---

# Current MVP

Implemented

- ✅ monitor()
- ✅ evaluate()
- ✅ report()
- ✅ OpenTelemetry instrumentation
- ✅ Heuristic evaluation
- ✅ FastAPI backend
- ✅ PyPI package

---

# Roadmap

Upcoming features

- RAGAS evaluation
- DeepEval integration
- Multiple LLM provider support
- Streaming response monitoring
- Interactive dashboard
- PostgreSQL persistence
- Docker deployment
- Authentication
- Team workspaces

---

# Why AgentOps?

Modern LLM applications require more than generating responses—they require **observability**.

AgentOps SDK provides a lightweight foundation for:

- Monitoring AI applications
- Evaluating response quality
- Tracking latency and cost
- Building production-ready AI systems

while keeping the developer experience simple.

---

# Links

- 📦 PyPI Package
- 💻 GitHub Repository

---

# License

MIT License