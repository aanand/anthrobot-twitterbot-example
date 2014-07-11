FROM orchardup/python:2.7

RUN apt-get update -qq && apt-get install -y git python-psycopg2

RUN mkdir /code
WORKDIR /code

ADD requirements.txt /code/requirements.txt
RUN pip install -r requirements.txt

ADD . /code

ENV PYTHONUNBUFFERED 1
CMD python bot.py
