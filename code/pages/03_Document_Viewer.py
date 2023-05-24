import requests
import streamlit as st
import os
import traceback
from utilities.helper import LLMHelper
import datetime


def now_date_time():
    return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')


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

    files_data = llm_helper.blob_client.get_all_files()

    # 待探索，新增多选框
    st.dataframe(files_data, use_container_width=True)

    if st.button("补充缺失的 converted 文件"):
        for i in range(len(files_data)):
            file_data = files_data[i]
            filename = file_data["filename"]
            fullpath = file_data["fullpath"]
            if file_data.get("converted") is False and not filename.endswith('.txt'):
                st.write(f"{now_date_time()}【{i}】{filename} 开始了")
                llm_helper.convert_file(bytes_data=requests.get(fullpath).content, filename=filename, enable_translation=False)
                # llm_helper.convert_file(source_url=fullpath, filename=filename, enable_translation=False)
                st.write(f"{now_date_time()}【{i}】{filename} 完成了")
    if st.button("补充缺失的 embeddings 向量"):
        for i in range(len(files_data)):
            file_data = files_data[i]
            filename = file_data["filename"]
            converted_file_url = file_data["converted_path"]
            if file_data.get("converted") is True and file_data.get("embeddings_added") is False:
                st.write(f"{now_date_time()}【{i}】{filename} 开始了")
                llm_helper.add_embeddings_lc(converted_file_url)
                llm_helper.blob_client.upsert_blob_metadata(filename, {'embeddings_added': 'true'})
                st.write(f"{now_date_time()}【{i}】{filename} 完成了")
    if st.button("将所有文档 embeddings_added 状态置为 false"):
        for i in range(len(files_data)):
            file_data = files_data[i]
            filename = file_data["filename"]
            st.write(f"{now_date_time()}【{i}】{filename} 开始了")
            llm_helper.blob_client.upsert_blob_metadata(filename, {'embeddings_added': 'false'})
            st.write(f"{now_date_time()}【{i}】{filename} 完成了")
except Exception as e:
    traceback.print_exc()
    st.error(traceback.format_exc())
