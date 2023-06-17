FROM python:3.10

WORKDIR /app

COPY requirements.txt .

COPY ./.env .



COPY  . .
RUN apt-get update\
	#&& apt-get install -y netcat\
	&& apt-get install -y make\
	&& pip install --upgrade pip\
	&& pip install --no-cache-dir -r requirements.txt
#RUN alembic upgrage head
#CMD ["gunicorn", "api_yamdb.wsgi:application", "--bind", "0:8000"]
#CMD [ "uvicorn", "main:app"]
#, "--host", "127.0.0.1", "--port", "8000" ]