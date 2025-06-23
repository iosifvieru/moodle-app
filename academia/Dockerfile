FROM python:3.10.12-bookworm
ENV APP_PORT=8000

WORKDIR /academia
COPY requirements.txt requirements.txt
RUN apt-get update
RUN apt-get install mysql-common -y
RUN pip install --upgrade setuptools
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
COPY . /academia/

EXPOSE ${APP_PORT}

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]