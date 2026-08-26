from openai import OpenAI

from backend.app.domain.ports import ChatGateway

SYSTEM_PROMPT_TEMPLATE = (
    "Ты - полезный ИИ помощник. Отвечай на вопрос пользователя строго на основе "
    "представленного контекста из документов. Если в документах нет ответа, "
    "то честно так и скажи.\n\n"
    "Контекст из документов: \n{context}"
)


class OpenAIChatGateway(ChatGateway):
    def __init__(self, api_key: str, model: str = "gpt-4o-mini") -> None:
        self._client = OpenAI(api_key=api_key)
        self._model = model

    def ask(self, question: str, context: str) -> str:
        response = self._client.chat.completions.create(
            model=self._model,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT_TEMPLATE.format(context=context)},
                {"role": "user", "content": question},
            ],
        )
        return response.choices[0].message.content
