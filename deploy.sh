#!/usr/bin/env bash

source ./common.sh

log INFO "docker compose begin ..."
docker-compose -p jw-pyserver up -d
log INFO "docker compose end"

log INFO "create db indexes begin ..."
docker-compose -p jw-pyserver exec server ./src/manage.py create-mongodb-index
log INFO "create db indexes end"

exit 0
