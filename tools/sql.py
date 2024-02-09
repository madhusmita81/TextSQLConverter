from typing import List
from pydantic.v1 import BaseModel, Field
import sqlite3
from langchain.tools import Tool

import langchain
langchain.debug= True

conn= sqlite3.connect("db.sqlite")

def list_tables():
    c= conn.cursor()
    c.execute("select name from sqlite_master where type= 'table'; ")
    rows= c.fetchall()
    return "\n".join(row[0] for row in rows if row[0] is not None)

## define functions

def run_sqlite_query(query):
    c= conn.cursor()
    try:   
        c.execute(query)
        return c.fetchall()
    except sqlite3.OperationalError as err:
        return f"The following error occured: {str(err)}"
    
def describe_tables(table_names):
    c= conn.cursor()
    tables= ','.join("'" + tab + "'" for tab in table_names)
    rows= c.execute(f"select sql from sqlite_master where type= 'table' and name in ({tables});")
    return "\n".join(row[0] for row in rows if row[0] is not None)

## define classes

class RunQueryArgsSchema(BaseModel):
    query : str = Field(description="The string argument for this tool")

class DescribeTablesArgsSchema(BaseModel):
    table_names : List[str] = Field(description="The list of string argument for this tool")


## define func used by chatgpt    

run_query_tool= Tool.from_function(name= "run_sqlite_query",
                                   description= "Run a sqlite query",
                                   func= run_sqlite_query,
                                   args_schema= RunQueryArgsSchema,
                                   verbose= True)

describe_tables_tool= Tool.from_function(
    name= "describe_tables",
    description= "Given a list of table names, returns the schema of those tables",
    func= describe_tables,
    args_schema= DescribeTablesArgsSchema,
    verbose= True
    )
