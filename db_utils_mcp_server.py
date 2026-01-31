#!/usr/bin/env python3

import duckdb
from fastmcp import FastMCP
from time import time

mcp = FastMCP("DB Utils MCP Server")

def get_connection():
    """
    Establishes a connection to the DuckDB database.

    Returns:
        duckdb.DuckDBPyConnection: A connection object to the DuckDB database.
    """
    view_sqls = [
        "CREATE TEMPORARY VIEW orders as select * from read_parquet('data/orders.parquet')",
        "CREATE TEMPORARY VIEW order_items as select * from read_parquet('data/order_items.parquet')",
        "CREATE TEMPORARY VIEW order_item_refunds as select * from read_parquet('data/order_item_refunds.parquet')",
        "CREATE TEMPORARY VIEW products as select * from read_parquet('data/products.parquet')",
        "CREATE TEMPORARY VIEW website_pageviews as select * from read_parquet('data/website_pageviews.parquet')",
        "CREATE TEMPORARY VIEW website_sessions as select * from read_parquet('data/website_sessions.parquet')",
    ]

    conn = duckdb.connect()

    for view_sql in view_sqls:
        conn.execute(view_sql)
    return conn


@mcp.tool
def run_sql(sql_query: str) -> str:
    """
    Executes a SQL query on a DuckDB database.

    Args:
        sql_query (str): The SQL query to execute.

    Returns:
        str: The result of the SQL query as JSON list of records
    """
    
    # Connect to the DuckDB database
    conn = get_connection()
    # Execute the SQL query
    start_time = time()
    result_df = conn.execute(sql_query).fetchdf()
    end_time = time()
    result_json = result_df.to_json(orient="records")
    return result_json

@mcp.tool
def get_table_schema(table_name: str) -> str:
    """
    Retrieves the schema of a specified table in the DuckDB database.

    Args:
        table_name (str): The name of the table whose schema is to be retrieved.

    Returns:
        str: A JSON string containing the schema information of the table.
    """

    conn = get_connection()

    # Get the schema without quotes around table name
    sql_query = f"PRAGMA table_info({table_name})"
    result_df = conn.execute(sql_query).fetchdf()
    result_json = result_df.to_json(orient="records")
    return result_json

if __name__ == "__main__":
    mcp.run(transport="stdio")