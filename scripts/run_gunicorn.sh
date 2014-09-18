#!/bin/bash
set -e 
LOGFILE=/home/app/logs/gunicorn.log 
LOGDIR=$(dirname $LOGFILE)
NUM_WORKERS=2 
USER=app 
GROUP=web ADDRESS=127.0.0.1:8000

cd /web/django/stackstreamer
source venv/bin/activate
test -d $LOGDIR || mkdir -p $LOGDIR
exec gunicorn -w $NUM_WORKERS --bind=$ADDRESS \
  --user=$USER --group=$GROUP --log-level=debug \
  --log-file=$LOGFILE stackstreamer.wsgi:application
