from crewai import Task
from Tools import web_scrape_tool, search_tool
from Agents import Researcher, Analyst, DecisionAdvisor

research = Task(
    description = (
        "1. Prioritize gathering the latest news and major global events that could impact the {stock}, with special attention to US government actions and geopolitical conflicts.\n"
        "2. Identify and specify the market segment or industry to which the {stock} belongs.\n"
        "3. Collect recent financial data, earnings reports, and key performance indicators from reputable sources.\n"
        "4. Analyze market sentiment by reviewing news, social media, and expert commentary relevant to the {stock}."
        "5. Use the Scrape and Search Tool to gather this information, ensuring that you only use it twice. If you cannot find global news, end the process and provide the data you have gathered."
    ),
    expected_output = (
        "A well-organized summary containing:\n"
        "- The most recent and relevant news headlines and global events affecting {stock}.\n"
        "- The identified market segment or industry classification for {stock}.\n"
        "- A table or list of up-to-date financial data, earnings reports, and key performance indicators.\n"
        "- A brief analysis of current market sentiment, including highlights from news, social media, and expert opinions."
    ),
    name = "Research",
    agent = Researcher,
    
)

analysis = Task(
    description = (
        "1. Review the research summary, including news, financial data, and market sentiment for {stock}.\n"
        "2. Perform fundamental analysis using financial indicators (e.g., P/E ratio, revenue growth, profit margins).\n"
        "3. Conduct technical analysis by identifying recent stock price trends, support/resistance levels, and trading volume patterns.\n"
        "4. Assess risks and opportunities based on both qualitative and quantitative findings."
    ),
    expected_output = (
        "A comprehensive analysis report that includes:\n"
        "- Key insights from fundamental and technical analysis of NVIDIA.\n"
        "- Identification of major risks and potential opportunities.\n"
        "- Visuals or tables summarizing important financial and technical metrics.\n"
        "- A concise summary of overall stock outlook based on the analysis."
    ),
    name = "Analysis",
    agent = Analyst,
    context=(research,)
)


reporting = Task(
    description = (
        "1. Review the analysis report for {stock}, including all key findings and metrics.\n"
        "2. Summarize the most important insights in clear, jargon-free language.\n"
        "3. Provide actionable recommendations for investors, such as buy/hold/sell guidance, with supporting rationale.\n"
        "4. Highlight any critical risks, uncertainties, or factors that could affect investment decisions."
        "5. If it's a buy, say BUY, if it's a hold, say HOLD, if it's a sell, say SELL"
        "6. Use quantitative metrics like Strong Buy, Buy, Hold, Sell, Strong Sell to indicate the strength of the recommendation."
    ),
    expected_output = (
        "A concise investment report that includes:\n"
        "- An executive summary of the stock’s outlook.\n"
        "- Clear, actionable recommendations (e.g., buy, hold, sell) with supporting arguments.\n"
        "- A summary of key risks and considerations for potential investors.\n"
        "- Well-structured sections for easy reading and decision-making."
    ),
    name = "Reporting",
    agent = DecisionAdvisor,
    context= (research, analysis)

)

