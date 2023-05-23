import streamlit as st
import os
import traceback
from utilities.helper import LLMHelper

try:
    # Set page layout to wide screen and menu item
    menu_items = {
        'Get help': None,
        'Report a bug': None,
        'About': '''
            ## Embeddings App

            Document Reader Sample Demo.
        '''
    }
    st.set_page_config(layout="wide", menu_items=menu_items)

    hide_streamlit_style = """
                <style>
                #MainMenu {visibility: hidden;}
                footer {visibility: hidden;}
                </style>
                """
    st.markdown(hide_streamlit_style, unsafe_allow_html=True)

    llm_helper = LLMHelper()

    col1, col2, col3 = st.columns([2, 1, 1])

    files_data = llm_helper.blob_client.get_all_files()

    st.dataframe(files_data, use_container_width=True)


    with st.expander("补漏（convert file and add embeddings）"):
        st.checkbox("Translate document to English", key="translate")
        if st.button("开始"):
            for file_data in files_data:
                filename = file_data["filename"]
                fullpath = file_data["fullpath"]
                if not file_data.get("converted") and not filename.endswith('.txt'):
                    st.write(filename + " 开始提取文件中的文本")
                    llm_helper.convert_file(source_url=fullpath, filename=filename, enable_translation=st.session_state['translate'])
                    st.write(filename + " 完成提取文件中的文本")
                if not file_data.get("embeddings_added"):
                    st.write(filename + " 开始添加文本对应的向量")
                    llm_helper.add_embeddings_lc(fullpath)
                    st.write(filename + " 完成添加文本对应的向量")
except Exception as e:
    st.error(traceback.format_exc())
