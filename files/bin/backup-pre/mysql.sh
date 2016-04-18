#!/bin/bash

TMPDIR=/var/lib/mysql/backup

rm -rf "$TMPDIR"
mkdir -p "$TMPDIR"
mysql -e 'show databases' | while read DBNAME; do mysqldump -uroot --complete-insert --events --single-transaction "$DBNAME" > "$TMPDIR/$DBNAME".sql; done
