#!/bin/bash

apt-get update
apt-get install libpq-dev python3-dev python3.10-venv
cd /tmp
python3 -m venv venv
source venv/bin/activate
pip install docker psycopg2
python3 create_user.py
