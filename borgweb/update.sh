#!/usr/bin/env bash

cd "${0%/*}"

source ./venv/bin/activate
python ./manage.py collectstatic --noinput
python ./manage.py compress
python ./manage.py migrate --noinput
deactivate