FROM python:3.8-slim-buster as builder
RUN pip install --upgrade pip
COPY requirements.txt /tmp
RUN pip install -r /tmp/requirements.txt

FROM python:3.8-slim-buster as runner
COPY --from=builder /usr/local /usr/local
COPY src/ /friends_service/src

WORKDIR /friends_service
ARG UVICORN_WORKERS
ARG APPLICATION_PORT
CMD gunicorn src.main:app -b 0.0.0.0:${APPLICATION_PORT} -w ${UVICORN_WORKERS} -k uvicorn.workers.UvicornWorker
