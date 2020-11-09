FROM python:3.8-slim-buster as builder
RUN pip install --upgrade pip
COPY requirements.txt /tmp
RUN pip install -r /tmp/requirements.txt

FROM python:3.8-slim-buster as runner
COPY --from=builder /usr/local /usr/local
COPY src/ /friends_service/src

WORKDIR /friends_service
CMD uvicorn src.main:app --host 0.0.0.0 --port 5057