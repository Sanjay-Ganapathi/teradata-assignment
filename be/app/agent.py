import os
from typing import List, TypedDict, Sequence
from typing_extensions import Annotated
from langchain_core.documents import Document
from langchain_core.prompts import ChatPromptTemplate
from langchain.tools.retriever import create_retriever_tool
from langchain_openai import AzureChatOpenAI, AzureOpenAIEmbeddings
from langgraph.graph import END, StateGraph, START
from langgraph.graph.message import add_messages
from app.vector_store import retriever
from langchain_core.messages import BaseMessage, ToolMessage, HumanMessage, SystemMessage
from langgraph.graph import MessagesState
from langgraph.prebuilt import ToolNode, tools_condition

llm = AzureChatOpenAI(azure_deployment=os.getenv(
    'AZURE_OPENAI_MODEL'), api_version="2024-10-21")

retriever_tool = create_retriever_tool(
    retriever,
    name="document_retriever",
    description="Search for information in the uploaded documents. Use this tool to answer questions about the content of the files.",
)

az_agent = llm.bind_tools([retriever_tool])

workflow = StateGraph(MessagesState)


def call_agent(state: MessagesState):
    print("---NODE: CALLING AGENT BRAIN---")
    response = az_agent.invoke(state["messages"])

    return {"messages": [response]}


document_retriever_node = ToolNode([retriever_tool])

workflow.add_node("agent", call_agent)
workflow.add_node("retrieve_documents", document_retriever_node)


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
