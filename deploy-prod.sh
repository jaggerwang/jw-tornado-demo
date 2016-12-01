#!/usr/bin/env bash

source ./common.sh

log INFO "docker compose begin ..."
docker-compose -p jw-pyserver -f docker-compose.yml up -d
log INFO "docker compose end"

exit 0
