#!/bin/bash

source .venv/bin/activate

uvicorn main:app --host stag.localhost --port 8000 --reload
