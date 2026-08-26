import io

import docx
import PyPDF2

from backend.app.domain.ports import TextExtractor


class FileTextExtractor(TextExtractor):
    def extract(self, file_bytes: bytes, filename: str) -> str:
        if filename.endswith(".txt"):
            return self._extract_txt(file_bytes)

        if filename.endswith(".pdf"):
            return self._extract_pdf(file_bytes)

        if filename.endswith(".docx"):
            return self._extract_docx(file_bytes)

        raise ValueError(
            "Формат файла не поддерживается. Пожалуйста, загрузите .txt, .pdf или .docx файл."
        )

    def _extract_txt(self, file_bytes: bytes) -> str:
        try:
            return file_bytes.decode("utf-8").strip()
        except UnicodeDecodeError as error:
            raise ValueError(
                "Не удалось прочитать .txt файл — используйте кодировку UTF-8."
            ) from error

    def _extract_pdf(self, file_bytes: bytes) -> str:
        pdf_reader = PyPDF2.PdfReader(io.BytesIO(file_bytes))
        text = "\n".join(page.extract_text() or "" for page in pdf_reader.pages)
        return text.strip()

    def _extract_docx(self, file_bytes: bytes) -> str:
        document = docx.Document(io.BytesIO(file_bytes))
        text = "\n".join(paragraph.text for paragraph in document.paragraphs)
        return text.strip()
