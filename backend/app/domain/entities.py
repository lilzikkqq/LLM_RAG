from dataclasses import dataclass


@dataclass
class DocumentChunk:
    id: str
    text: str
    source: str


@dataclass
class ChatAnswer:
    answer: str
    used_chunks: list[str]
