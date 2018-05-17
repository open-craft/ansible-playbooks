#!/usr/bin/env bash
# Will exit on first error (we want it!)
set -e

service gunicorn restart

timestamp=$(date +%Y%m%dT%H:%M:%S)

mv /var/log/lpd/debug.log-* "{{ LPD_LOG_DOWNLOAD_LOG_DIR }}"
chown "{{ LPD_LOG_DOWNLOAD_USER }}:{{ LPD_DB_USERNAME }}" "{{ LPD_LOG_DOWNLOAD_LOG_DIR }}" "{{ LPD_LOG_DOWNLOAD_DB_DIR }}"
chmod g+rwx "{{ LPD_LOG_DOWNLOAD_LOG_DIR }}" "{{ LPD_LOG_DOWNLOAD_DB_DIR }}"
sudo -u "{{ LPD_DB_USERNAME }}" -H {{LPD_MANAGE_PY}} dumpdata -o "{{ LPD_LOG_DOWNLOAD_DB_DIR }}/database-${timestamp}.json"
mysqldump -u "{{ LPD_DB_USERNAME }}" -p'{{ LPD_DB_PASSWORD }}' -h "{{ LPD_DB_HOST }}" "{{ LPD_DB_NAME }}" -r "{{ LPD_LOG_DOWNLOAD_DB_DIR }}/database-${timestamp}.sql"
gzip "{{ LPD_LOG_DOWNLOAD_LOG_DIR }}"/* "{{ LPD_LOG_DOWNLOAD_DB_DIR }}"/*
chown "{{ LPD_LOG_DOWNLOAD_USER }}:{{ LPD_LOG_DOWNLOAD_USER }}" "{{ LPD_LOG_DOWNLOAD_LOG_DIR }}"/* "{{ LPD_LOG_DOWNLOAD_DB_DIR }}"/*
