#!/usr/bin/env bash

if [ ! -d "venv" ]; then
    virtualenv venv
fi

source venv/bin/activate

pip3 install -r requirements.txt

python3 hibp.py
