from fastapi import FastAPI, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import re
import uuid

# I am assuming this import works perfectly based on your src folder structure!
from src.crew import truthguard_crew 

app = FastAPI(title="TruthGuard API", description="AI Multi-Agent Fact-Checking Service")

# 🚨 The Bridge: Allows React to talk to FastAPI 🚨
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class FactCheckRequest(BaseModel):
    claim: str

# In-memory database for local testing
results_db = {}

def run_crew_logic(job_id: str, claim: str, safe_name: str):
    try:
        # Kicks off your multi-agent system
        result = truthguard_crew.kickoff(inputs={'claim': claim, 'safe_name': safe_name})
        results_db[job_id] = {"status": "completed", "result": str(result)}
    except Exception as e:
        results_db[job_id] = {"status": "failed", "error": str(e)}

@app.post("/api/fact-check")
async def start_fact_check(request: FactCheckRequest, background_tasks: BackgroundTasks):
    job_id = str(uuid.uuid4())
    safe_name = re.sub(r'[^a-zA-Z0-9]', '_', request.claim)
    
    background_tasks.add_task(run_crew_logic, job_id, request.claim, safe_name)
    return {"job_id": job_id, "status": "processing", "message": "Agents are researching..."}

@app.get("/api/status/{job_id}")
async def get_status(job_id: str):
    return results_db.get(job_id, {"status": "not_found"})