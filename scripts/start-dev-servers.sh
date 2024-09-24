#!/bin/env bash

cd /home/dhwanil/personal-github/PyFinMange/scripts/execution

## Start FastApi Server
nohup /home/dhwanil/personal-github/PyFinMange/.venv/bin/python \
    /home/dhwanil/personal-github/PyFinMange/backend/start-dev-uvicorn-server.py > /home/dhwanil/personal-github/PyFinMange/scripts/execution/logs/start-script/fastapi.log 2>&1 &
#Log the process ID
echo $! > "/home/dhwanil/personal-github/PyFinMange/scripts/execution/logs/$0.FastAPI.pid"


# Start vue server
cd ../../frontend-vue/
nohup npm run dev > /home/dhwanil/personal-github/PyFinMange/scripts/execution/logs/start-script/vue.log 2>&1 &
VUE_PID=$!

# Log the process ID
echo $! > "/home/dhwanil/personal-github/PyFinMange/scripts/execution/logs/$0.frontend-vue.pid"

sleep 5
if ps -p $VUE_PID > /dev/null; then
    echo "Vue Started "
else
    return 1
fi



