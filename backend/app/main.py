from fastapi import FastAPI

from backend.app.adapters.controllers import chat_controller, upload_controller

app = FastAPI(title="RAG Backend")

app.include_router(upload_controller.router)
app.include_router(chat_controller.router)
