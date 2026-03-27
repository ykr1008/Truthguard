# src/crew.py
from crewai import Crew, Process
from src.agents import osint_researcher, senior_fact_checker, executive_editor
from src.tasks import research_task, fact_check_task, edit_task

truthguard_crew = Crew(
    agents=[osint_researcher, senior_fact_checker, executive_editor],
    tasks=[research_task, fact_check_task, edit_task],
    process=Process.sequential,
    verbose=True
)