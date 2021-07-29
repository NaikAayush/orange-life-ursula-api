#!/bin/sh

source env/bin/activate
uvicorn app:app --host 0.0.0.0 --port 80
