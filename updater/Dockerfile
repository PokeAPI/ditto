FROM docker:dind

RUN apk update
RUN apk add curl python3 git bash dos2unix openssh build-base python3-dev

RUN ln -sf $(ls /usr/bin/easy_install*) /usr/bin/easy_install
RUN easy_install pip
RUN pip install docker-compose
RUN pip install poetry

RUN mkdir /updater
WORKDIR /updater
COPY . /updater/
RUN dos2unix cmd.bash

ENV COMMIT_NAME 'Updater Bot'
ENV COMMIT_EMAIL 'anon@example.com'
ENV COMMIT_MESSAGE '[Updater Bot] Regenerate data'
ENV BRANCH_NAME 'updater-bot'
ENV REPO_POKEAPI  'git@github.com:sargunv/pokeapi'
ENV REPO_DITTO  'git@github.com:sargunv/ditto'

CMD bash cmd.bash
