import requests

BACKEND_URL = "http://backend:8000"


class BackendError(Exception):
    pass


def upload_document(filename: str, file_bytes: bytes) -> dict:
    files = {"file": (filename, file_bytes)}

    try:
        response = requests.post(f"{BACKEND_URL}/upload", files=files)
    except requests.exceptions.RequestException as error:
        raise BackendError(f"Не удалось связаться с сервером: {error}") from error

    if response.status_code != 200:
        detail = response.json().get("detail", "Неизвестная ошибка сервера.")
        raise BackendError(detail)

    return response.json()


def ask_question(question: str) -> dict:
    try:
        response = requests.post(f"{BACKEND_URL}/chat", json={"question": question})
    except requests.exceptions.RequestException as error:
        raise BackendError(f"Потеряна связь с сервером: {error}") from error

    if response.status_code != 200:
        detail = response.json().get("detail", "Неизвестная ошибка сервера.")
        raise BackendError(detail)

    return response.json()
