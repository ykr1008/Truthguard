from fastapi import FastAPI, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import re
import uuid

# Import your crew
from src.crew import truthguard_crew 

app = FastAPI(title="TruthGuard API", description="AI Multi-Agent Fact-Checking Service")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class FactCheckRequest(BaseModel):
    claim: str

# In-memory databases
results_db = {}
thoughts_db = {} # NEW: Stores the step-by-step thoughts

def run_crew_logic(job_id: str, claim: str, safe_name: str):
    # Initialize an empty list for this specific job's thoughts
    thoughts_db[job_id] = []

    # NEW: The interception function
    def custom_step_callback(step):
        # CrewAI 'steps' can be complex objects, so we convert it to a string to easily send to React
        thought_log = str(step)
        thoughts_db[job_id].append(thought_log)
        print(f"\n--- Intercepted Thought for {job_id[:8]} ---")

    # NEW: Attach the callback to every agent in your crew right before they start
    for agent in truthguard_crew.agents:
        agent.step_callback = custom_step_callback

    try:
        # Kick off the research
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

# NEW: The endpoint React will ping to get the latest thoughts
@app.get("/api/thoughts/{job_id}")
async def get_thoughts(job_id: str):
    # Returns the list of thoughts, or an empty list if none exist yet
    return {"thoughts": thoughts_db.get(job_id, [])}