#!/bin/bash

. ./venv/bin/activate
for port in 800{0..3}
do
  uvicorn --port ${port} main_fastapi:app --reload &
done
