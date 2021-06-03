#!/usr/bin/env bash

function fill_line () {
	printf '=%.0s' $(seq 1 $1)
	printf "\n"
}

function print_action () {
	printf "\n"
	fill_line $(tput cols)
	printf "$1\n"
	fill_line $(tput cols)
	printf "\n"
}

cd "${0%/*}"

print_action "Checking for existence of python venv"

if ! source ./venv/bin/activate; then
	printf "No venv activation script\n"
    if [ -d "./venv" ]
	then
		printf "Removing old venv\n"
		rm -r ./venv
	fi
	printf "Creating new venv\n"
	
	# Create venv at ./venv
	virtualenv ./venv --prompt "(borg-web) "
	source ./venv/bin/activate
fi

print_action "Installing pip packages, this may take a while..."

# install required pip packages
yes | python -m pip install --upgrade wheel
yes | python -m pip install django gunicorn django-libsass django-compressor django-axes django-redis

print_action "Setting up static files and database"

# setup static files and database
python ./manage.py collectstatic --noinput --link
python ./manage.py migrate --noinput

deactivate
