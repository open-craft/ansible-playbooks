#!/usr/bin/env bash
# Will exit on first error (we want it!)
set -e

BACKUPSDIR="/var/backups/catchpy/"
sudo su postgres -c "pg_dumpall" | gzip > ${BACKUPSDIR}/catchpy_db.gz
