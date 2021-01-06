#!/usr/bin/env bash

set -euo pipefail

cd $(dirname $0)

function executeCommand() {
    echo "===== ${1}"
    ${2}
}

function executeComposeCommand() {
    executeCommand "${1}" "docker-compose ${2}"
}

function main() {
    executeComposeCommand "PULLING IMAGES" "pull";
    executeComposeCommand "RESTARTING CONTAINERS" "up -d --no-deps django celeryworker"
    executeCommand "CLEANING UP DOCKER SYSTEM" "docker system prune -f"
}

main;
