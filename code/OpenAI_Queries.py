from dotenv import load_dotenv

load_dotenv()

import streamlit as st
import os
import traceback
from utilities.helper import LLMHelper
from utilities.customprompt import condense_question_prompt_template
from utilities.customprompt import completion_prompt_template

import logging

logger = logging.getLogger('azure.core.pipeline.policies.http_logging_policy').setLevel(logging.WARNING)


def check_deployment():
    # Check if the deployment is working
    # \ 1. Check if the llm is working
    try:
        llm_helper = LLMHelper()
        llm_helper.get_completion("Generate a joke!")
        st.success("LLM is working!")
    except Exception as e:
        st.error(f"""LLM is not working.  
            Please check you have a deployment name {llm_helper.deployment_name} in your Azure OpenAI resource {llm_helper.api_base}.  
            If you are using an Instructions based deployment (text-davinci-003), please check you have an environment variable OPENAI_DEPLOYMENT_TYPE=Text or delete the environment variable OPENAI_DEPLOYMENT_TYPE.  
            If you are using a Chat based deployment (gpt-35-turbo or gpt-4-32k or gpt-4), please check you have an environment variable OPENAI_DEPLOYMENT_TYPE=Chat.  
            Then restart your application.
            """)
        st.error(traceback.format_exc())
    # \ 2. Check if the embedding is working
    try:
        llm_helper = LLMHelper()
        llm_helper.embeddings.embed_documents(texts=["This is a test"])
        st.success("Embedding is working!")
    except Exception as e:
        st.error(f"""Embedding model is not working.  
            Please check you have a deployment named "text-embedding-ada-002" for "text-embedding-ada-002" model in your Azure OpenAI resource {llm_helper.api_base}.  
            Then restart your application.
            """)
        st.error(traceback.format_exc())
    # \ 3. Check if the translation is working
    try:
        llm_helper = LLMHelper()
        llm_helper.translator.translate("This is a test", "it")
        st.success("Translation is working!")
    except Exception as e:
        st.error(f"""Translation model is not working.  
            Please check your Azure Translator key in the App Settings.  
            Then restart your application.  
            """)
        st.error(traceback.format_exc())
    # \ 4. Check if the Redis is working with previous version of data
    try:
        llm_helper = LLMHelper()
        if llm_helper.vector_store_type != "AzureSearch":
            if llm_helper.vector_store.check_existing_index("embeddings-index"):
                st.warning("""Seems like you're using a Redis with an old data structure.  
                If you want to use the new data structure, you can start using the app and go to "Add Document" -> "Add documents in Batch" and click on "Convert all files and add embeddings" to reprocess your documents.  
                To remove this working, please delete the index "embeddings-index" from your Redis.  
                If you prefer to use the old data structure, please change your Web App container image to point to the docker image: fruocco/oai-embeddings:2023-03-27_25. 
                """)
            else:
                st.success("Redis is working!")
        else:
            try:
                llm_helper.vector_store.index_exists()
                st.success("Azure Cognitive Search is working!")
            except Exception as e:
                st.error("""Azure Cognitive Search is not working.  
                    Please check your Azure Cognitive Search service name and service key in the App Settings.  
                    Then restart your application.  
                    """)
                st.error(traceback.format_exc())
    except Exception as e:
        st.error(f"""Redis is not working. 
            Please check your Redis connection string in the App Settings.  
            Then restart your application.
            """)
        st.error(traceback.format_exc())


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


@st.cache_data()
def get_languages():
    return llm_helper.translator.get_available_languages()

try:

    if 'question' not in st.session_state:
        st.session_state['question'] = ""
    if 'response' not in st.session_state:
        st.session_state['response'] = ""
    if 'context' not in st.session_state:
        st.session_state['context'] = ""

    if 'condense_question_prompt' not in st.session_state:
        st.session_state['condense_question_prompt'] = os.getenv("CONDENSE_QUESTION_PROMPT", "")
    if 'completion_prompt' not in st.session_state:
        st.session_state['completion_prompt'] = os.getenv("COMPLETION_PROMPT", "")
    if 'temperature' not in st.session_state:
        st.session_state['temperature'] = float(os.getenv("OPENAI_TEMPERATURE", 0.7))
    if 'max_response' not in st.session_state:
        st.session_state['max_response'] = int(os.getenv("OPENAI_MAX_TOKENS", -1))
    if 'top_p' not in st.session_state:
        st.session_state['top_p'] = float(os.getenv("OPENAI_TOP_P", 0.95))
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

    # Set page layout to wide screen and menu item
    menu_items = {
        'Get help': None,
        'Report a bug': None,
        'About': '''
             ## Embeddings App
             Embedding testing application.
            '''
    }
    st.set_page_config(layout="wide", menu_items=menu_items)

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

    col1, col2, col3 = st.columns([1, 2, 1])
    with col1:
        st.image(os.path.join('images', 'microsoft.png'))

    col1, col2, col3 = st.columns([2, 2, 2])
    with col1:
        st.button("Check deployment", on_click=check_deployment)
    with col3:
        with st.expander("Settings"):
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
            st.number_input("Top k", key='top_k', min_value=1, step=1, help="用来限制从Redis搜索到的最大Chunk数")
            st.slider("Score threshold", key='score_threshold', min_value=0.1, step=0.1, max_value=1.0, help="向量相似性：数值越小相似性要求越高")
            st.selectbox("Search type", key='search_type', options=("similarity", "similarity_limit"), help="similarity_limit 模式下，匹配分数低于 Score threshold，不会返回")
            st.selectbox("Language", [None] + list(available_languages.keys()), key='translation_language')

    question = st.text_input("OpenAI Semantic Answer", "")

    if question != '':
        st.session_state['question'] = question
        st.session_state['question'], st.session_state['response'], st.session_state['context'], sources = llm_helper.get_semantic_answer_lang_chain(question, [])
        st.markdown("Answer:" + st.session_state['response'])
        st.markdown(f'\n\nSources: {sources}')
        with st.expander("Question and Answer Context"):
            st.markdown(st.session_state['context'].replace('$', '\$'))
            st.markdown(f"SOURCES: {sources}")

    if st.session_state['translation_language'] and st.session_state['translation_language'] != '':
        st.write(f"Translation to other languages, 翻译成其他语言, النص باللغة العربية")
        st.write(f"{llm_helper.translator.translate(st.session_state['response'], available_languages[st.session_state['translation_language']])}")

except Exception:
    traceback.print_exc()
    st.error(traceback.format_exc())
