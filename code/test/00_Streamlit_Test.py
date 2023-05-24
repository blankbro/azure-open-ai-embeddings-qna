import streamlit as st
from langchain.schema import Document
import utilities.myutil as myutil

doc = Document(page_content="")

doc.metadata["source"] = "[https://nbotstr.blob.core.windows.net/documents/SN_B 75-2021.05技术文件审核流程标准.pdf](https://nbotstr.blob.core.windows.net/documents/SN_B 75-2021.05技术文件审核流程标准.pdf_SAS_TOKEN_PLACEHOLDER_)"
doc.metadata["filename"] = "SN_B 75-2021.05技术文件审核流程标准.pdf"


st.markdown(f'\n\nSources: {myutil.document_to_markdown_link(doc)}')
