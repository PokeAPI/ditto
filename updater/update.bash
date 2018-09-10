#!/usr/bin/env bash

# This script assumes you've done some setup already:
#  - These executables are in your PATH
#     - git
#     - docker
#     - docker-compose
#     - poetry
#  - Nothing else is using ports used by PokeAPI
#  - Git is configured with appropriate name and email
#  - GitHub SSH keys are configured
#
# The script should be run from the working directory containing the rate limit
# patch and no ditto or pokeapi repository present.

set -e
set -o pipefail

BRANCH_NAME='updater-bot'
COMMIT_MESSAGE='[Updater Bot] Regenerate data'

git clone git@github.com:PokeAPI/ditto.git --depth=1
git clone git@github.com:PokeAPI/pokeapi.git --depth=1

# set up the pokeapi side
cd pokeapi
git apply ../disable-rate-limit.patch

docker volume create --name=redis_data
docker volume create --name=pg_data
docker-compose up -d

docker-compose exec app python manage.py migrate
echo "from data.v2.build import build_all; build_all()" \
    | docker-compose exec app python manage.py shell

# set up the ditto side
cd ../ditto
git branch -D ${BRANCH_NAME} || true
git branch ${BRANCH_NAME}
git checkout ${BRANCH_NAME}

poetry install
rm -r ./data
poetry run ditto clone --src-url http://localhost/ --dest-dir ./data
poetry run ditto analyze --api-dir ./data/api --schema-dir ./data/schema

# commit and push
git add data
git commit -m ${COMMIT_MESSAGE}
git push -fu origin ${BRANCH_NAME}

# cleanup
cd ../ditto
docker-compose kill
docker-compose rm -f
docker volume rm redis_data
docker volume rm pg_data
cd ..
rm -rf ditto pokeapi