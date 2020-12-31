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
    executeComposeCommand "STOPPING CONTAINERS" "stop"
    executeComposeCommand "STARTING CONTAINERS" "up -d"
}

main;
