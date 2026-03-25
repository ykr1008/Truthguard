import os
from dotenv import load_dotenv
from crewai import Agent, LLM
from crewai.tools import BaseTool
from tavily import TavilyClient

# 1. Load Environment Variables
load_dotenv()

# 2. Initialize the LLM (The Native CrewAI Way)
gemini_llm = LLM(
    model="gemini/gemini-1.5-flash",
    api_key=os.getenv("GOOGLE_API_KEY"),
    temperature=0.2
)

# 3. Create a Custom Native CrewAI Tool
# This bypasses LangChain completely and talks directly to Tavily!
class NativeTavilySearchTool(BaseTool):
    name: str = "Tavily Web Search"
    description: str = "Search the web for current events, news, and factual information. Input should be a search query string."
    
    def _run(self, query: str) -> str:
        # Initialize the official Tavily client directly
        client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))
        # Perform the search and return the raw string data to the Agent
        results = client.search(query=query, max_results=5)
        return str(results)

search_tool = NativeTavilySearchTool()

# 4. Define the Agents

osint_researcher = Agent(
    role='Senior OSINT Researcher',
    goal='Gather comprehensive, accurate, and up-to-date information regarding the given claim or news headline.',
    backstory=(
        "You are an expert investigative researcher. Your expertise lies in "
        "navigating the web to find credible sources, extracting key facts, "
        "and identifying the origin of claims. You leave no stone unturned."
    ),
    verbose=True,
    allow_delegation=False, 
    tools=[search_tool], # Now using our custom, crash-proof tool
    llm=gemini_llm
)

senior_fact_checker = Agent(
    role='Senior Fact-Checker',
    goal='Analyze research data to determine the factual accuracy of a claim, identifying any contradictions or logical fallacies.',
    backstory=(
        "You are a meticulous fact-checker with years of experience at a major news organization. "
        "You excel at cross-referencing information, spotting biases, and objectively evaluating "
        "evidence to classify claims as True, False, or Misleading."
    ),
    verbose=True,
    allow_delegation=False,
    llm=gemini_llm
)

executive_editor = Agent(
    role='Executive Editor',
    goal='Format the fact-checker\'s analysis into a clean, professional, and easy-to-read Markdown report.',
    backstory=(
        "You are a seasoned editor who values clarity, precision, and readability. "
        "You take raw analytical data and transform it into structured, compelling "
        "reports that are accessible to the general public, ensuring all sources are properly cited."
    ),
    verbose=True,
    allow_delegation=False,
    llm=gemini_llm
)