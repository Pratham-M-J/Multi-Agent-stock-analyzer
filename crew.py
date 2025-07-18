from crewai import Crew
from Tasks import research, analysis, reporting
from Agents import Researcher, Analyst, DecisionAdvisor

crew = Crew(
    agents = [Researcher, Analyst, DecisionAdvisor],
    tasks = [research, analysis, reporting],
    verbose = True
)

result = crew.kickoff(inputs = {"stock" :"NVIDIA_CORP"})