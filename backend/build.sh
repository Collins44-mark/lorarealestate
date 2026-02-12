#!/bin/bash
# Render build script - creates admin user automatically (no Shell needed on free tier)
set -e
pip install -r requirements.txt
python manage.py collectstatic --noinput
python manage.py migrate --noinput
python manage.py ensure_admin
