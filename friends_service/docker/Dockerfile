FROM python:3.8-slim-buster as builder
ADD https://github.com/ufoscout/docker-compose-wait/releases/download/2.7.3/wait /usr/local/bin/wait
RUN chmod +x /usr/local/bin/wait
RUN pip install --upgrade pip
COPY requirements.txt /tmp
RUN pip install -r /tmp/requirements.txt

FROM python:3.8-slim-buster as runner
COPY --from=builder /usr/local /usr/local
COPY src/ /friends_service/src
COPY alembic/ /friends_service/alembic
COPY alembic.ini /friends_service/alembic.ini

WORKDIR /friends_service
ARG UVICORN_WORKERS
ARG APPLICATION_PORT

CMD /usr/local/bin/wait && alembic upgrade head && gunicorn src.main:app -b 0.0.0.0:${APPLICATION_PORT} -w ${UVICORN_WORKERS} -k uvicorn.workers.UvicornWorker
