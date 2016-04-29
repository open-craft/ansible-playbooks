#!/bin/bash

TMPDIR='{{ MONGODB_SERVER_BACKUP_DIR }}'

rm -rf "$TMPDIR"
sudo -u mongodb mkdir -p "$TMPDIR"
sudo -u mongodb mongodump -u '{{ MONGODB_ROOT_ADMIN_NAME }}' -p '{{ MONGODB_ROOT_ADMIN_PASSWORD }}' -o "$TMPDIR"
