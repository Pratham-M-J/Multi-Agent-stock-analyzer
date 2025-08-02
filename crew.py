from crewai import Crew
from Tasks import research, analysis, reporting, sentiment_analysis
from Agents import Researcher, Analyst, DecisionAdvisor, Sentiment_analyser
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
import os

load_dotenv()

crew = Crew(
    agents = [Researcher,Sentiment_analyser, Analyst, DecisionAdvisor],
    tasks = [research,sentiment_analysis, analysis, reporting],
    verbose = True
)

print("Welcome to the Stock Analysis Crew! 🚀")
print("This crew will help you analyze stocks by gathering data, analyzing sentiment, and generating reports." \
"Services offered include:\n" \
    "1. Analyse your portfolio\n"
    "2. Analyse a stock\n" )
print("Please select a service to proceed:")

x = input("🙍‍♂️Enter your choice:")

if x == "1":
    print("Portfolio analysis is not yet implemented. Please check back later!")
elif x == "2":
    stock = input("Please enter the stock you want to analyze: ")
    result = crew.kickoff(inputs={"stock": stock})
else:
    print("Invalid choice. Please try again.")


google_api_key = os.getenv("GOOGLE_API_KEY")
llm = ChatGoogleGenerativeAI(
    google_api_key=google_api_key,
    model="gemini-2.0-flash",
    temperature=0.1,
)

print(result)

print('\n\n')
llm_response = llm.invoke(f"Here is the analysis report for {stock}:\n{result}, u should output 'buy' or 'sell' or 'hold' according to the report, no extra stuff")
print(f"LLM's recommendation: {llm_response.content.strip()}")