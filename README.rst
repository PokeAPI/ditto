.. image:: https://img.shields.io/docker/pulls/pokesource/ditto.svg?maxAge=3600 :target: https://hub.docker.com/r/pokesource/ditto/

Ditto
=====

`http://bulbapedia.bulbagarden.net/wiki/Ditto_(Pokemon)`

This repository contains:
 - a static copy of the JSON data generated from `PokeAPI`_ based on `Veekun’s data`_
 - a PokeAPI schema generated from the above data
 - a script to serve the data in the same form as PokeAPI
 - a script to crawl an instance of PokeAPI to regenerate the data
 - a script to analyze the generated data and produce a JSON Schema

Usage
-----

This project is on Docker Hub. If you just want to run it, you just have to run one command. Replace ``8080`` with the port of your choice.

.. code:: bash

    docker run -p 8080:80 pokesource/ditto

Development
-----------

If you plan to edit the project, you can install it locally for development.

.. code:: bash

    cd ~
    git clone https://github.com/pokesource/ditto.git
    cd ditto
    pip3 install -r requirements.txt
    python3 setup.py develop
    ditto serve --port 8080

Advanced
--------

You can manually update the data if necessary. If I abandon this project, here’s how to update it. It's a bit of an involved process.

Before starting, you’ll need to install `Docker and Docker Compose`_. These instructions assume you've cloned this repo into ``~/ditto``.

First clone the Ditto and PokeAPI repositories:

.. code:: bash

    cd ~
    git clone https://github.com/pokesource/ditto.git
    git clone https://github.com/PokeAPI/pokeapi.git

Apply the patch to disable rate limiting on your local PokeAPI:

.. code:: bash

    # Assuming you have the repos in ~
    cd ~/pokeapi
    git apply ~/ditto/extra/disable-rate-limit.patch

Run PokeAPI using docker-compose:

.. code:: bash

    docker volume create --name=redis_data
    docker volume create --name=pg_data
    docker-compose up -d

Build the PokeAPI database:

.. code:: bash

    docker-compose exec app python manage.py migrate
    docker-compose exec app python manage.py shell

.. code:: python

    from data.v2.build import build_all
    build_all()

The above step can take a really long time to complete. Once it’s done, you can finally update Ditto’s data:

.. code:: bash

    cd ~/ditto
    rm -r ./data
    pip3 install -r requirements.txt # If you didn't do these two already
    python3 setup.py develop         #
    ditto clone --source http://localhost/ --destination ./data
    ditto analyze --api-dir ./data/api --schema-dir ./data/schema

This will crawl your local instance of PokeAPI, copy all the data to `./data`, and regenerate the schema.
Once that's finished, you can serve the freshly updated data!

.. code:: bash

    ditto serve --port 8080

.. _PokeAPI: https://github.com/PokeAPI/pokeapi
.. _Veekun’s data: https://github.com/veekun/pokedex
.. _Docker and Docker Compose: https://docs.docker.com/compose/install/
