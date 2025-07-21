import os
import tempfile
from fastapi import UploadFile

from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_community.vectorstores import Chroma
from langchain_openai import AzureOpenAIEmbeddings
from langchain.storage import LocalFileStore
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.retrievers import ParentDocumentRetriever
from langchain.storage._lc_store import create_kv_docstore
from dotenv import load_dotenv

load_dotenv()

PERSIST_DIRECTORY = "./chroma_db"
DOC_STORE_DIRECTORY = "./doc_store"
COLLECTION_NAME = "split_docs"

parent_splitter = RecursiveCharacterTextSplitter(chunk_size=2000)
child_splitter = RecursiveCharacterTextSplitter(chunk_size=400)

embeddings = AzureOpenAIEmbeddings(
    model=os.getenv("AZURE_OPENAI_EMBEDDING_MODEL"),
)

vectorstore = Chroma(
    collection_name=COLLECTION_NAME,
    embedding_function=embeddings,
    persist_directory=PERSIST_DIRECTORY,
)

fs_store = LocalFileStore(root_path=DOC_STORE_DIRECTORY)
store = create_kv_docstore(fs_store)

retriever = ParentDocumentRetriever(
    vectorstore=vectorstore,
    docstore=store,
    child_splitter=child_splitter,
    parent_splitter=parent_splitter,
)


async def process_and_store_document(file: UploadFile):
    file_extension = os.path.splitext(file.filename)[1].lower()

    with tempfile.NamedTemporaryFile(delete=False, suffix=file_extension) as tmp:
        contents = await file.read()
        tmp.write(contents)
        tmp_path = tmp.name

    docs = []

    try:
        if file_extension == ".pdf":

            loader = PyPDFLoader(tmp_path)
            docs = loader.load()
        elif file_extension == ".txt":

            print(tmp_path)

            loader = TextLoader(tmp_path)

            docs = loader.load()
        else:

            return

        retriever.add_documents(docs, ids=None)
        print(f"Successfully processed and stored document: {file.filename}")

    finally:
        os.remove(tmp_path)
