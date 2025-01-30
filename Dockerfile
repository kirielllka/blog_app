FROM python:3.11-buster
LABEL authors='Yan'

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /blog_backend

RUN apt-get update && \
    apt install -y python3-dev

RUN pip install --upgrade pip
RUN pip install poetry  
COPY pyproject.toml .
RUN apt-get update && \
    apt install -y python3-dev

COPY . .


ENV PYTHONPATH=/blog_backend/src

WORKDIR /blog_backend/src


CMD ["python", "manage.py", "runserver"]    

EXPOSE 8000