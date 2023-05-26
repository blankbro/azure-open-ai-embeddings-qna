import streamlit as st
from streamlit_chat import message
from utilities.helper import LLMHelper
import os
from utilities.customprompt import condense_question_prompt_template
from utilities.customprompt import completion_prompt_template
from langchain.chains.llm import LLMChain

import langchain.chains.conversational_retrieval.base as conversational_retrieval


def clear_chat_data():
    st.session_state['input'] = ""
    st.session_state['chat_history'] = []
    st.session_state['source_documents'] = []


def send_msg():
    if st.session_state['input']:
        last_chats = get_last_chats()
        question, result, context, sources = llm_helper.get_semantic_answer_lang_chain(st.session_state['input'], last_chats)
        st.session_state['chat_history'].append((question, result))
        st.session_state['source_documents'].append(sources)
        st.session_state['contexts'].append(context)
        st.session_state['input'] = ""


def get_last_chats(count: int = 10):
    if len(st.session_state['chat_history']) < count:
        return st.session_state['chat_history']
    else:
        return st.session_state['chat_history'][-count:]


@st.cache_data()
def get_languages():
    return llm_helper.translator.get_available_languages()


def check_variables_in_condense_question_prompt():
    # Check if "chat_history" is present in the string condense_question_prompt
    if "{chat_history}" not in st.session_state.condense_question_prompt:
        st.warning("""Your condense question prompt doesn't contain the variable "{chat_history}".   
        Please add it to your condense question prompt to use the app.  
        Reverting to default prompt.
        """)
        st.session_state.completion_prompt = ""
    if "{question}" not in st.session_state.completion_prompt:
        st.warning("""Your condense question prompt doesn't contain the variable "{question}".  
        This variable is used to add the user's question to the prompt.  
        Please add it to your condense question prompt to use the app.  
        Reverting to default prompt.  
        """)
        st.session_state.completion_prompt = ""


def check_variables_in_completion_prompt():
    # Check if "summaries" is present in the string completion_prompt
    if "{summaries}" not in st.session_state.completion_prompt:
        st.warning("""Your completion prompt doesn't contain the variable "{summaries}".  
        This variable is used to add the content of the documents retrieved from the VectorStore to the prompt.  
        Please add it to your completion prompt to use the app.  
        Reverting to default prompt.
        """)
        st.session_state.completion_prompt = ""
    if "{question}" not in st.session_state.completion_prompt:
        st.warning("""Your completion prompt doesn't contain the variable "{question}".  
        This variable is used to add the user's question to the prompt.  
        Please add it to your completion prompt to use the app.  
        Reverting to default prompt.  
        """)
        st.session_state.completion_prompt = ""


st.set_page_config(layout="wide")

# Initialize chat history
if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []
if 'source_documents' not in st.session_state:
    st.session_state['source_documents'] = []
if 'new_questions' not in st.session_state:
    st.session_state['new_questions'] = []
if 'contexts' not in st.session_state:
    st.session_state['contexts'] = []

if 'condense_question_prompt' not in st.session_state:
    st.session_state['condense_question_prompt'] = os.getenv("CONDENSE_QUESTION_PROMPT", "")
if 'completion_prompt' not in st.session_state:
    st.session_state['completion_prompt'] = os.getenv("COMPLETION_PROMPT", "")
if 'temperature' not in st.session_state:
    st.session_state['temperature'] = float(os.getenv("OPENAI_TEMPERATURE", 0.7))
if 'max_response' not in st.session_state:
    st.session_state['max_response'] = int(os.getenv("OPENAI_MAX_TOKENS", -1))
if 'top_p' not in st.session_state:
    st.session_state['top_p'] = float(os.getenv("OPENAI_TOP_P", 1))
if 'frequency_penalty' not in st.session_state:
    st.session_state['frequency_penalty'] = float(os.getenv("OPENAI_FREQUENCY_PENALTY", 0))
if 'presence_penalty' not in st.session_state:
    st.session_state['presence_penalty'] = float(os.getenv("OPENAI_PRESENCE_PENALTY", 0))

if 'top_k' not in st.session_state:
    st.session_state['top_k'] = int(os.getenv("REDISEARCH_TOP_K", 4))
if 'score_threshold' not in st.session_state:
    st.session_state['score_threshold'] = float(os.getenv("REDISEARCH_SCORE_THRESHOLD", 0.2))
