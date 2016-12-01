#!/usr/bin/env bash

source ./common.sh

docker-compose -p jw-pyserver exec server ./restart.sh

fswatch -e ".*" -i "\.py$" -r . >>.fswatch_modified 2>&1 &

while [[ true ]]
do
	if [[ `wc .fswatch_modified | awk {'print $1'}` -gt 0 ]]; then
		cat /dev/null >.fswatch_modified
		docker-compose -p jw-pyserver exec server ./restart.sh
	fi

	sleep 1
done
