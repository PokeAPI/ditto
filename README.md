# Ditto

This repository contains a copy of the JSON data generated from [PokeAPI](https://github.com/PokeAPI/pokeapi) based on [Veekun's data](https://github.com/veekun/pokedex).

## Usage

Just use the command `make serve` to serve the data. Edit the Makefile to change the port.

```bash
cd ~
git clone https://github.com/pokesource/ditto.git
cd ditto
make serve
```

## Advanced

You can manually update the data if necessary. This is quite an involved process. You shouldn't really need to do this, since I'll be keeping the data in this repo up to date. But if I abandon it for some reason, here's how to update it.

Before starting, you'll need to install [Docker and Docker Compose](https://docs.docker.com/compose/install/).

First clone the PokeAPI repository:

```bash
cd ~
git clone https://github.com/PokeAPI/pokeapi.git
cd pokeapi
```

Apply the patch to disable rate limiting on your local PokeAPI:

```bash
# Assuming you have this "ditto" repo in ../ditto
git apply ../ditto/disable-rate-limit.patch
```

Run PokeAPI using docker-compose:

```bash
docker volume create --name=redis_data
docker volume create --name=pg_data
docker up -d
```

Build the PokeAPI database:

```bash
docker-compose exec app python manage.py migrate
docker-compose exec app python manage.py shell
```

```python
from data.v2.build import build_all
# This will take a loooong time!
build_all()
```

Once that's done, you can finally update Ditto's data:

```bash
cd ../ditto
make clean
make data
```

And now serve the fresh data!

```bash
make serve
```
