from fastapi import FastAPI, File, UploadFile, HTTPException
import PyPDF2
import os
import chromadb
from openai import OpenAI
import docx
import io
from pydantic import BaseModel
import uuid
from dotenv import load_dotenv
from chromadb.utils import embedding_functions


load_dotenv()

app = FastAPI(title="RAG Backend")

openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

chroma_client = chromadb.PersistentClient(path="/app/chroma_db")

openai_ef = embedding_functions.OpenAIEmbeddingFunction(
    api_key=os.getenv("OPENAI_API_KEY"),
    model_name="text-embedding-3-small"
)

collection = chroma_client.get_or_create_collection(
    "rag_documents",
    embedding_function=openai_ef
)

class ChatRequests(BaseModel):
    question: str

def extract_text(file_bytes:bytes, filename:str) -> str:
    text = ""

    if filename.endswith(".txt"):
        text = file_bytes.decode("utf-8")

    elif filename.endswith(".pdf"):
        pdf_reader = PyPDF2.PdfReader(io.BytesIO(file_bytes))
        for page in pdf_reader.pages:
            text += page.extract_text() + "\n"

    elif filename.endswith(".docx"):
        doc = docx.Document(io.BytesIO(file_bytes))
        for paragraph in doc.paragraphs:
            text += paragraph.text + "\n"

    else:
        raise ValueError("Формат файла не поддерживается. Пожалуйста, загрузите .txt, .pdf или .docx файл.")

    return text.strip()

def split_text_into_chunks(text:str, chunk_size:int = 500, overlap: int = 50) -> list:
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size

        chunks.append(text[start:end])

        start += chunk_size - overlap
    return chunks


@app.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    try:
        file_bytes = await file.read()

        extracted_text = extract_text(file_bytes, file.filename)

        if not extracted_text:
            raise HTTPException(status_code=400, detail="Не удалось извлечь текст из файла.")

        chunks = split_text_into_chunks(extracted_text)

        chunks_id = [str(uuid.uuid4()) for _ in chunks]

        collection.add(documents=chunks, ids=chunks_id,
                       metadatas=[{"source": file.filename} for _ in chunks])

        return {
            "message": f"Файл {file.filename} успешно обработан." ,
            "text_preview": extracted_text[:200] + "..."
        }

    except UnicodeDecodeError:
        print("Пожалуйста, используйте .txt файл с кодировкой utf-8")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Произошла ошибка - {str(e)}")

@app.post("/chat")
async def chat_with_docs(request: ChatRequests):
    try:
        user_question = request.question

        results = collection.query(
            query_texts=[user_question],n_results=3
        )

        retrieved_chunks = results["documents"][0] if results["documents"] else []

        if not retrieved_chunks:
            return {"answer":"База знаний пуста. Пожалуйста, загрузите документы."}

        context = "\n---\n".join(retrieved_chunks)

        system_prompt = (
            "Ты - полезный ИИ помощник. Отвечай на вопрос пользователя строго на основе представленного контекста из документов. Если в документах нет ответа, то честно так и скажи.\n\n"
            f"Контекст из документов: \n{context}"
        )

        response = openai_client.chat.completions.create(
            model="gpt-4o-mini",
            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_question}
            ]
        )

        answer = response.choices[0].message.content

        return {
            "answer": answer,
            "used_content": retrieved_chunks
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))