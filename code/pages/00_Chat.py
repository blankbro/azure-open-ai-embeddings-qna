import os

import streamlit as st
from streamlit_chat import message

from utilities.helper import LLMHelper


def clear_chat_data():
    st.session_state['input'] = ""
    st.session_state['chat_history'] = []
    st.session_state['source_documents'] = []


def send_msg():
    if st.session_state['input']:
        question, result, _, sources, _ = llm_helper.get_semantic_answer_lang_chain(st.session_state['input'], st.session_state['chat_history'])
        st.session_state['chat_history'].append((question, result))
        st.session_state['source_documents'].append(sources)
        st.session_state['input'] = ""


st.set_page_config(layout="wide", page_title=os.getenv("page_title", "问答助手"), page_icon=os.path.join('images', 'openai.png'))

hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# Initialize chat history
if 'question' not in st.session_state:
    st.session_state['question'] = None
if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []
if 'source_documents' not in st.session_state:
    st.session_state['source_documents'] = []

llm_helper = LLMHelper(temperature=0.2)

col1, col2 = st.columns([9, 1])
with col1:
    st.text_input("You: ", placeholder="type your question", key="input")
with col2:
    st.text("")
    st.text("")
    st.button("Send", on_click=send_msg)

col1, col2 = st.columns([1, 1])
with col1:
    clear_chat = st.button("Clear chat", key="clear_chat", on_click=clear_chat_data)

if st.session_state['chat_history']:
    for i in range(len(st.session_state['chat_history']) - 1, -1, -1):
        message(st.session_state['chat_history'][i][1], key=str(i))
        if st.session_state["source_documents"][i]:
            st.markdown(f'\n\nSources: {st.session_state["source_documents"][i]}')
        message(st.session_state['chat_history'][i][0], is_user=True, key=str(i) + '_user')
