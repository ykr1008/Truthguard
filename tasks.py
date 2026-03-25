from crewai import Task
from agents import osint_researcher, senior_fact_checker, executive_editor

# Task 1: The Research Assignment
research_task = Task(
    description=(
        "Conduct a comprehensive web search to gather information regarding "
        "the following claim or news headline: '{claim}'.\n"
        "Find the original source of the claim if possible, and gather at least "
        "3 credible articles or data points that either support or refute it."
    ),
    expected_output=(
        "A detailed summary of findings, including the original context of the claim, "
        "a list of sources found, and a breakdown of what each source states regarding "
        "the headline. Include the raw URLs."
    ),
    agent=osint_researcher
)

# Task 2: The Fact-Checking Assignment
fact_check_task = Task(
    description=(
        "Review the research data provided by the OSINT Researcher regarding "
        "the claim: '{claim}'.\n"
        "Cross-reference the information, look for contradictions, assess the "
        "credibility of the sources, and determine if the claim is True, False, "
        "or Misleading. You must justify your conclusion using the provided evidence."
    ),
    expected_output=(
        "A definitive classification (True, False, or Misleading) accompanied by a "
        "thorough analytical justification. Highlight any contradictory evidence "
        "and explain why certain sources were trusted over others."
    ),
    agent=senior_fact_checker
)

# Task 3: The Editorial Assignment
edit_task = Task(
    description=(
        "Take the analytical conclusion from the Senior Fact-Checker regarding "
        "the claim: '{claim}' and format it into a public-facing report.\n"
        "Ensure the tone is objective, professional, and easy for a general "
        "audience to understand."
    ),
    expected_output=(
        "A final, highly readable Markdown document structured with the following headers:\n"
        "# TruthGuard Fact-Check Report\n"
        "## The Claim\n"
        "## Verdict: [True/False/Misleading]\n"
        "## Analysis\n"
        "## Sources Cited\n"
    ),
    agent=executive_editor,
    output_file="truthguard_report.md" # This will automatically save the output to a file!
)