if 'search_type' not in st.session_state:
    st.session_state['search_type'] = os.getenv("REDISEARCH_SEARCH_TYPE", "similarity")

llm_helper = LLMHelper(condense_question_prompt=st.session_state.condense_question_prompt,
                       completion_prompt=st.session_state.completion_prompt,
                       temperature=st.session_state.temperature,
                       max_tokens=st.session_state.max_response,
                       top_p=st.session_state.top_p,
                       frequency_penalty=st.session_state.frequency_penalty,
                       presence_penalty=st.session_state.presence_penalty,
                       k=st.session_state.top_k,
                       score_threshold=st.session_state.score_threshold,
                       search_type=st.session_state.search_type)
# Get available languages for translation
available_languages = get_languages()

col1, col2 = st.columns([3, 1])
with col1:
    col1_col1, col1_col2 = st.columns([7, 1])
    with col1_col1:
        st.text_input("You: ", placeholder="type your question", key="input")
        clear_chat = st.button("Clear chat", key="clear_chat", on_click=clear_chat_data)
    with col1_col2:
        st.text("")
        st.text("")
        st.button("Send", on_click=send_msg)

    if st.session_state['chat_history']:
        for i in range(len(st.session_state['chat_history']) - 1, -1, -1):
            with st.expander("Debug", expanded=False):
                if st.session_state["source_documents"][i]:
                    st.markdown(f'\n\nSources: {st.session_state["source_documents"][i]}')
                if st.session_state["contexts"][i]:
                    st.markdown(f'\n\nContext: {st.session_state["contexts"][i]}')
            message(st.session_state['chat_history'][i][1], key=str(i))
            message(st.session_state['chat_history'][i][0], is_user=True, key=str(i) + '_user')
with col2:
    st.text("")
    st.text("")
    with st.expander("Settings", expanded=True):
        # model = st.selectbox(
        #     "OpenAI GPT-3 Model",
        #     [os.environ['OPENAI_ENGINE']]
        # )
        # st.tokens_response = st.slider("Tokens response length", 100, 500, 400)
        st.slider("Temperature", key='temperature', min_value=0.0, max_value=1.0, step=0.1)
        st.slider("Max response", key='max_response', min_value=-1, max_value=4000, step=1, help="最大响应数。-1表示无限制")
        st.slider("Top p", key='top_p', min_value=0.0, max_value=1.0, step=0.1, help="与温度类似，这控制随机性但使用不同的方法。降低 Top P 将缩小模型的令牌选择范围，使其更有可能选择令牌。增加 Top P 将让模型从高概率和低概率的令牌中进行选择。尝试调整温度或 Top P，但不要同时调整两者。")
        st.slider("Frequency penalty", key='frequency_penalty', min_value=0.0, max_value=2.0, step=0.1, help="根据单词在文本中出现的频率，按比例减少单词重复出现的机会。这降低了在响应中重复完全相同的文本的可能性。")
        st.slider("Presence penalty", key='presence_penalty', min_value=0.0, max_value=2.0, step=0.1, help="减少重复出现在文本中的单词的机会。这增加了在回应中引入新话题的可能性。")
        st.text_area("Condense question prompt", key='condense_question_prompt', height=150,
                     on_change=check_variables_in_condense_question_prompt,
                     placeholder=condense_question_prompt_template,
                     help="You can configure a condense question prompt by adding the variables {chat_history} and {question} to the prompt.")
        st.text_area("Completion prompt", key='completion_prompt', height=150,
                     on_change=check_variables_in_completion_prompt,
                     placeholder=completion_prompt_template,
                     help="""You can configure a completion prompt by adding the variables {summaries} and {question} to the prompt.  
                            {summaries} will be replaced with the content of the documents retrieved from the VectorStore.  
                            {question} will be replaced with the user's question.""")
        st.number_input("Top k", key='top_k', min_value=1, step=1, help="限制Redis搜索到的最大Chunk数")
        st.slider("Score threshold", key='score_threshold', min_value=0.1, step=0.1, max_value=1.0, help="向量相似度（越接近0，也就越相似）")
        st.selectbox("Search type", key='search_type', options=("similarity", "similarity_limit"), help="similarity_limit会根据相似度的要求进行过滤")
        st.selectbox("Language", [None] + list(available_languages.keys()), key='translation_language')
