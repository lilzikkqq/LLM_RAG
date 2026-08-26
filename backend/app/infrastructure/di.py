from functools import lru_cache

from backend.app.adapters.extractors.text_extractor import FileTextExtractor
from backend.app.adapters.gateways.openai_gateway import OpenAIChatGateway
from backend.app.adapters.repositories.chroma_repository import ChromaDocumentRepository
from backend.app.infrastructure.config import CHROMA_PERSIST_PATH, OPENAI_API_KEY
from backend.app.use_cases.chat_with_docs import ChatWithDocsUseCase
from backend.app.use_cases.upload_doc import UploadDocumentUseCase


@lru_cache
def get_repository() -> ChromaDocumentRepository:
    return ChromaDocumentRepository(
        persist_path=CHROMA_PERSIST_PATH,
        openai_api_key=OPENAI_API_KEY,
    )


@lru_cache
def get_chat_gateway() -> OpenAIChatGateway:
    return OpenAIChatGateway(api_key=OPENAI_API_KEY)


@lru_cache
def get_extractor() -> FileTextExtractor:
    return FileTextExtractor()


def get_upload_use_case() -> UploadDocumentUseCase:
    return UploadDocumentUseCase(repository=get_repository(), extractor=get_extractor())


def get_chat_use_case() -> ChatWithDocsUseCase:
    return ChatWithDocsUseCase(repository=get_repository(), chat_gateway=get_chat_gateway())
