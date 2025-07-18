from dotenv import load_dotenv
from crewai_tools import SerperDevTool, ScrapeWebsiteTool
from crewai.tools import BaseTool
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
load_dotenv()
import os

serper_api_key = os.environ['SERPER_API_KEY'] 
google_api_key = os.getenv("GOOGLE_API_KEY")

llm = ChatGoogleGenerativeAI(
    api_key=google_api_key,
    model="gemini-2.0-flash",
)

promptTemplate = PromptTemplate(
    input_variables=["data"],
    template="""
        You will be given a rough data from the web and you need to output a list of links separated by commas.
        Your response should have no other text, not even 'Here are your links:' etc.
        Here is the data: {data}
        Output the links in this format: [link1, link2, link3]
    """
)

extract_info_template = PromptTemplate(
    input_variables=["data", "stock"],
    template="""
        you will be given a huge chunk of data, you need to ignore all the giberish and
        extract only the information that is very important wrt {stock} and important global events and news
        Here is the data: {data}
    """
)

qa_chain = promptTemplate | llm
extraction_chain = extract_info_template | llm


web_scrape_tool = ScrapeWebsiteTool()

search_tool = SerperDevTool(
    search_url="https://google.serper.dev/scholar",
    n_results=10,
    api_key = serper_api_key
)


class Scrape_and_Search_Tool(BaseTool):
    name: str = "Scrape and Search Tool"
    description: str = (
        "This tool searches the web for information and then gets the web-links. "
        "The scraper tool scrapes the web and gives the relevant information which is structured by an LLM."
    )

    def _run(self, stock: str) -> str:
        # 1. Search
        data = search_tool.run(search_query=f"{stock} stocks")

        response = qa_chain.invoke({"data": data})
        links_text = response.content.strip().strip("[]")
        links = [link.strip().strip("'").strip('"') for link in links_text.split(",")]

        # 3. Scrape all links
        scraped_data = []
        for link in links:
            if link:  # basic safety
                try:
                    x = web_scrape_tool.run(website_url = link)
                    y = extraction_chain.invoke({"data": x, "stock": stock})
                    content = y.content
                    scraped_data.append(f"\n[Source: {link}]\n{content}")
                except Exception as e:
                    scraped_data.append(f"\n[Source: {link}]\nError scraping: {e}")
        print(links)
        return "\n".join(scraped_data)
    

scrape_and_search_tool = Scrape_and_Search_Tool()
