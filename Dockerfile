FROM python:3.7-stretch

WORKDIR /app

ADD . /app
RUN pip install --upgrade pip

RUN pip install -r requirements.txt
RUN python -m nltk.downloader punkt -d /usr/local/nltk_data
RUN python -m nltk.downloader stopwords -d /usr/local/nltk_data
RUN python -m nltk.downloader wordnet -d /usr/local/nltk_data


CMD ["python", "app.py"]


