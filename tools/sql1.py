from typing import List
from langchain.pydantic_v1 import BaseModel, Field
import sqlite3
from langchain.tools import BaseTool, StructuredTool, tool

import langchain
langchain.debug= True

conn= sqlite3.connect("db.sqlite")

def list_tables():
    c= conn.cursor()
    c.execute("select name from sqlite_master where type= 'table'; ")
    rows= c.fetchall()
    return "\n".join(row[0] for row in rows if row[0] is not None)

## define classes

# class RunQueryArgsSchema(BaseModel):
#     query : str = Field(description="The string argument for this tool")

# class DescribeTablesArgsSchema(BaseModel):
#     table_names : List[str] = Field(description="The list of string argument for this tool")

## define functions
@tool("run_query_tool",  return_direct= True )
def run_query_tool(query: str) -> str:
    """run a sql query"""
    c= conn.cursor()
    try:   
        c.execute(query)
        return c.fetchall()
    except sqlite3.OperationalError as err:
        return f"The following error occured: {str(err)}"

@tool("describe_tables_tool",  return_direct= True)   
def describe_tables_tool(table_names: List[str]):
    """Given a list of table names, returns the schema of those tables"""
    c= conn.cursor()
    tables= ','.join("'" + tab + "'" for tab in table_names)
    rows= c.execute(f"select sql from sqlite_master where type= 'table' and name in ({tables});")
    return "\n".join(row[0] for row in rows if row[0] is not None)

