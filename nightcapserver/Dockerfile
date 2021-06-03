FROM python:3.8-slim as production

ENV PYTHONUNBUFFERED=1
WORKDIR /app/

RUN apt-get update && \
    apt-get install -y \
    bash \
    build-essential \
    gcc \
    libffi-dev \
    musl-dev \
    openssl \
    libpq-dev

COPY ./nightcapsite ./nightcapsite
COPY ./nightcapserver ./nightcapserver
COPY ./requirements.txt ./requirements.txt
RUN pip install -r ./requirements.txt

EXPOSE 8000 

FROM production as development

COPY . .
RUN pip install -r ./dev.txt