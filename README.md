# Ditto

[https://bulbapedia.bulbagarden.net/wiki/Ditto_(Pokémon)](https://bulbapedia.bulbagarden.net/wiki/Ditto_(Pok%C3%A9mon))

This repository contains:

 - Ditto script:
    - `ditto clone`: a script to crawl an instance of PokeAPI and download all objects
    - `ditto analyze`: a script to generate a JSON schema of the above data
    - `ditto transform`: a script to apply a new base url to data in `data/api` 
    - `ditto serve`: a script to serve the data in the same form as PokeAPI
       - with full support for dynamic pagination using GET args `offset` and `limit`
 - Static data:
    - [data/api](data/api): a static copy of the JSON data generated with the above script
    - [data/schema](data/schema): a static copy of the PokeAPI schema generated from the above data
    - [updater](updater): a bot that runs in docker and can update the data stored in this repo

## Docker

This project is on Docker Hub. If you just want to serve a PokeApi clone, you
just have to run one command.

 - Replace `8080` with the port of your choice
 - Replace `http://localhost:8080` with the base url of your choice

``` bash
docker run -p 8080:80 -e DITTO_BASE_URL=http://localhost:8080 sargunv/pokeapi-ditto:latest
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

You can manually update the data if necessary. See [the updater bot](updater). You can run the bot in docker, or read and adapt its update script yourself. 
