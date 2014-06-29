FROM orchardup/python:2.7

RUN apt-get update -qq && apt-get install -y git

ADD . /code
WORKDIR /code

RUN pip install -r requirements.txt

ENV PYTHONUNBUFFERED 1
CMD ./run.sh
