from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.infrastructure.di import get_chat_use_case

router = APIRouter()


class ChatRequest(BaseModel):
    question: str


@router.post("/chat")
async def chat_with_docs(request: ChatRequest) -> dict:
    use_case = get_chat_use_case()

    try:
        result = use_case.execute(request.question)
        return {"answer": result.answer, "used_content": result.used_chunks}

    except Exception as error:
        raise HTTPException(status_code=500, detail=str(error))
