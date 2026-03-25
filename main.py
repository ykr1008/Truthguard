import re
from crewai import Crew, Process

# Import our configurations from the other files
from src.agents import osint_researcher, senior_fact_checker, executive_editor
from src.tasks import research_task, fact_check_task, edit_task

# 1. Assemble the Crew
# We bundle the agents and tasks into a single Crew object.
truthguard_crew = Crew(
    agents=[osint_researcher, senior_fact_checker, executive_editor],
    tasks=[research_task, fact_check_task, edit_task],
    process=Process.sequential, # This strictly enforces our linear Research -> Check -> Edit flow
    verbose=True # Keeps the terminal output detailed so you can watch them "think"
)

# 2. The Main Execution Block
if __name__ == "__main__":
    print("🛡️ Welcome to TruthGuard: Automated Multi-Agent Fact-Checking 🛡️")
    print("-" * 60)
    
    # Capture the claim dynamically from the user
    claim_to_check = input("Enter a news headline or claim to verify: ")
    
    # 2. SANITIZE THE INPUT: 
    # This replaces all spaces and special characters with an underscore
    safe_name = re.sub(r'[^a-zA-Z0-9]', '_', claim_to_check)
    
    print(f"\n[!] Initiating TruthGuard analysis for: '{claim_to_check}'")
    print("[!] Handing off to the OSINT Researcher...\n")
    
    # 3. Inject BOTH the real claim and the sanitized filename into the tasks
    result = truthguard_crew.kickoff(inputs={
        'claim': claim_to_check,
        'safe_name': safe_name
    })
    
    print("\n" + "=" * 60)
    print("✅ ANALYSIS COMPLETE ✅")
    print("=" * 60 + "\n")
    print(result)