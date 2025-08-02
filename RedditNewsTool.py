from crewai.tools import BaseTool
import asyncio
import asyncpraw
import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate

load_dotenv()


class RedditNewsTool(BaseTool):
    name: str = "Market News Tool Reddit"
    description: str = (
        "Fetches Reddit posts from finance-related subreddits, analyzes for actionable market news, "
        "and summarizes relevant economic/stock market updates."
    )

    async def fetch_hot_posts_per_subreddit(self, reddit, subreddit_name, limit=30, upvote_min=200, top_n_comments=5):
        subreddit = await reddit.subreddit(subreddit_name)
        posts_content = []

        async for submission in subreddit.hot(limit=limit):
            is_meme = (submission.link_flair_text and "meme" in submission.link_flair_text.lower())
            if submission.score < upvote_min or is_meme:
                continue
            await submission.load()
            await submission.comments.replace_more(limit=0)
            top_comments = sorted(
                [c for c in submission.comments if isinstance(c, asyncpraw.models.Comment)],
                key=lambda x: x.score,
                reverse=True
            )[:top_n_comments]

            posts_content.append({
                "subreddit": subreddit.display_name,
                "title": submission.title,
                "selftext": submission.selftext,
                "url": submission.url,
                "id": submission.id,
                "score": submission.score,
                "created_utc": submission.created_utc,
                "flair": submission.link_flair_text,
                "top_comments": [{"body": c.body, "score": c.score} for c in top_comments]
            })

        return posts_content

    async def fetch_top_hot_posts(self, subreddits=None, per_sub_limit=30, upvote_min=200, top_n_comments=5, overall_top_n=10):
        if subreddits is None:
            subreddits = ["indianstockmarket", "Wallstreetbets", "IndianStocks", "business"]

        reddit = asyncpraw.Reddit(
            client_id=os.getenv("REDDIT_CLIENT_ID"),
            client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
            user_agent="Arthya/1.0",
        )

        tasks = [
            self.fetch_hot_posts_per_subreddit(
                reddit, subreddit,
                limit=per_sub_limit,
                upvote_min=upvote_min,
                top_n_comments=top_n_comments
            )
            for subreddit in subreddits
        ]

        all_results = await asyncio.gather(*tasks)
        await reddit.close()

        all_posts = [post for group in all_results for post in group]
        return sorted(all_posts, key=lambda x: x['score'], reverse=True)[:overall_top_n]

    async def _run(self) -> list:
        posts = await self.fetch_top_hot_posts()
        if not posts:
            return ["No relevant posts found."]

        llm = ChatGoogleGenerativeAI(
            google_api_key=os.getenv('GOOGLE_API_KEY'),
            model='gemini-2.0-flash',
            temperature=0,
        )

        prompt_template = PromptTemplate(
            input_variables=["title", "top_comments"],
            template="""
You will be provided with a Reddit post, including its Title and a list of the Top Comments.

Your task is to:
- Analyze the text for any information about important global news, or news specifically related to the stock market, economic trends, trade, corporate actions, or major business developments.
- If such news is present, extract and summarize the key facts in clear, concise points.
- Clean the data to remove irrelevant content, slang, personal remarks, memes, or unrelated opinions. Focus only on factual and actionable information.

Your output should be a formatted summary highlighting the significance of the detected news or event, especially as it relates to markets or global business.

If there is no relevant news, respond with: "None"

Title: {title}
Top Comments: {top_comments}
"""
        )

        analysis_chain = prompt_template | llm
        responses = []

        for post in posts:
            top_comments_text = "\n".join([comment['body'] for comment in post['top_comments']])
            inputs = {
                "title": post["title"],
                "top_comments": top_comments_text
            }
            response = await analysis_chain.ainvoke(inputs)
            content = response.content.strip()
            if content != "None":
                responses.append(content)

        return responses or ["No significant global, stock market, or business news identified."]

