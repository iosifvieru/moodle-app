FROM python:3.10.12-bookworm

WORKDIR /idm

ENV JWT_SECRET=e54f8eae766958431a1bf4b91cf9d6e6ce4c4cf8
ENV JWT_ALGORITHM=HS256
ENV JWT_EXPIRATION=30
ENV PASS_SECRET=151002e28asgedsa

COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

RUN apt-get update \
    && apt-get install -y default-mysql-client \
    && rm -rf /var/lib/apt/lists/*

COPY . .


EXPOSE 50051
CMD ["python3", "idm_server.py"]