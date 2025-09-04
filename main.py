import streamlit as st

from models import Conversation, Message
from services import MessageSubmissionService

st.session_state.setdefault("conversation", Conversation())


def main_app():
    def _process_user_message():
        user_message = Message(role="user", content=st.session_state["chat_input"])
        with conversation.container():
            with st.chat_message(user_message.role):
                st.write(user_message.content)

            with st.spinner(text="Processando...", show_time=True):
                assistant_message = MessageSubmissionService(
                    st.session_state.conversation
                ).send_message(user_message)
                st.session_state.conversation.messages.append(user_message)
                st.session_state.conversation.messages.append(assistant_message)

    with st.sidebar:
        st.logo(
            "https://cdn.prod.website-files.com/66cf2bfc3ed15b02da0ca770/66d07240057721394308addd_Logo%20(1).svg",
            size="large",
        )
        st.divider()
        st.title("Interface Conversacional")
        st.write(
            """
            Esta é uma aplicação com o intuito de demonstrar o potencial da CrewAI para lidar com casos de uso
            conversacionais.

            No momento há suporte para agentes trabalharem de forma reativa a mensagens de um usuário, mas isto
            só mostra a arte do possível.

            **Futuramente, o objetivo será ter agentes que trabalham de forma proativa,
            buscando informações baseados em dados históricos, preferências e outras regras de negócio relevantes.**
            """
        )
        st.divider()
        st.link_button(
            "**Inscreva-se para uma avaliação gratuita**",
            "https://app.crewai.com/",
            type="primary",
        )

    with st.container():
        st.title("Conversa")
        conversation = st.container()

    with st._bottom:
        st.chat_input(
            key="chat_input",
            placeholder="Interaja com o agente aqui",
            on_submit=_process_user_message,
        )

    @st.fragment
    def _render_message(message: Message):
        with st.chat_message(message.role):
            st.write(message.content)

    for message in st.session_state.conversation.messages:
        with conversation.container():
            _render_message(message)


if __name__ == "__main__":
    main_app()
