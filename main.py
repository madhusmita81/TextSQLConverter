from langchain_community.chat_models import ChatOpenAI    
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder, HumanMessagePromptTemplate
from langchain.agents import OpenAIFunctionsAgent, AgentExecutor
from tools.sql import list_tables, run_query_tool, describe_tables_tool 
from tools.report import write_report_tool
from langchain.schema import SystemMessage
from langchain.memory import ConversationBufferMemory
from langchain_community.tools.convert_to_openai import format_tool_to_openai_function


from dotenv import load_dotenv
load_dotenv()

llm= ChatOpenAI()
tables= list_tables()
prompt = ChatPromptTemplate(
    messages=[
        SystemMessage(content=(
            "You are an AI that has access to a SQLite database.\n"
            f"The database has tables of: {tables}\n"
            "Do not make any assumptions about what tables exist "
            "or what columns exist. Instead, use the 'describe_tables' function"
        )),
       MessagesPlaceholder(variable_name= "chat_history"),
        HumanMessagePromptTemplate.from_template("{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad")
    ]
)


tools= [run_query_tool, describe_tables_tool, write_report_tool]
memory= ConversationBufferMemory(memory_key= "chat_history", return_messages= True)
      

agent= OpenAIFunctionsAgent(llm= llm,
                            prompt= prompt,
                            tools= tools)
agent_executor= AgentExecutor(agent= agent,
                              verbose= True,
                              tools= tools,
                              memory= memory,
                              handle_parsing_errors=True)

agent_executor(
    "How many orders are there? Write the result to an html report."
)
print("2nd executer")
agent_executor(
    "Repeat the exact same process for users."
)

