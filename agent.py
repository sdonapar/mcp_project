from langchain_mcp_adapters.client import MultiServerMCPClient  
from langchain.agents import create_agent
import asyncio
import dotenv
import json

dotenv.load_dotenv()

client = MultiServerMCPClient(  
    {
        "dbuitls": {
            "transport": "stdio",  # Local subprocess communication
            "command": "/Users/sdonapar/.local/bin/uv",
            # Absolute path to your math_server.py file
            "args": ["--directory", "/Users/sdonapar/Documents/mcp_project", "run", "db_utils_mcp_server.py"]
        }
    }
)

tools = asyncio.run(client.get_tools())

agent = create_agent(
    "gpt-4.1",
    tools
)

def run_agent(system_message: str, query: str) -> str:
    response =  asyncio.run(agent.ainvoke(
            {"messages" : [{"role":"assistant", "content": system_message}, {"role": "user", "content": query}]}
        ))
    return response["messages"][-1].content

if __name__ == "__main__":
    test_query = "List top 5 products that has max returns"
    system_message = """
    You are a data analysis assistant. Use the provided tools to answer questions about the data present in DuckDB. There are 6 tables available: orders, order_items, order_item_refunds, products, website_pageviews, and website_sessions. First, use the get_table_schema tool to understand the structure of the tables. Then, use the run_sql tool to execute SQL queries to retrieve the necessary information to answer the user's question. Always think step-by-step and ensure your SQL queries are accurate."""
    response =  run_agent(system_message, test_query)
    print("Agent Response:")
    print(response)