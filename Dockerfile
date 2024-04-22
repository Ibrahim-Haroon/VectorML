FROM python:3.11

ENV PYTHONUNBUFFERED 1
ENV TZ=America/New_York

WORKDIR /VectorML

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .