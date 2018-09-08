# Ditto

[https://bulbapedia.bulbagarden.net/wiki/Ditto_(Pokémon)](https://bulbapedia.bulbagarden.net/wiki/Ditto_(Pok%C3%A9mon))

This repository contains:

 -   a static copy of the JSON data generated from
     [PokeAPI](https://github.com/PokeAPI/pokeapi) based on
     [Veekun’s data](https://github.com/veekun/pokedex)
 -   a PokeAPI schema generated from the above data
 -   a script to serve the data in the same form as PokeAPI
 -   a script to crawl an instance of PokeAPI to regenerate the data
 -   a script to analyze the generated data and produce a JSON Schema

## Usage

This project is on Docker Hub. If you just want to run it, you just have
to run one command. Replace `8080` with the port of your choice.

``` bash
docker run -p 8080:80 sargunv/pokeapi-ditto
```

## Development

If you plan to edit the project, you can install it locally for
development. [Poetry](https://poetry.eustace.io/) is required.

``` bash
cd ~
git clone https://github.com/PokeAPI/ditto.git
cd ditto
poetry install

# now you can run ditto!
poetry run ditto --help
```

## Advanced

You can manually update the data if necessary. If I abandon this
project, here’s how to update it. It's a bit of an involved process.

Before starting, you’ll need to install [Docker and Docker
Compose](https://docs.docker.com/compose/install/). You'll
also need [Poetry](https://poetry.eustace.io/).

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

The above step can take a really long time to complete. Once it’s done,
you can finally update Ditto’s data:

``` bash
cd ~/ditto
rm -r ./data
poetry install
poetry run ditto clone --source http://localhost/ --destination ./data
poetry run ditto analyze --api-dir ./data/api --schema-dir ./data/schema
```

This will crawl your local instance of PokeAPI, copy all the data to
./data, and regenerate the schema. Once that's finished, you can serve
the freshly updated data!

``` bash
poetry run ditto serve --port 8080
```
