# MCP Project - DB Utils MCP Server

A Model Context Protocol (MCP) server that provides database utilities for querying e-commerce data using DuckDB and LangChain.

## Overview

This project implements an MCP server that exposes database tools for:
- Executing SQL queries on e-commerce datasets
- Retrieving table schemas
- Processing parquet files from the Maven Analytics Toy Store dataset

## Setup

### Prerequisites
- Python 3.12 or higher
- `uv` package manager

### Installation

1. Clone or navigate to the project directory:
```bash
cd /Users/sdonapar/Documents/mcp_project
```

2. Install dependencies using `uv`:
```bash
uv sync
```

3. Download the dataset from Maven Analytics:
   - Visit: https://mavenanalytics.io/data-playground/toy-store-e-commerce-database
   - Download the dataset and unzip it in the `data/` directory

4. Convert CSV files to Parquet format (optional, for better performance):
```bash
uv run data/csv_to_parquet.py
```

## Project Structure

```
├── db_utils_mcp_server.py    # MCP server with database tools
├── agent.py                   # LangChain agent using the MCP tools
├── main.py                    # Main entry point
├── pyproject.toml            # Project configuration
├── README.md                 # This file
└── data/                     # Dataset directory
    ├── orders.parquet
    ├── order_items.parquet
    ├── order_item_refunds.parquet
    ├── products.parquet
    ├── website_pageviews.parquet
    ├── website_sessions.parquet
    └── [CSV files]
```

## Available Tools

### run_sql
Executes a SQL query on the DuckDB database.

**Parameters:**
- `sql_query` (str): The SQL query to execute

**Returns:**
- JSON list of records

### get_table_schema
Retrieves the schema of a specified table.

**Parameters:**
- `table_name` (str): The name of the table

**Returns:**
- JSON string containing schema information

## Usage

### Running the MCP Server
```bash
uv run db_utils_mcp_server.py
```

### Running the Agent (CLI)
```bash
uv run agent.py
```

The agent uses GPT-4o-mini with the MCP tools to answer database queries conversationally.

### Running the Streamlit Web App
```bash
streamlit run streamlit_app.py
```

This launches an interactive web interface where you can:
- Input natural language queries
- See responses in real-time
- View example queries in the sidebar

## Available Tables

- `orders` - Order information
- `order_items` - Individual items in orders
- `order_item_refunds` - Refund information
- `products` - Product catalog
- `website_pageviews` - Page view events
- `website_sessions` - Session information

## Configuration

Ensure you have an OpenAI API key set in your environment:
```bash
export OPENAI_API_KEY="your-api-key"
```

## Dependencies

- **duckdb** - SQL database engine
- **fastmcp** - MCP server framework
- **langchain** - LLM framework
- **langchain-mcp-adapters** - Bridge between LangChain and MCP
- **langchain-openai** - OpenAI integration
- **pandas** - Data manipulation
- **pyarrow** - Arrow data format support
- **fastparquet** - Parquet file support
- **streamlit** - (Optional) Web UI support

## Notes

- The project uses temporary views in DuckDB to expose data as tables
- Parquet files are preferred over CSV for better performance
- Each MCP tool is self-contained and cannot call other tools directly
