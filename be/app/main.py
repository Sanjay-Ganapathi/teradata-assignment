import os
from pydantic import BaseModel
import uvicorn
from fastapi import FastAPI, File, HTTPException, UploadFile
from dotenv import load_dotenv

from app.vector_store import process_and_store_document

load_dotenv()

# TODO change title and description
app = FastAPI(
    title="Intelligent Agent Chatbot API",
    description="An API for a RAG-based chatbot using LangGraph and FastAPI.",

)


class UploadResponse(BaseModel):
    filename: str
    message: str


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


if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
