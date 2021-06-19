FROM tiangolo/uvicorn-gunicorn:python3.8
ENV ELASTIC_HOST=elasticsearch
ENV REDIS_HOST=redis
COPY ./src /app
RUN pip install --upgrade pip
RUN pip install -r requirements.txt --force-reinstall