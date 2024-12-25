
FROM --platform=linux/amd64 python:3.12-slim

RUN apt-get update && apt-get install -y curl

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --upgrade pip \
    && pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./src /code/app

EXPOSE 8080

CMD ["fastapi", "run", "app/main.py", "--port", "8080"]