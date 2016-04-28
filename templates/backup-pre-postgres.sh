#!/bin/bash

TMPDIR="{{ POSTGRES_SERVER_BACKUP_DIR }}"

rm -rf "$TMPDIR"
mkdir -p "$TMPDIR"
sudo -u postgres pg_dumpall > "$TMPDIR/postgresql_all_dbs.sql"
