#!/usr/bin/env bash

set -euo pipefail

function executeCommand() {
    echo "===== ${1}"
    ${2}
}

function executeComposeCommand() {
    executeCommand "${1}" "docker-compose ${2}"
}

function main() {
    docker login registry.gitlab.com -u ${DOCKER_USER} -p VFQ-C98sJnoaExeG7Kmn
    executeComposeCommand "PULLING IMAGES" "pull";
    executeComposeCommand "STOPPING CONTAINERS" "stop"
    executeComposeCommand "STARTING CONTAINERS" "up -d"
}

main;
