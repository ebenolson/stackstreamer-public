#!/bin/bash
cp /web/setup-scripts/celeryd.conf.example /etc/default/celeryd
cp /web/setup-scripts/celeryd.sh.example /etc/init.d/celeryd

cp /web/setup-scripts/gunicorn.conf.example /etc/init/gunicorn.conf
ln -s /lib/init/upstart-job /etc/init.d/gunicorn

cp /web/setup-scripts/node.conf.example /etc/init/node.conf
ln -s /lib/init/upstart-job /etc/init.d/node

cp /web/setup-scripts/nginx-site.example /etc/nginx/sites-enabled/default

head -c 32 /dev/urandom | base64 > /web/django/stackstreamer/django_key.secret
head -c 32 /dev/urandom | base64 > /web/django/stackstreamer/viewer_key.secret

chown -R app /web
chgrp -R web /web

mkdir /data
chown app /data
chgrp web /data

service nginx reload
service node start
service gunicorn start
/etc/init.d/celeryd start
