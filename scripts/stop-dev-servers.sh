#!/bin/env bash

kill $(cat ./execution/logs/start-dev-servers.sh.FastAPI.pid) && echo "" > ./execution/logs/start-dev-servers.sh.FastAPI.pid

#kill $(cat ./execution/logs/start-dev-servers.sh.frontend-vue.pid) && echo "" > ./execution/logs/start-dev-servers.sh.FastAPI.pid

## kill all node servers in the project
pkill -f /home/dhwanil/personal-github/PyFinMange/frontend-vue/node_modules/.bin/vite