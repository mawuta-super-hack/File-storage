FROM python:3.10

WORKDIR /app

COPY requirements.txt .

COPY ./.env .

COPY  . .

RUN apt-get update\
	&& apt-get install -y make\
    && apt-get install -y netcat-traditional\
	&& pip install --upgrade pip\
	&& pip install --no-cache-dir -r requirements.txt
