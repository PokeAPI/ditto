FROM python:3.6

MAINTAINER Sargun Vohra <sargun.vohra@gmail.com>

RUN curl -sSL https://raw.githubusercontent.com/sdispater/poetry/master/get-poetry.py | python

RUN mkdir /ditto
WORKDIR /ditto/
ADD . /ditto/

RUN poetry install

CMD poetry run ditto serve
EXPOSE 80
