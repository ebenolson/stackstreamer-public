#!/bin/bash

tar -cvjf /web/django/dbbackup/$(date +%Y%m%d).tar.bz2 /web/django/stackstreamer/db.sqlite3