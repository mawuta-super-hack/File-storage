start:
	while ! nc -z ${POSTGRES_HOST} ${DOCKER_DB_PORT}; do sleep 0.1; done
	alembic upgrade head
	python -m gunicorn --name file_service -k uvicorn.workers.UvicornWorker -w 2 -b 0.0.0.0:8000 main:app
