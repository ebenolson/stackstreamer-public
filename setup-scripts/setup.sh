#!/bin/bash
cp /web/setup-scripts/celeryd.conf.example /etc/init/celeryd.conf
ln -s /lib/init/upstart-job /etc/init.d/celeryd

cp /web/setup-scripts/gunicorn.conf.example /etc/init/gunicorn.conf
ln -s /lib/init/upstart-job /etc/init.d/gunicorn

cp /web/setup-scripts/node.conf.example /etc/init/node.conf
ln -s /lib/init/upstart-job /etc/init.d/node

service node start
service gunicorn start
service celeryd start
