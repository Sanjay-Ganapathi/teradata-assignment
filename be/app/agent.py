import os
from langchain.tools.retriever import create_retriever_tool
from langchain_openai import AzureChatOpenAI
from langgraph.graph import END, StateGraph, START
from app.vector_store import retriever
from langgraph.graph import MessagesState
from langgraph.prebuilt import ToolNode, tools_condition
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.tools import tool


llm = AzureChatOpenAI(azure_deployment=os.getenv(
    'AZURE_OPENAI_MODEL'), api_version="2024-10-21")


retriever_tool = create_retriever_tool(
    retriever,
    name="document_retriever",
    description="Search for information in the uploaded documents. Use this tool to answer questions about the content of the files.",
)


@tool
def calculator(expression: str):
    """
    Use this tool to evaluate mathematical expressions.
    Example: 'What is 2 + 2 * 10?' -> calculator(expression="2 + 2 * 10")
    """

    try:
        print(expression)
        allowed_chars = "0123456789+-*/.() "
        if all(char in allowed_chars for char in expression):
            return eval(expression)
        else:
            return "Error: Invalid characters in expression"
    except Exception as e:
        return f"Error: {e}"


SYSTEM_PROMPT = """
You are an expert question-answering assistant. You have access to a tool called 'document_retriever'.
Your ONLY source of information is the set of documents that the user has uploaded. You MUST use the 'document_retriever' tool to find relevant information to answer the user's questions.
You are strictly forbidden from answering questions using your own internal knowledge or any information outside of the provided documents.
For any user question that is not a simple greeting (like 'hello' or 'thank you'), you MUST call the 'document_retriever' tool. Do not try to answer from memory.
You also have access to calculator tool for calculations.
"""

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", SYSTEM_PROMPT),
        MessagesPlaceholder(variable_name="messages"),
    ]
)


az_agent = llm.bind_tools([retriever_tool, calculator])

agent = prompt | az_agent

workflow = StateGraph(MessagesState)


def call_agent(state: MessagesState):
    # print("---NODE: CALLING AGENT ---")
    response = agent.invoke(state["messages"])

    return {"messages": [response]}


tool_node = ToolNode([retriever_tool, calculator])

workflow.add_node("agent", call_agent)
workflow.add_node("retrieve_documents", tool_node)


workflow.add_edge(START, "agent")

workflow.add_conditional_edges(
    "agent",

    tools_condition,
    {

        "tools": "retrieve_documents",

        END: END,
    },
)
workflow.add_edge("retrieve_documents", "agent")

agent_app = workflow.compile()
