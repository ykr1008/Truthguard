from crewai import Crew, Process

# Import our configurations from the other files
from agents import osint_researcher, senior_fact_checker, executive_editor
from tasks import research_task, fact_check_task, edit_task

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
    
    print(f"\n[!] Initiating TruthGuard analysis for: '{claim_to_check}'")
    print("[!] Handing off to the OSINT Researcher...\n")
    
    # 3. Kick off the process
    # The 'inputs' dictionary automatically injects the claim into our tasks
    result = truthguard_crew.kickoff(inputs={'claim': claim_to_check})
    
    print("\n" + "=" * 60)
    print("✅ ANALYSIS COMPLETE ✅")
    print("=" * 60 + "\n")
    
    # Print the final result to the terminal 
    # (Remember, it also automatically saves to truthguard_report.md!)
    print(result)