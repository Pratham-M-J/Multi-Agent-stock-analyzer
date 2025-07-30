# Multi-Agent Stock Analysis & Advisory Platform

This repository delivers an **AI-powered pipeline for end-to-end stock research, analysis, and investment recommendations**. Built on CrewAI, it uses several agents, each tasked with a specific part of the financial due diligence process, combining real-time web data, news, quantitative analysis, and sentiment checks.

---

## 🚦 Overview

- **Automates stock research** by collecting and analyzing:
  - The latest global news (geopolitics, government actions)
  - Company financials and key metrics
  - Social and news sentiment (via Reddit, GNews)
  - Market/technical/fundamental signals
- **Generates clear, actionable investment guidance** (Strong Buy, Buy, Hold, etc.)
- **Planned features:** Broker account integration (e.g., Zerodha) and portfolio analytics

---

## 🏗 System Structure

### Agents

| Agent               | Role & Function                                                                                         |
|---------------------|--------------------------------------------------------------------------------------------------------|
| Market Data Researcher | Gathers up-to-date news, financials, and industry info. No assumptions—fresh data only.                 |
| Analyst             | Performs both fundamental (P/E, growth) and technical (price/trend) analysis; assesses risks & upsides. |
| Decision Advisor    | Generates a high-level investment report & actionable recommendation (with rationale & risk summary).    |

### Tools

- **Scrape and Search Tool:** Hybrid Google search, link parser, and web data scraper (limited to 2 runs per research).
- **NewsTool (GNews):** Shows latest macro/global headlines, tailored to stock or events.
- **MarketSentimentTool:** Pulls Reddit posts and comments for real-world, crowd-driven sentiment.
- **SerperDevTool:** Runs targeted search requests on scholarly/financial topics.
- **Portfolio/Trade Automation (Planned):** Zerodha & portfolio review capability.

---

## ⚙️ How to Use

1. **Prerequisites**
    - Python 3.9+
    - Set environment variables for all API keys:
        - `OPEN_AI_KEY`, `GOOGLE_API_KEY`, `GROQ_API_KEY`, `SERPER_API_KEY`, `GNEWS_KEY`, `REDDIT_CLIENT_ID`, `REDDIT_CLIENT_SECRET`
2. **Install**
    ```
    pip install -r requirements.txt
    ```
3. **Run**
    ```
    from crewai import Crew
    # Make sure agents/tasks are imported
    result = crew.kickoff(inputs={"stock": "OlaElectric"})
    print(result)
    ```
4. **Customize**
    - Change `"stock": "OlaElectric"` to any ticker or company name.
    - Modify/extend agents, tools, or logic as desired.

---

## 🟢 Outputs

- **Research summary:** Latest news, events, and core company data.
- **Analysis report:** In-depth, metric-heavy, with tables or visual summaries.
- **Investment report:** Actionable and graded advice—BUY, SELL, HOLD, etc.—with concise risks/opportunities.

---

## 📦 Roadmap & Extensibility

- Plug in other broking APIs to automate real trades.
- Ask the system to review your portfolio or rate its risk/reward.
- Add advanced data or social sentiment tools (Twitter, global feeds).

---

Output: Complete research, analytics, and an investment recommendation for Reliance.

---

## 🛑 Important

- **API keys required for all tools**—set in `.env`.
- No outdated/cached—always-live data.
- This system provides **data-driven suggestions**; always cross-check major investment decisions.

---

## 👋 Contributing / Next Steps

- Add scrapers, analytics, and broker connectors.
- Extend to more markets and asset classes.
- Join in to evolve the next-gen investment pipeline!

---


