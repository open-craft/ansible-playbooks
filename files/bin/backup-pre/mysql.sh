#!/bin/bash

TMPDIR=/var/lib/mysql/backup

rm -rf "$TMPDIR"
mkdir -p "$TMPDIR"
mysql -s -e 'show databases' | tail -n +1 | grep -v performance_schema | grep -v information_schema | while read DBNAME; do mysqldump -uroot --complete-insert --events --single-transaction "$DBNAME" > "$TMPDIR/$DBNAME".sql; done
