#!/usr/bin/env bash
# exit on error
set -o errexit

pip install -r requirements.txt

# Run database initialization if needed
python seed_data.py

