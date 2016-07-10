# Ditto

This repository contains a copy of the JSON data generated from [PokeAPI](https://github.com/PokeAPI/pokeapi) based on [Veekun's data](https://github.com/veekun/pokedex).

## Usage

Just use the command `make serve` (TODO) to serve the data. Edit the Makefile to change the port.

## Update

To update the data, first set up a local instance of the PokeApi application, preferably with rate limiting disabled. You can use the included `disable-rate-limit.patch` file to disable rate limiting on PokeApi. Once that's running, use the commands `make clean; make data` to purge the data and download the new data from the api. The script assumes it's being served on `localhost:80`, but that can be changed by editing the Makefile.

Please don't point the script at the live PokeApi! Use it with a local instance of the api.
