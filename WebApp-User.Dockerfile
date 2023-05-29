FROM python:3.9.10-slim-buster
RUN apt-get update && apt-get install python-tk python3-tk tk-dev -y
COPY ./code/requirements.txt /usr/local/src/myscripts/requirements.txt
WORKDIR /usr/local/src/myscripts
RUN pip install -r requirements.txt
COPY ./code/ /usr/local/src/myscripts
# 删除自测页面（WebApp.Dockerfile.dockerignore不好使，所以用了这种方法）
RUN rm -rf pages/01_Add_Document.py \
    pages/04_Index_Management.py \
    pages/10_Sandbox.py\
    pages/10_Utils\ -\ Document_Summary.py\
    pages/11_Utils\ -\ Conversation_Data_Extraction.py\
    pages/12_Utils\ -\ Prompt\ Exploration.py\
    pages/100_Chat_Debug.py\
    pages/103_Document_Viewer_Debug.py\
    pages/199_Streamlit_Test.py\
    OpenAI_Queries.py
RUN mv pages/00_Chat.py 00_Chat.py
EXPOSE 80
CMD ["streamlit", "run", "00_Chat.py", "--server.port", "80", "--server.enableXsrfProtection", "false"]