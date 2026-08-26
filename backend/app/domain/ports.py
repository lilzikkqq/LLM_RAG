from abc import ABC, abstractmethod

from backend.app.domain.entities import DocumentChunk


class DocumentRepository(ABC):
    @abstractmethod
    def add_chunks(self, chunks: list[DocumentChunk]) -> None:
        ...

    @abstractmethod
    def search(self, query: str, n_results: int = 3) -> list[str]:
        ...


class ChatGateway(ABC):
    @abstractmethod
    def ask(self, question: str, context: str) -> str:
        ...


class TextExtractor(ABC):
    @abstractmethod
    def extract(self, file_bytes: bytes, filename: str) -> str:
        ...
