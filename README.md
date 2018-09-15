# Ditto

[https://bulbapedia.bulbagarden.net/wiki/Ditto_(Pokémon)](https://bulbapedia.bulbagarden.net/wiki/Ditto_(Pok%C3%A9mon))

This repository contains:

 - Ditto script:
    - `ditto clone`: a script to crawl an instance of PokeAPI and download all objects
    - `ditto analyze`: a script to generate a JSON schema of the above data
    - `ditto transform`: a script to apply a new base url to data in `data/api` 
    - `ditto serve`: a script to serve the data in the same form as PokeAPI
       - with full support for dynamic pagination using GET args `offset` and `limit`

## Usage

```
pip install pokeapi-ditto
poetry run ditto --help
```
