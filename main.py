from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

import os
import shutil

import rag


# ==========================================
# FastAPI Application
# ==========================================

app = FastAPI(
    title="DocMind AI API"
)


# ==========================================
# CORS
# ==========================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5500",
        "http://localhost:5500",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ==========================================
# Request Model
# ==========================================

class QuestionRequest(BaseModel):
    question: str


# ==========================================
# Home
# ==========================================

@app.get("/")
def home():

    return {
        "message": "DocMind AI API is running"
    }


# ==========================================
# Upload PDF
# ==========================================

@app.post("/upload")
async def upload_pdf(
    file: UploadFile = File(...)
):

    # Check file extension

    if not file.filename.lower().endswith(".pdf"):

        raise HTTPException(
            status_code=400,
            detail="Only PDF files are allowed."
        )


    # Create upload folder

    upload_folder = "data/uploads"

    os.makedirs(
        upload_folder,
        exist_ok=True
    )


    # Create file path

    file_path = os.path.join(
        upload_folder,
        file.filename
    )


    # Save uploaded PDF

    try:

        with open(file_path, "wb") as buffer:

            shutil.copyfileobj(
                file.file,
                buffer
            )

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=f"Could not save PDF: {str(e)}"
        )


    # Create RAG from uploaded PDF

    try:

        pages, chunks = rag.create_rag_from_pdf(
            file_path
        )

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=f"Could not process PDF: {str(e)}"
        )


    # Response

    return {

        "message": "PDF uploaded and processed successfully.",

        "filename": file.filename,

        "pages": pages,

        "chunks": chunks
    }


# ==========================================
# Ask Question
# ==========================================

@app.post("/ask")
def ask_question(
    request: QuestionRequest
):

    question = request.question.strip()


    # Validate question

    if not question:

        return {

            "answer": "Please enter a question.",

            "sources": []
        }


    # Check Retriever

    if rag.retriever is None:

        return {

            "answer": "Please upload a PDF first.",

            "sources": []
        }


    # Retrieve relevant PDF chunks

    results = rag.retriever.invoke(
        question
    )


    # Build Context

    context = "\n\n".join(

        document.page_content

        for document in results

    )


    # Create Prompt

    messages = rag.prompt.invoke({

        "context": context,

        "question": question

    })


    # Ask Ollama

    response = rag.llm.invoke(
        messages
    )


    # Get Sources

    sources = []


    for document in results:

        source = document.metadata.get(
            "source",
            "Unknown source"
        )

        page = document.metadata.get(
            "page"
        )


        if page is not None:

            sources.append(

                f"{os.path.basename(source)} - page {page + 1}"

            )

        else:

            sources.append(

                os.path.basename(source)

            )


    # Return Answer

    return {

        "answer": response.content,

        "sources": list(
            dict.fromkeys(sources)
        )

    }