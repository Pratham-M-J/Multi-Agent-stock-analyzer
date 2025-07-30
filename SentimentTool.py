import asyncio
import asyncpraw
from langchain_groq import ChatGroq
from langchain_core.runnables import RunnableLambda
from langchain_core.prompts import PromptTemplate
from crewai.tools import BaseTool
from dotenv import load_dotenv
import os

class MarketSentimentTool(BaseTool):
  name: str = "Market sentiment analyser Tool"
  description: str = (
    "This tool fetches Reddit posts from specified subreddits based on a stock keyword."
    "Parameters : stock (str): The stock keyword to search for."
    "Returns a List[dict]: A list of Market sentiment analysis for every post."

  )
  
  async def fetch_posts(self, stock, subreddit_list, limit=20):
      reddit = asyncpraw.Reddit(
          client_id=os.getenv("REDDIT_CLIENT_ID"),
          client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
          user_agent="Arthya",
      )
      all_posts = []
      for subreddit_name in subreddit_list:
          subreddit = await reddit.subreddit(subreddit_name)
          async for submission in subreddit.search(stock, sort="new", limit=limit):
              post_data = {
                  "subreddit": subreddit_name,
                  "title": submission.title,
                  "selftext": submission.selftext,
                  "url": submission.url,
                  "id": submission.id,
                  "comments": []
              }
              await submission.load()
              await submission.comments.replace_more(limit=0)
              for comment in submission.comments.list():
                  post_data["comments"].append(comment.body)
              all_posts.append(post_data)
      await reddit.close()
      return all_posts

  async def _run(self, stock:str):

    x = await self.fetch_posts(stock, ["IndianStockMarket", "IndiaInvestments"], limit=20)
    llm = ChatGroq(
      groq_api_key = os.environ['GROQ_API_KEY'],
      model = 'llama-3.1-8b-instant'
    )
    prompt_template = PromptTemplate(
      input_variables=["title", "top_comments"],
      template="""
        You are a financial analyst AI. You'll be given a Reddit post about a stock, including the title and top comments.
        Analyze the sentiment of the post and comments to determine the overall market sentiment toward the stock.

        ---
        **Title:** {title}

        **Top Comments:**
        {top_comments}

        ---
        Return your response in this format:
        - Detected Stock(s): <stock name(s)>
        - Sentiment: <Positive / Negative / Neutral>
        - Justification: <Why you think this is the sentiment>
        """
      )
    analysis_chain = prompt_template | llm
    responses = []
    if len(x) > 15:
      x = x[:15]
    else:
      x
    for post in x:
        inputs = {
            "title": post["title"],
            "top_comments": "\n".join(post["comments"][:15])
        }
        responses.append(analysis_chain.invoke(inputs).content)

    return responses