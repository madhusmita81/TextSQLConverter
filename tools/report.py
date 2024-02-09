# Import things that are needed generically
from langchain.pydantic_v1 import BaseModel, Field
from langchain.tools import BaseTool, StructuredTool, tool

def write_report(filename, html):
    with open (filename, 'w') as f:
        f.write(html)

class WriteReportArgsSchema(BaseModel):
    filename: str
    html: str

write_report_tool= StructuredTool.from_function(
    name= "write_report",
    description= "Write a HTML file to disk. Use this tool whenever someone asks for a report.",
    func= write_report,
    args_schema= WriteReportArgsSchema
)