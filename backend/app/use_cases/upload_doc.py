import uuid

from backend.app.domain.entities import DocumentChunk
from backend.app.domain.ports import DocumentRepository, TextExtractor


class UploadDocumentUseCase:
    def __init__(
        self,
        repository: DocumentRepository,
        extractor: TextExtractor,
        chunk_size: int = 500,
        overlap: int = 50,
    ) -> None:
        self._repository = repository
        self._extractor = extractor
        self._chunk_size = chunk_size
        self._overlap = overlap

    def execute(self, file_bytes: bytes, filename: str) -> str:
        text = self._extractor.extract(file_bytes, filename)

        if not text:
            raise ValueError("Не удалось извлечь текст из файла.")

        chunks = [
            DocumentChunk(id=str(uuid.uuid4()), text=chunk_text, source=filename)
            for chunk_text in self._split_into_chunks(text)
        ]

        self._repository.add_chunks(chunks)

        return text[:200]

    def _split_into_chunks(self, text: str) -> list[str]:
        chunks: list[str] = []
        start = 0

        while start < len(text):
            end = start + self._chunk_size
            chunks.append(text[start:end])
            start += self._chunk_size - self._overlap

        return chunks
