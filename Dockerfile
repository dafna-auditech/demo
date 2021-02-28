FROM python:3.8.7-slim-buster
ENV PYTHONUNBUFFERED 1
ENV DJANGO_SETTINGS_MODULE=graph_tutorial.settings
RUN mkdir /code
WORKDIR /code
COPY requirements.txt /code/
RUN pip install -r requirements.txt
RUN apt-get update \
  && apt-get install -y wget

COPY . /code/
EXPOSE 5545

WORKDIR /code/graph_tutorial

RUN /bin/bash -c "echo $(pwd);\
        python3 manage.py migrate;"

CMD python3 manage.py runserver 0.0.0.0:5545