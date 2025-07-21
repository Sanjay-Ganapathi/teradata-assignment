import uvicorn
from fastapi import FastAPI
from dotenv import load_dotenv

load_dotenv()

# TODO change title and description
app = FastAPI(
    title="Intelligent Agent Chatbot API",
    description="An API for a RAG-based chatbot using LangGraph and FastAPI.",

)


@app.get("/")
def read_root():

    return {"status": "ok", "message": "All services are working fine!"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
