Ditto
=====

This repository contains a copy of the JSON data generated from
`PokeAPI`_ based on `Veekun’s data`_.

Usage
-----

.. code:: bash

    cd ~
    git clone https://github.com/pokesource/ditto.git
    cd ditto
    python3 setup.py develop --user
    ditto serve --port 8080 --source ./data

Uninstall
---------

.. code:: bash

    cd ~/ditto
    python3 setup.py develop --user --uninstall

Docker
------

Replace 8080 with the port of your choice.

.. code:: bash

    # After cloning the repo to ~
    cd ~/ditto
    docker build -t ditto .
    docker run -d -p 8080:80 ditto
    

Advanced
--------

You can manually update the data if necessary. This is quite an involved
process. You shouldn’t really need to do this, since I’ll be keeping the
data in this repo up to date. But if I abandon it for some reason,
here’s how to update it.

Before starting, you’ll need to install `Docker and Docker Compose`_.

First clone the PokeAPI repository:

.. code:: bash

    cd ~
    git clone https://github.com/PokeAPI/pokeapi.git
    cd pokeapi

Apply the patch to disable rate limiting on your local PokeAPI:

.. code:: bash

    # Assuming you have this "ditto" repo in ../ditto
    git apply ../ditto/disable-rate-limit.patch

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
    # This will take a loooong time!
    build_all()

Once that’s done, you can finally update Ditto’s data:

.. code:: bash

    cd ../ditto
    rm -r ./data
    python3 setup.py install --user # If you didn't do this already
    ditto clone --source http://localhost/ --destination ./data

And now serve the fresh data!

.. code:: bash

    make serve

.. _PokeAPI: https://github.com/PokeAPI/pokeapi
.. _Veekun’s data: https://github.com/veekun/pokedex
.. _Docker and Docker Compose: https://docs.docker.com/compose/install/
