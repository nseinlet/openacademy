#!/bin/bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r ../odoo/20.0/requirements.txt
python3 -m pip install faker