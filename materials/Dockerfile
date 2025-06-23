FROM python:3.10.12-alpine
ENV APP_PORT=8001

WORKDIR /materials
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY . /materials/

EXPOSE ${APP_PORT}

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8001"]