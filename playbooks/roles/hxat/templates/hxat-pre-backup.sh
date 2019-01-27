#!/usr/bin/env bash
# Will exit on first error (we want it!)
set -e

BACKUPSDIR="/var/backups/hxat/"
sudo su postgres -c "pg_dumpall" | gzip > ${BACKUPSDIR}/hxat_db.gz
