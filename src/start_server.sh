#! bin/sh

sleep 3
start:
	
	alembic upgrade head

    python -m gunicorn --name backend -k uvicorn.workers.UvicornWorker -w 1-b 0.0.0.0:8000 main:app