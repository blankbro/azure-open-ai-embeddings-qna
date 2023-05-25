import streamlit as st
from langchain.schema import Document
import utilities.myutil as myutil
import urllib

# 测试 myutil.document_to_markdown_link()
doc = Document(page_content="")
doc.metadata["source"] = "[https://nbotstr.blob.core.windows.net/documents/SN_B 75-2021.05技术文件审核流程标准.pdf](https://nbotstr.blob.core.windows.net/documents/SN_B 75-2021.05技术文件审核流程标准.pdf_SAS_TOKEN_PLACEHOLDER_)"
doc.metadata["filename"] = "SN_B 75-2021.05技术文件审核流程标准.pdf"
st.markdown(f'\n\nSources: {myutil.document_to_markdown_link(doc)}')

# 测试 urllib.parse.unquote()
url = "https://nbotstr.blob.core.windows.net/documents/%E4%BC%81%E4%B8%9A%E5%BE%AE%E4%BF%A1-%E5%BE%AE%E6%96%87%E6%A1%A3%E6%93%8D%E4%BD%9C%E6%96%87%E6%A1%A3.pdf"
st.write(urllib.parse.unquote(url))
