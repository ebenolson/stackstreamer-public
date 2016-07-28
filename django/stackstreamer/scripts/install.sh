#!/bin/bash

head -c 32 /dev/urandom | base64 > /web/django/stackstreamer/django_key.secret
head -c 32 /dev/urandom | base64 > /web/django/stackstreamer/viewer_key.secret

source stackstreamerrc

yes no | ./manage.py syncdb
./manage.py migrate tastypie
./manage.py migrate djcelery
./manage.py collectstatic --noinput

export ADMIN_PASSWORD=`< /dev/urandom tr -dc _A-Z-a-z-0-9 | head -c${1:-8}`
python -m scripts.cmdline create_admin
echo "Admin password: " $ADMIN_PASSWORD
unset ADMIN_PASSWORD

touch /usr/local/stackstreamer_installed