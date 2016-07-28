#!/bin/bash

test -e /usr/local/stackstreamer_installed || ./scripts/install.sh
./scripts/run_gunicorn.sh