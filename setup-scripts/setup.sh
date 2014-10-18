#!/bin/bash
cp /web/setup-scripts/celeryd.conf.example /etc/default/celeryd
cp /web/setup-scripts/celeryd.sh.example /etc/init.d/celeryd

cp /web/setup-scripts/gunicorn.conf.example /etc/init/gunicorn.conf
ln -s /lib/init/upstart-job /etc/init.d/gunicorn

cp /web/setup-scripts/node.conf.example /etc/init/node.conf
ln -s /lib/init/upstart-job /etc/init.d/node

cp /web/setup-scripts/nginx-site.example /etc/nginx/sites-enabled/default

service nginx reload
service node start
service gunicorn start
/etc/init.d/celeryd start
