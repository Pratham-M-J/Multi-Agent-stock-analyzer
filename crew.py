import streamlit as st
from crewai import Crew
from Tasks import research, analysis, reporting, sentiment_analysis
from Agents import Researcher, Analyst, DecisionAdvisor, Sentiment_analyser
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
import os
from langchain.vectorstores import Chroma
from langchain.embeddings import HuggingFaceEmbeddings
from langchain_openai import ChatOpenAI
from langchain.chains import RetrievalQA
import tempfile
import shutil

# Load environment variables
load_dotenv()

# Page config
st.set_page_config(
    page_title="Stock Analysis Crew",
    page_icon="📈",
    layout="wide"
)

# Initialize session state
if 'analysis_result' not in st.session_state:
    st.session_state.analysis_result = None
if 'vectordb' not in st.session_state:
    st.session_state.vectordb = None
if 'stock_symbol' not in st.session_state:
    st.session_state.stock_symbol = None

def initialize_crew():
    """Initialize the CrewAI crew"""
    try:
        crew = Crew(
            agents=[Researcher, Sentiment_analyser, Analyst, DecisionAdvisor],
            tasks=[research, sentiment_analysis, analysis, reporting],
            verbose=True
        )
        return crew
    except Exception as e:
        st.error(f"Error initializing crew: {str(e)}")
        return None

def get_llm_recommendation(stock, result):
    """Get LLM recommendation based on analysis"""
    try:
        google_api_key = os.getenv("GOOGLE_API_KEY")
        if not google_api_key:
            st.error("Google API key not found. Please set GOOGLE_API_KEY in your environment variables.")
            return None
            
        llm = ChatGoogleGenerativeAI(
            google_api_key=google_api_key,
            model="gemini-2.0-flash",
            temperature=0.1,
        )
        
        prompt = f"Here is the analysis report for {stock}:\n{result}\n\nBased on this analysis, provide a recommendation: 'BUY', 'SELL', or 'HOLD'. Only respond with one of these three words."
        response = llm.invoke(prompt)
        return response.content.strip().upper()
    except Exception as e:
        st.error(f"Error getting LLM recommendation: {str(e)}")
        return None

def setup_rag_system(analysis_text):
    """Setup RAG system with the analysis results"""
    try:
        # Create embedding model
        embedding_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        
        # Convert result to list of text chunks if it's a string
        if isinstance(analysis_text, str):
            # Split the text into smaller chunks for better retrieval
            text_chunks = [analysis_text[i:i+1000] for i in range(0, len(analysis_text), 800)]
        else:
            text_chunks = [str(analysis_text)]
        
        # Create metadata for each chunk
        metadatas = [{"source": f"analysis_chunk_{i}", "chunk_id": i} for i in range(len(text_chunks))]
        
        # Create temporary directory for this session
        temp_dir = tempfile.mkdtemp()
        chroma_dir = os.path.join(temp_dir, "chroma_db")
        
        # Create vector database
        vectordb = Chroma.from_texts(
            texts=text_chunks,
            embedding=embedding_model,
            metadatas=metadatas,
            persist_directory=chroma_dir
        )
        
        vectordb.persist()
        
        return vectordb, chroma_dir
    except Exception as e:
        st.error(f"Error setting up RAG system: {str(e)}")
        return None, None

def query_rag_system(vectordb, query):
    """Query the RAG system"""
    try:
        openai_api_key = os.getenv("OPEN_AI_KEY")
        if not openai_api_key:
            st.error("OpenAI API key not found. Please set OPEN_AI_KEY in your environment variables.")
            return None
            
        llm = ChatOpenAI(
            model_name="gpt-3.5-turbo", 
            temperature=0, 
            openai_api_key=openai_api_key
        )
        
        qa_chain = RetrievalQA.from_chain_type(
            llm=llm,
            retriever=vectordb.as_retriever(search_kwargs={"k": 3}),
            return_source_documents=True
        )
        
        result = qa_chain({"query": query})
        return result
    except Exception as e:
        st.error(f"Error querying RAG system: {str(e)}")
        return None

# Main UI
st.title("🚀 Stock Analysis Crew")
st.markdown("---")

st.markdown("""
This application helps you analyze stocks by:
- 📊 Gathering comprehensive stock data
- 💭 Analyzing market sentiment
- 📈 Performing technical and fundamental analysis
- 📋 Generating detailed reports
- 🤖 Providing AI-powered recommendations
""")

# Sidebar for configuration
with st.sidebar:
    st.header("⚙️ Configuration")
    
    # Check API keys
    google_key = os.getenv("GOOGLE_API_KEY")
    openai_key = os.getenv("OPEN_AI_KEY")
    
    st.markdown("**API Key Status:**")
    st.write("🔑 Google API:", "✅ Configured" if google_key else "❌ Missing")
    st.write("🔑 OpenAI API:", "✅ Configured" if openai_key else "❌ Missing")
    
    if not google_key:
        st.warning("Google API key is required for analysis")
    if not openai_key:
        st.warning("OpenAI API key is required for RAG queries")

