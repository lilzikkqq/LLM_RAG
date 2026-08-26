import chromadb
from chromadb.utils import embedding_functions

from backend.app.domain.entities import DocumentChunk
from backend.app.domain.ports import DocumentRepository


class ChromaDocumentRepository(DocumentRepository):
    def __init__(
        self,
        persist_path: str,
        openai_api_key: str,
        collection_name: str = "rag_documents",
    ) -> None:
        client = chromadb.PersistentClient(path=persist_path)

        embedding_function = embedding_functions.OpenAIEmbeddingFunction(
            api_key=openai_api_key,
            model_name="text-embedding-3-small",
        )

        self._collection = client.get_or_create_collection(
            collection_name,
            embedding_function=embedding_function,
        )

    def add_chunks(self, chunks: list[DocumentChunk]) -> None:
        self._collection.add(
            documents=[chunk.text for chunk in chunks],
            ids=[chunk.id for chunk in chunks],
            metadatas=[{"source": chunk.source} for chunk in chunks],
        )

    def search(self, query: str, n_results: int = 3) -> list[str]:
        results = self._collection.query(query_texts=[query], n_results=n_results)
        documents = results.get("documents")
        return documents[0] if documents else []
