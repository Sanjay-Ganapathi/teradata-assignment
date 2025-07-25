
import os
from typing import AsyncGenerator, List, Literal
from pydantic import BaseModel
import uvicorn
from fastapi import FastAPI, File, HTTPException, UploadFile
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage, AIMessage, BaseMessage
import asyncio
from fastapi.responses import StreamingResponse
from app.vector_store import process_and_store_document
from app.agent import agent_app

load_dotenv()

# TODO change title and description
app = FastAPI(
    title="Intelligent Agent Chatbot API",
    description="An API for a RAG-based chatbot using LangGraph and FastAPI.",

)


class UploadResponse(BaseModel):
    filename: str
    message: str


class ChatMessage(BaseModel):
    role: Literal["user", "assistant"]
    content: str


class ChatRequest(BaseModel):
    messages: List[ChatMessage]


class ChatResponse(BaseModel):
    answer: str


@app.get("/")
def read_root():

    return {"status": "ok", "message": "All services are working fine!"}


@app.post("/upload", response_model=UploadResponse, tags=["Document Management"])
async def upload_document(file: UploadFile = File(...)):

    allowed_extensions = {".txt", ".pdf"}
    file_extension = os.path.splitext(file.filename)[1].lower()

    if file_extension not in allowed_extensions:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file type '{file_extension}'. Please upload a .txt or .pdf file."
        )

    try:

        await process_and_store_document(file)
        return {
            "filename": file.filename,
            "message": "File processed and stored successfully."
        }
    except Exception as e:

        print(f"Error processing file: {e}")
        raise HTTPException(
            status_code=500, detail=f"An error occurred while processing the file: {e}")


@app.post("/chat", response_model=ChatResponse, tags=["Chat"])
def chat_with_agent(request: ChatRequest):
    try:

        langchain_messages: List[BaseMessage] = []
        for msg in request.messages:
            if msg.role == "user":
                langchain_messages.append(HumanMessage(content=msg.content))
            elif msg.role == "assistant":
                langchain_messages.append(AIMessage(content=msg.content))

        inputs = {"messages": langchain_messages}

        final_state = agent_app.invoke(inputs)

        final_message = final_state['messages'][-1]

        return {"answer": final_message.content}

    except Exception as e:
        print(f"Error processing file: {e}")
        raise HTTPException(
            status_code=500, detail=f"An error occurred while processing the file: {e}")


async def stream_agent_response(messages: List[BaseMessage]) -> AsyncGenerator[str, None]:

    async for event in agent_app.astream_events(
        {"messages": messages},
        version="v1",
    ):
        kind = event["event"]

        if kind == "on_chat_model_stream":

            content = event["data"]["chunk"].content
            if content:

                yield content


@app.post("/chat/stream")
async def chat_stream_with_agent(request: ChatRequest):

    langchain_messages: List[BaseMessage] = [
        HumanMessage(content=msg.content) if msg.role == "user"
        else AIMessage(content=msg.content)
        for msg in request.messages
    ]

    return StreamingResponse(
        stream_agent_response(langchain_messages),
        media_type="text/plain"
    )

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
