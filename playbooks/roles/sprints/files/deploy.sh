#!/usr/bin/env bash
set -ex
docker-compose pull
docker-compose up -d --no-deps django celeryworker
