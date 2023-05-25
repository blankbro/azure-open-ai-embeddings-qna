FROM python:3.9.10-slim-buster
RUN apt-get update && apt-get install python-tk python3-tk tk-dev -y
COPY ./code/requirements.txt /usr/local/src/myscripts/requirements.txt
WORKDIR /usr/local/src/myscripts
RUN pip install -r requirements.txt
COPY ./code/pages/00_Chat.py /usr/local/src/myscripts/00_Chat.py
COPY ./code/pages/03_Document_Viewer.py /usr/local/src/myscripts/03_Document_Viewer.py
COPY ./code/ /usr/local/src/myscripts
EXPOSE 80
CMD ["streamlit", "run", "00_Chat.py", "--server.port", "80", "--server.enableXsrfProtection", "false"]