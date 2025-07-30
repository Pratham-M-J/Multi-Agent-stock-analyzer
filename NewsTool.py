from crewai.tools import BaseTool
import json
import urllib.request
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GNEWS_KEY")

class NewsTool(BaseTool):
  name: str = "News tool"
  description: str = (
      "This tool upon giving a single word input for eg: AAPL or Apple"
      "Gets the top headlines, description, date and url of the latest news"
  )

  def _run(self, stocks: str) -> str:
    apikey = api_key
    q =  stocks
    url = f"https://gnews.io/api/v4/search?q={q}&lang=en&country=any&max=10&apikey={apikey}"
    with urllib.request.urlopen(url) as response:
        data = json.loads(response.read().decode("utf-8"))
        articles = data["articles"]
        response = ""
        for article in articles:
          response += f"Title:{article['title']}\n Description: {article['description']} \n Date: {article['publishedAt']} \n URL: {article['url']}\n\n"

        return response if response else "No news found for the given stock."
    


