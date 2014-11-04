Installation Guide
==================

* Start with an Ubuntu 14.04.1 LTS amd64 server base image
All commands should be run as `root` unless noted

* Install dependencies

        apt-get update
        apt-get install libjpeg-dev libtiff-dev python-dev python-numpy zip mercurial gunicorn npm nodejs-legacy rabbitmq-server python-virtualenv nginx

* Clone repository

         hg clone https://bitbucket.org/emolson/stackstreamer-public /web

* Set up python environment

        cd /web/django/stackstreamer 
        virtualenv venv
        source venv/bin/activate
        pip install -r requirements.txt

        cd /web/node
        npm install
        npm install -g forever

* Create user 

        addgroup web
        adduser app
        usermod -G web app

* Execute setup script

        /web/setup-scripts/setup.sh

* Prepare Django database
Run these commands as the `app` user

        su app
        cd /web/django/stackstreamer
        source venv/bin/activate
        ./manage.py syncdb
        ./manage.py migrate tastypie
        ./manage.py migrate djcelery
        ./manage.py collectstatic

* Place your data files in the `/data/` directory. Make sure to follow the format specification. To import new stacks, run the import script as the `app` user

        su app
        /web/django/stackstreamer/scripts/import.sh
