FROM python:3.10.12-bookworm

WORKDIR /login_api
COPY requirements.txt requirements.txt
RUN apt-get update
RUN apt-get install mysql-common -y
RUN pip install --upgrade setuptools
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
COPY . /login_api/

EXPOSE 8002

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8002"]