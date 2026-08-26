import streamlit as st

from api_client import BackendError, ask_question, upload_document

st.set_page_config(page_title="LLM ассистент с RAG", page_icon="👾")
st.title("Чат с документами📚")

if "message" not in st.session_state:
    st.session_state["message"] = []

with st.sidebar:
    st.header("Загрузка документов📑")
    uploaded_file = st.file_uploader("Выберите файл", type=["pdf", "txt", "docx"])

    if st.button("Загрузить базу") and uploaded_file is not None:
        with st.spinner("Идёт обработка📝..."):
            try:
                upload_document(uploaded_file.name, uploaded_file.getvalue())
                st.success("Документ успешно добавлен в базу✅")
            except BackendError as error:
                st.error(str(error))

for message in st.session_state.message:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if user_question := st.chat_input("Напишите ваш вопрос по документу..."):
    st.session_state.message.append({"role": "user", "content": user_question})

    with st.chat_message("user"):
        st.markdown(user_question)

    with st.chat_message("assistant"):
        with st.spinner("Ищу информацию в документе🔎..."):
            try:
                result = ask_question(user_question)
                answer = result.get("answer", "Нет ответа")
                st.markdown(answer)
                st.session_state.message.append({"role": "assistant", "content": answer})
            except BackendError as error:
                st.error(str(error))
