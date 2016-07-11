.. image:: https://img.shields.io/docker/pulls/pokesource/ditto.svg?maxAge=3600
   :target: https://hub.docker.com/r/pokesource/ditto/

Ditto
=====

This repository contains a copy of the JSON data generated from `PokeAPI`_ based on `Veekun’s data`_. It also contains a small server script to serve the data in the same form as PokeAPI, and a crawler script to harvest the data from an instance of PokeAPI.

Usage
------

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
    python3 setup.py develop --user
    ditto serve --port 8080 --source ./data

Advanced
--------

You can manually update the data if necessary. This is quite an involved process. You shouldn’t really need to do this, since I’ll be keeping the data in this repo up to date. But if I abandon it for some reason, here’s how to update it.

Before starting, you’ll need to install `Docker and Docker Compose`_. These instructions assume you've cloned this repo into ``~/ditto``.

First clone the PokeAPI repository:

.. code:: bash

    cd ~
    git clone https://github.com/PokeAPI/pokeapi.git
    cd pokeapi

Apply the patch to disable rate limiting on your local PokeAPI:

.. code:: bash

    # Assuming you have this "ditto" repo in ../ditto
    git apply ~/ditto/extra/disable-rate-limit.patch

Run PokeAPI using docker-compose:

.. code:: bash

    docker volume create --name=redis_data
    docker volume create --name=pg_data
    docker up -d

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
    python3 setup.py develop --user  #
    ditto clone --source http://localhost/ --destination ./data

This will crawl your local instance of PokeAPI and copy all the data to `./data`. Once that's finished, you can serve the freshly updated data!

.. code:: bash

    ditto serve --port 8080 --source ./data

.. _PokeAPI: https://github.com/PokeAPI/pokeapi
.. _Veekun’s data: https://github.com/veekun/pokedex
.. _Docker and Docker Compose: https://docs.docker.com/compose/install/
