# Multi-Agent Stock Analyzer

**Empowering smarter investment decisions with AI-driven agents.**

This project is an end-to-end platform for automated stock analysis and investment advisory, leveraging a multi-agent architecture (CrewAI) to orchestrate research, analytics, and actionable recommendations. The system integrates real-time data sources, advanced sentiment analysis, and extensible tooling—making it a robust foundation for both retail investors and quant developers.

---

## 🚀 Key Features

- **Automated Stock Research:**  
  Aggregates up-to-the-minute market news, company financials, and sentiment signals from sources like Reddit and GNews.
- **Multi-Agent Analysis Pipeline:**  
  Specialized agents for data gathering, financial/technical analysis, and decision recommendation.
- **Actionable Investment Guidance:**  
  Generates clear, graded advice (Buy, Hold, Sell) with supporting rationale and risk summary.
- **Extensible Tools:**  
  Modular integration with search, scraping, and sentiment tools—plus planned support for broker APIs (e.g. Zerodha).
- **Live Data, Not Cached:**  
  Ensures every analysis is based on fresh, real-world signals.

---

## 🧠 System Architecture

### Agents

| Agent                   | Responsibilities                                                                                      |
|-------------------------|------------------------------------------------------------------------------------------------------|
| **Market Data Researcher** | Scrapes and collects the latest news, financials, and sector insights for a given stock.             |
| **Analyst**             | Runs both fundamental (P/E, growth, metrics) and technical analyses (trend, price signals).            |
| **Decision Advisor**    | Synthesizes research and analysis into a human-readable investment report with clear recommendations.  |

### Integrated Tools

- **Scrape & Search Tool:**  
  Hybrid web search, scraper, and parser for gathering real-time data.
- **NewsTool (GNews):**  
  Macro/global headlines focused on relevant stocks/events.
- **MarketSentimentTool:**  
  Reddit-based sentiment extraction for crowd psychology.
- **SerperDevTool:**  
  Targeted scholarly/financial search.
- **Planned:**  
  Broker integration (Zerodha), portfolio analytics, and additional social data feeds.

---

## ⚙️ Getting Started

### Prerequisites

- Python 3.9+
- API keys for all integrated services:
  - `OPEN_AI_KEY`, `GOOGLE_API_KEY`, `GROQ_API_KEY`, `SERPER_API_KEY`, `GNEWS_KEY`, `REDDIT_CLIENT_ID`, `REDDIT_CLIENT_SECRET`
- Set environment variables in your `.env` file.

### Installation

```bash
pip install -r requirements.txt
```

### Usage

```python
from crewai import Crew

# Prepare agents and tasks as per your use-case
result = crew.kickoff(inputs={"stock": "RELIANCE"})
print(result)
```

- Change `"stock": "RELIANCE"` to any ticker or company name of interest.
- Agents, tools, and logic are modular—customize for your needs!

---

## 📊 Outputs

- **Research Summary:**  
  Concise aggregation of latest news, events, and company fundamentals.
- **Analysis Report:**  
  Metric-heavy, with tables or visual summaries.
- **Investment Recommendation:**  
  Graded advice (Buy/Sell/Hold), rationale, and risk/opportunity breakdown.

---

## 🛣️ Roadmap

- ✅ Broker API integration (Zerodha Kite Connect) for live trading and portfolio management.
- ✅ Strategy automation—run trades on agent-generated signals.
- 🔜 Advanced sentiment and alternative data sources (Twitter, global feeds).
- 🔜 Multi-agent RL for evolving trading strategies.

---

## 🧩 Extending & Contributing

This is a work-in-progress towards a fully autonomous, AI-native trading platform.

**Ways to contribute:**
- Build new tools (scrapers, analytics, alternative data integrations)
- Expand agent logic for new asset classes or markets
- Help with broker API integrations
- Collaborate on reinforcement learning or advanced strategy modules

**Get involved:**
- Fork or clone the repo and run locally
- Open issues for bugs, feature requests, or suggestions
- Submit pull requests for improvements

---

## ⚠️ Disclaimer

- All API keys required—**set them in your `.env` file**.
- Analyses use live data—no stale/cached information.
- Data-driven suggestions only; always cross-check before making investment decisions.

---

## 🙌 Join the Evolution

Interested in AI, trading, LLMs, or financial automation?  
Collaborate with us—help build the next generation of autonomous investment platforms!

---

**Sample Output:**  
_Automated research, analysis, and investment recommendation for Reliance Industries._
