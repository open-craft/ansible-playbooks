#!/usr/bin/env bash

set -euo pipefail

function executeCommand() {
    echo "===== ${1}"
    exec "${2}"
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
