FROM python:3.8-slim-buster as builder
COPY requirements.txt /tmp
RUN pip install -r /tmp/requirements.txt

FROM python:3.8-slim-buster as runner
COPY --from=builder /usr/local /usr/local
COPY src /app

WORKDIR /app
CMD uvicorn main:app --host 0.0.0.0 --port 5057