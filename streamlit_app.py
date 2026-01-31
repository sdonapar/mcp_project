#!/usr/bin/env python3

import streamlit as st
from agent import run_agent
import dotenv
import json
import os
from datetime import datetime

dotenv.load_dotenv()

# Query log file path
QUERY_LOG_FILE = "logs/query_logs.json"

# Ensure logs directory exists
os.makedirs(os.path.dirname(QUERY_LOG_FILE), exist_ok=True)


def load_query_logs():
    """Load existing query logs from JSON file"""
    if os.path.exists(QUERY_LOG_FILE):
        with open(QUERY_LOG_FILE, "r") as f:
            return json.load(f)
    return []

def save_query_log(query: str, response: str, success: bool, error_message: str = None):
    """Save a query and its response to the JSON log file"""
    logs = load_query_logs()
    
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "query": query,
        "response": response,
        "success": success,
        "error_message": error_message
    }
    
    logs.append(log_entry)
    
    with open(QUERY_LOG_FILE, "w") as f:
        json.dump(logs, f, indent=2)

# Streamlit page configuration
st.set_page_config(
    page_title="DB Utils Agent",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Database Query Agent")
st.markdown("Ask questions about your e-commerce data using natural language")

# System message
SYSTEM_MESSAGE = """
You are a data analysis assistant. Use the provided tools to answer questions about the data present in DuckDB. There are 6 tables available: orders, order_items, order_item_refunds, products, website_pageviews, and website_sessions. First, use the get_table_schema tool to understand the structure of the tables. created_at is a text column, do explicit type casting of this column to extract timestamp. Then, use the run_sql tool to execute SQL queries to retrieve the necessary information to answer the user's question. Always think step-by-step and ensure your SQL queries are accurate."""

# Sidebar for example queries
with st.sidebar:
    # Dataset information
    st.header("📦 Dataset Information")
    st.markdown("**Dataset:** Maven Analytics - Toy Store E-Commerce")
    
    st.subheader("📋 Available Tables")
    tables = [
        "orders",
        "order_items",
        "order_item_refunds",
        "products",
        "website_pageviews",
        "website_sessions"
    ]
    for table in tables:
        st.text(f"• {table}")
    
    st.markdown("---")
    
    st.header("📝 Example Queries")
    st.markdown("""
    Try asking questions like:
    - List top 5 products that have max returns
    - What is the total revenue by product?
    - Show me the top 10 customers by spending
    - How many orders were placed each month?
    - What is the average order value?
    """)
    
    st.markdown("---")
    
    st.header("📊 Query History")
    logs = load_query_logs()
    if logs:
        st.metric("Total Queries", len(logs))
        successful = sum(1 for log in logs if log["success"])
        failed = len(logs) - successful
        col1, col2 = st.columns(2)
        col1.metric("Successful", successful)
        col2.metric("Failed", failed)
        
        # Create dropdown options from recent queries
        recent_logs = list(reversed(logs[-10:]))  # Show last 10 queries
        query_options = [f"{'✅' if log['success'] else '❌'} {log['timestamp']}" for log in recent_logs]
        
        selected_query = st.selectbox("View Query Logs:", query_options, label_visibility="collapsed")
        
        if selected_query:
            selected_index = query_options.index(selected_query)
            log = recent_logs[selected_index]
            
            st.subheader("Query Details")
            st.code(log['query'], language='text')
            
            if log['success']:
                st.markdown("**Response:**")
                st.markdown(log['response'])
            else:
                st.error(f"Error: {log['error_message']}")
    else:
        st.info("No queries logged yet.")

# Main query input
st.markdown("### Enter your question:")
query = st.text_area(
    "Ask a question about your database:",
    placeholder="e.g., What are the top 5 products by sales?",
    height=100,
    label_visibility="collapsed"
)

col1, col2 = st.columns([1, 4])
with col1:
    submit_button = st.button("🔍 Run Query", type="primary")

# Run agent when button is clicked
if submit_button:
    if not query.strip():
        st.warning("Please enter a query first!")
    else:
        with st.spinner("Processing your query..."):
            try:
                result = run_agent(SYSTEM_MESSAGE, query)
                
                # Save successful query log
                save_query_log(query, result, success=True)
                
                # Display results
                st.success("Query executed successfully!")
                st.markdown("### Response:")
                st.markdown(result)
                
            except Exception as e:
                error_msg = str(e)
                
                # Save failed query log
                save_query_log(query, "", success=False, error_message=error_msg)
                
                st.error(f"Error executing query")
                st.error("Please make sure the MCP server is running and your query is valid.")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: gray; font-size: 0.8em;">
    Powered by LangChain + MCP + DuckDB | Data from Maven Analytics
</div>
""", unsafe_allow_html=True)
