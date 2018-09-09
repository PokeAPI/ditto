FROM python:3.6

MAINTAINER Sargun Vohra <sargun.vohra@gmail.com>

ENV PYTHONUNBUFFERED 1
ENV DITTO_BASE_URL http://localhost/

EXPOSE 80

RUN mkdir /ditto
WORKDIR /ditto/

COPY pyproject.* /ditto/
COPY pokeapi_ditto /ditto/pokeapi_ditto
COPY data /ditto/data

RUN curl -sSL https://raw.githubusercontent.com/sdispater/poetry/master/get-poetry.py | python
RUN poetry install
CMD poetry run ditto serve "--base-url=$DITTO_BASE_URL"
