FROM python:3-alpine

RUN pip install poetry

ADD . /ditto

WORKDIR /ditto

RUN poetry install
CMD poetry run ditto clone --dest-dir ./data && \
    poetry run ditto clone --src-url http://localhost/ --dest-dir ./data --select pokemon/129 && \
    poetry run ditto analyze --data-dir ./data && \
    poetry run ditto transform \
        --base-url='https://pokeapi.co' \
        --src-dir=./data \
        --dest-dir=./_gen