FROM python:3.9.10-slim-buster
RUN apt-get update && apt-get install python-tk python3-tk tk-dev -y
COPY ./code/requirements.txt /usr/local/src/myscripts/requirements.txt
WORKDIR /usr/local/src/myscripts
RUN pip install -r requirements.txt
COPY ./code/ /usr/local/src/myscripts
# 删除自测页面（WebApp.Dockerfile.dockerignore不好使，所以用了这种方法）
RUN rm -rf pages/100_Streamlit_Test.py
EXPOSE 80
CMD ["streamlit", "run", "OpenAI_Queries.py", "--server.port", "80", "--server.enableXsrfProtection", "false"]