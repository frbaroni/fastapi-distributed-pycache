#!/bin/bash

PORTS=(800{0..3})

. ./venv/bin/activate

for PORT in "${PORTS[@]}"
do
  export MY_NAME=http://localhost:${PORT}/
  uvicorn --port ${PORT} --reload main_fastapi:app &
done

read 

sleep 0.5
./kill_server.sh
