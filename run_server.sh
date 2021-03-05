#!/bin/bash

. ./venv/bin/activate
uvicorn main_fastapi:app --reload