# Main content
col1, col2 = st.columns([2, 1])

with col1:
    st.header("📈 Stock Analysis")
    
    # Service selection
    service_option = st.selectbox(
        "Select Service:",
        ["Analyze a Stock", "Analyze Portfolio (Coming Soon)"],
        index=0
    )
    
    if service_option == "Analyze a Stock":
        # Stock input
        stock_symbol = st.text_input(
            "Enter Stock Symbol:",
            placeholder="e.g., AAPL, GOOGL, TSLA",
            help="Enter the stock ticker symbol you want to analyze"
        )
        
        # Analysis button
        if st.button("🔍 Start Analysis", type="primary", disabled=not stock_symbol):
            if not os.getenv("GOOGLE_API_KEY"):
                st.error("Please configure your Google API key in the environment variables.")
            else:
                with st.spinner(f"Analyzing {stock_symbol.upper()}... This may take a few minutes."):
                    # Initialize crew
                    crew = initialize_crew()
                    
                    if crew:
                        try:
                            # Run analysis
                            result = crew.kickoff(inputs={"stock": stock_symbol.upper()})
                            
                            # Store results in session state
                            st.session_state.analysis_result = str(result)
                            st.session_state.stock_symbol = stock_symbol.upper()
                            
                            # Setup RAG system
                            vectordb, chroma_dir = setup_rag_system(str(result))
                            if vectordb:
                                st.session_state.vectordb = vectordb
                                st.session_state.chroma_dir = chroma_dir
                            
                            st.success("Analysis completed!")
                            st.rerun()
                            
                        except Exception as e:
                            st.error(f"Error during analysis: {str(e)}")
    
    else:
        st.info("Portfolio analysis feature is coming soon! Please check back later.")

with col2:
    st.header("🎯 Quick Actions")
    
    if st.session_state.analysis_result:
        st.success(f"✅ Analysis completed for {st.session_state.stock_symbol}")
        
        # Get recommendation
        if st.button("💡 Get AI Recommendation"):
            with st.spinner("Getting recommendation..."):
                recommendation = get_llm_recommendation(
                    st.session_state.stock_symbol, 
                    st.session_state.analysis_result
                )
                if recommendation:
                    # Style the recommendation
                    if recommendation == "BUY":
                        st.success(f"🟢 **Recommendation: {recommendation}**")
                    elif recommendation == "SELL":
                        st.error(f"🔴 **Recommendation: {recommendation}**")
                    else:  # HOLD
                        st.warning(f"🟡 **Recommendation: {recommendation}**")
    else:
        st.info("Run an analysis first to see quick actions")

# Display results
if st.session_state.analysis_result:
    st.markdown("---")
    st.header(f"📊 Analysis Results for {st.session_state.stock_symbol}")
    
    # Create tabs for different views
    tab1, tab2 = st.tabs(["📋 Full Report", "❓ Ask Questions"])
    
    with tab1:
        st.markdown("### Detailed Analysis Report")
        st.text_area(
            "Analysis Report:",
            value=st.session_state.analysis_result,
            height=400,
            disabled=True
        )
        
        # Download button
        st.download_button(
            label="📥 Download Report",
            data=st.session_state.analysis_result,
            file_name=f"{st.session_state.stock_symbol}_analysis_report.txt",
            mime="text/plain"
        )
    
    with tab2:
        st.markdown("### Ask Questions About the Analysis")
        
        if st.session_state.vectordb:
            # Query input
            user_query = st.text_input(
                "Ask a question about the analysis:",
                placeholder="e.g., What are the main risks? What's the price target?",
                help="Ask specific questions about the stock analysis"
            )
            
            # Query button
            if st.button("🤔 Ask Question", disabled=not user_query):
                if not os.getenv("OPEN_AI_KEY"):
                    st.error("Please configure your OpenAI API key to use the Q&A feature.")
                else:
                    with st.spinner("Searching for answer..."):
                        rag_result = query_rag_system(st.session_state.vectordb, user_query)
                        
                        if rag_result:
                            st.markdown("### 💬 Answer")
                            st.write(rag_result['result'])
                            
                            # Show sources
                            if rag_result.get('source_documents'):
                                with st.expander("📚 Sources"):
                                    for i, doc in enumerate(rag_result['source_documents']):
                                        st.markdown(f"**Source {i+1}:**")
                                        st.text(doc.page_content[:300] + "..." if len(doc.page_content) > 300 else doc.page_content)
        else:
            st.info("RAG system not available. Please run an analysis first.")

# Footer
st.markdown("---")
st.markdown("*Built with CrewAI, LangChain, and Streamlit*")