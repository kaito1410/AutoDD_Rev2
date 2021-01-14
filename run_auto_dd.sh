#!/bin/bash

if [ -d .env ]; then
    source ./.env/bin/activate
else
    echo "WARN: You do not have a virtual environment. Have you ran install_requirements.sh?"
    echo "Things might explode in a spectacular fashion"
fi

python -u main.py

if [ -d .env ]; then
    deactivate
fi