from fastapi import APIRouter, File, HTTPException, UploadFile

from backend.app.infrastructure.di import get_upload_use_case

router = APIRouter()


@router.post("/upload")
async def upload_document(file: UploadFile = File(...)) -> dict:
    use_case = get_upload_use_case()

    try:
        file_bytes = await file.read()
        preview = use_case.execute(file_bytes, file.filename)

        return {
            "message": f"Файл {file.filename} успешно обработан.",
            "text_preview": preview + "...",
        }

    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error))
    except Exception as error:
        raise HTTPException(status_code=500, detail=f"Произошла ошибка - {error}")
