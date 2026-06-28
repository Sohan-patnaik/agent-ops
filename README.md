# AgentOps SDK – LLM Observability & Evaluation Platform MVP

A developer tool that helps AI engineers monitor and evaluate their AI agents locally. This repository contains the SDK client, a FastAPI backend server, in-memory processing engines, and a telemetry pipeline.

---

## Architecture Flow

```text
Developer Agent
      ↓ (Calls SDK method)
AgentOps SDK
      ↓ (HTTP POST payload & OpenTelemetry tracing)
FastAPI Backend (main.py)
      ↓ (Triggers Engines)
Monitoring Engine   ↔   Evaluation Engine (Ragas/Heuristic fallback)
      ↓
Dashboard API (/report, /monitor, /evaluate)
```

---

## Features

### 1. Automated LLM Monitoring
- **OpenTelemetry Instrumentation**: Automatically traces LLM invocations using the standard `llm.call` span.
- **Normalizer**: Automatically handles LangChain `AIMessage` objects and extracts token counts and models.
- **Cost Calculation**: Computes query costs in real time (e.g., GPT-4o input: \$5.0/1M, output: \$15.0/1M).

### 2. Automated RAG/LLM Evaluation
- **Faithfulness**: Measures context alignment (Ragas metric with heuristic fallback).
- **Relevance**: Measures query alignment (Ragas metric with heuristic fallback).
- **Graceful Fallback**: Automatically defaults to a local token-heuristic evaluator if `ragas` or `OPENAI_API_KEY` are not configured, preventing runtime failures.

### 3. Aggregated Reporting
- Global endpoints (`GET /report`) return average latencies, average query costs, total requests, and overall evaluation scores.

---

## File Structure

```text
agent-ops/
├── api/
│   ├── monitor.py         # POST /monitor (logs payload), GET /monitor (gets logs)
│   ├── evaluate.py        # POST /evaluate (runs ragas/heuristic), GET /evaluate
│   └── report.py          # GET /report (aggregated statistics)
│
├── core/
│   ├── config.py          # Configuration parser (loads from .env)
│   └── constants.py       # Shared constants
│
├── engines/
│   ├── monitoring_engine.py  # Stores logs in-memory and calculates LLM costs
│   ├── evaluation_engine.py  # Computes faithfulness and relevance (Ragas/Heuristic)
│   └── reporting_engine.py   # Computes average dashboard metrics
│
├── graph/
│   └── workflow.py        # Orchestration helper (Monitor -> Evaluate -> Report)
│
├── sdk/
│   ├── client.py          # Main SDK interface (AgentOps class)
│   ├── monitor.py         # Handles OpenTelemetry spans and POSTs metrics
│   ├── evaluate.py        # POSTs evaluation requests
│   ├── normalizer.py      # Standardizes LangChain AIMessages
│   └── pricing.py         # Pricing matrix and calculations
│
├── main.py                # Starts the FastAPI server (uvicorn)
├── requirements.txt       # Dependencies
└── .env                   # Configuration parameters
```

---

## Quick Start

### 1. Install Dependencies
```bash
python -m pip install -r requirements.txt
```

### 2. Configure Environment
Set up your local configuration in `.env`:
```env
AGENTOPS_API_URL=https://agent-ops.onrender.com
OPENAI_API_KEY=your-key-here # Optional: Required for active Ragas evaluation
```

### 3. Start the Backend
Start the backend server using Python:
```bash
python main.py
```

### 4. SDK Usage

#### Monitoring an LLM Call
```python
from sdk.client import AgentOps
from langchain_core.messages import AIMessage

agentops = AgentOps()

# Pass a LangChain response object directly
response = AIMessage(
    content="Paris is the capital of France.",
    response_metadata={
        "token_usage": {"prompt_tokens": 100, "completion_tokens": 50, "total_tokens": 150},
        "model_name": "gpt-4o"
    }
)

log_result = agentops.monitor(
    prompt="What is the capital of France?",
    response=response
)
print(log_result)
```

#### Evaluating a QA Response
```python
eval_result = agentops.evaluate(
    question="What is the capital of France?",
    answer="Paris.",
    context="Paris is the capital of France."
)
print(eval_result)
# Output: {'faithfulness': 1.0, 'relevance': 1.0}
```

#### Retrieving Reports
```python
import requests
report = requests.get("https://agent-ops.onrender.com/report").json()
print(report)
```
