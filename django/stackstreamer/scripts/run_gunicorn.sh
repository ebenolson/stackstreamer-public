#!/bin/bash
set -e 
LOGFILE=/web/logs/gunicorn.log 
LOGDIR=$(dirname $LOGFILE)
NUM_WORKERS=2 
ADDRESS=0.0.0.0:8000

test -d $LOGDIR || mkdir -p $LOGDIR
exec gunicorn -w $NUM_WORKERS --bind=$ADDRESS --log-level=debug --log-file=$LOGFILE stackstreamer.wsgi:application
