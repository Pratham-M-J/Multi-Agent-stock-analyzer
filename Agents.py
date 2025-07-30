from crewai import Agent, LLM
from Tools import Scrape_and_Search_Tool
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI
load_dotenv()
from NewsTool import NewsTool
import os

open_api_key = os.getenv("OPEN_AI_KEY")
google_api_key = os.getenv("GOOGLE_API_KEY")
groq_api_key = os.getenv("GROQ_API_KEY")

scrape_and_search_tool = Scrape_and_Search_Tool()
news_tool = NewsTool()
Researcher = Agent(
    role = "Market Data Researcher",
    goal = "Retrieve the most relevant and up-to-date information about the specified {stock} from trusted online sources.",
    backstory = "You are an expert in financial research, tasked with investigating the company: {stock}. "
                "Your mission is to conduct thorough research by sourcing accurate and current data from reputable financial news sites, stock exchanges, and official company reports. "
                "Your meticulous research ensures that all subsequent analysis is based on reliable, comprehensive information, forming the essential foundation for the rest of the stock analysis process."
                "MAKE NO ASSUMPTIONS, Always search web and get recent data"
                "You can use the scrape_and_search tool only twice not more than that, even if the global news isn't found, you should end the process and give the data u have gathered.",
    allow_delegation = False,
    verbose = True,
    tools = [scrape_and_search_tool, news_tool],
    llm = LLM(
        api_key = open_api_key,
        model = "openai/gpt-4o",
    )
)

Analyst = Agent(
    role = "FINRA approved Financial Analyst",
    goal = "Analyze the gathered data to assess the stock’s current performance, trends, and potential opportunities or risks.",
    backstory = "You’re collaborating on a stock analysis project focused on the company: {stock}. "
                "Your task is to interpret and evaluate the raw information collected by the Market Data Researcher, "
                "using financial analysis techniques to provide meaningful insights. "
                "Your analysis is crucial for the Decision Advisor to craft a clear and actionable investment report on this stock.",
    allow_delegation = False,
    verbose = True,
    tools = [scrape_and_search_tool],
    


     llm = LLM(
        api_key = open_api_key,
        model = "openai/gpt-4o",
    )

)

DecisionAdvisor = Agent(
    role = "Report Generator & Decision Advisor",
    goal = "Summarize the analysis into a concise report with actionable insights and recommendations for the given {stock}.",
    backstory = "You’re collaborating on a stock analysis project focused on the company: {stock} "
                "Your task is to synthesize the findings from the Financial Analyst into a clear, well-structured report. "
                "Your report empowers investors to quickly understand the stock’s outlook and make informed decisions.",
    allow_delegation = False,
    verbose = True,
    llm = LLM(
        api_key = open_api_key,
        model = "openai/gpt-4o",
    )


)

