from backend.app.domain.entities import ChatAnswer
from backend.app.domain.ports import ChatGateway, DocumentRepository


class ChatWithDocsUseCase:
    def __init__(self, repository: DocumentRepository, chat_gateway: ChatGateway) -> None:
        self._repository = repository
        self._chat_gateway = chat_gateway

    def execute(self, question: str) -> ChatAnswer:
        retrieved_chunks = self._repository.search(question, n_results=3)

        if not retrieved_chunks:
            return ChatAnswer(
                answer="База знаний пуста. Пожалуйста, загрузите документы.",
                used_chunks=[],
            )

        context = "\n---\n".join(retrieved_chunks)
        answer = self._chat_gateway.ask(question, context)

        return ChatAnswer(answer=answer, used_chunks=retrieved_chunks)
