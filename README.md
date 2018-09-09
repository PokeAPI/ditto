# Ditto

[https://bulbapedia.bulbagarden.net/wiki/Ditto_(Pokémon)](https://bulbapedia.bulbagarden.net/wiki/Ditto_(Pok%C3%A9mon))

This repository contains:

 - `ditto clone`: a script to crawl an instance of PokeAPI and download all objects
 - `data/api`: a static copy of the JSON data generated with the above script
 - `ditto analyze`: a script to generate a JSON schema of the above data
 - `data/schema`: a static copy of the PokeAPI schema generated from the above data
 - `ditto transform`: a script to apply a new base url to data in `data/api` 
 - `ditto serve`: a script to serve the data in the same form as PokeAPI
    - with full support for dynamic pagination using GET args `offset` and `limit`

## Docker

This project is on Docker Hub. If you just want to serve a PokeApi clone, you
just have to run one command.

 - Replace `8080` with the port of your choice
 - Replace `http://localhost:8080` with the base url of your choice

``` bash
docker run -p 8080:80 -e DITTO_BASE_URL=http://localhost:8080 sargunv/pokeapi-ditto
```

## Usage

If you'd rather use the data for something else, you can generate a
copy with the base url of your choice applied. This assumes
[Poetry](https://poetry.eustace.io/) is installed and in your PATH. 

``` bash
git clone https://github.com/PokeAPI/ditto.git
cd ditto
poetry install
poetry run ditto transform --base-url http://localhost:8080
```

For other ditto functionality, run `poetry run ditto --help` 

If you're on Windows, you'll have to adapt the commands above to your platform.
The general idea is the same.

## Advanced

You can manually update the data if necessary. If I abandon this
project, here’s how to update it. It's a bit of an involved process.

Before starting, you’ll need to install [Docker and Docker
Compose](https://docs.docker.com/compose/install/). You'll
also need [Poetry](https://poetry.eustace.io/) in your PATH.

First clone the PokeAPI and Ditto repositories:

``` bash
cd ~
git clone https://github.com/PokeAPI/ditto.git
git clone https://github.com/PokeAPI/pokeapi.git
```

Apply the patch to disable rate limiting on your local PokeAPI:

``` bash
# Assuming you have the repos in ~
cd ~/pokeapi
git apply ~/ditto/extra/disable-rate-limit.patch
```

Run PokeAPI using docker-compose:

``` bash
docker volume create --name=redis_data
docker volume create --name=pg_data
docker-compose up -d
```

Build the PokeAPI database:

``` bash
docker-compose exec app python manage.py migrate
docker-compose exec app python manage.py shell
```

``` python
from data.v2.build import build_all
build_all()
```

Once it’s done, you can update Ditto’s data:

``` bash
cd ~/ditto
rm -r ./data
poetry install
poetry run ditto clone --src-url http://localhost/ --dest-dir ./data
poetry run ditto analyze --api-dir ./data/api --schema-dir ./data/schema
```

This will crawl your local instance of PokeAPI, copy all the data to
./data, and regenerate the schema.

Once that's finished, you can serve the freshly updated data!

``` bash
poetry run ditto serve --port 8080 --base-url http://localhost:8080
```