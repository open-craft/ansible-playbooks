#!/bin/bash

TMPDIR=/var/lib/postgresql/backup

rm -rf "$TMPDIR"
mkdir -p "$TMPDIR"
sudo -u postgres pg_dumpall > "$TMPDIR/postgresql_all_dbs.sql"
