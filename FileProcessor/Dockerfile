FROM python:3.11


ENV PYTHONUNBUFFERED 1


RUN mkdir /app
WORKDIR /app

RUN apt-get update && \
    # apt-get install -y --no-install-recommends \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*



COPY requirements.txt /app/
COPY Pipfile Pipfile.lock /app/
RUN pip install -r requirements.txt

COPY . /app/

EXPOSE 8000
