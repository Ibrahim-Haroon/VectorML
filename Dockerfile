FROM python:3.11

ENV PYTHONUNBUFFERED 1
ENV TZ=America/New_York
ENV PYTHONPATH="/VectorML/src:$PYTHONPATH"

WORKDIR /VectorML

RUN apt-get update && apt-get install -y \
    libhdf5-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

CMD ["/bin/bash"]