# 🛡️ TruthGuard: Multi-Agent Fact-Checking Engine

TruthGuard is an automated OSINT (Open Source Intelligence) and fact-checking pipeline. It uses specialized AI agents to investigate viral claims, cross-reference live web data, and generate objective research reports.

> **Status:** 🚧 Active Development (Migrating to FastAPI Backend)

## 🚀 Key Features
- **Multi-Agent Orchestration:** Powered by **CrewAI** to manage handoffs between Research, Fact-Checking, and Editorial agents.
- **High-Speed Inference:** Optimized with **Llama 3.3 70B** running on **Groq LPUs** for near-instant processing.
- **Live Web Intelligence:** Integrated with **Tavily Search API** for real-time data retrieval.
- **Modular Architecture:** Clean `src/` directory structure for enterprise-grade scalability.

## 📁 Project Structure
- `src/agents.py`: Expert agent definitions and personas.
- `src/tasks.py`: Sequential investigation and reporting pipelines.
- `src/crew.py`: The "Brain" that assembles the agents and tasks.
- `reports/`: Local archive of generated Markdown fact-check reports.
- `main.py`: Current CLI entry point for testing.

## 🛠️ Tech Stack
- **Language:** Python 3.11+
- **LLM:** Llama 3.3 70B (via Groq)
- **Framework:** CrewAI & LiteLLM
- **Search:** Tavily API
- **Backend:** FastAPI (Upcoming)

## 🏃 How to Run (Local CLI)
1. Clone the repo and install `requirements.txt`.
2. Set your `LLM_API_KEY` and `TAVILY_API_KEY` in a `.env` file.
3. Run `python main.py` and enter a claim to verify.