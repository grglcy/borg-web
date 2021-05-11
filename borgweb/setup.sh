#!/usr/bin/env bash

function fill_line () {
	printf '=%.0s' $(seq 1 $1)
}

function print_action () {
	printf "\n"
	fill_line $(tput cols)
	printf "\n$1\n"
	fill_line $(tput cols)
	printf "\n\n"
}

cd "${0%/*}"

if ! source ./.venv/bin/activate; then
	printf "No venv activation script\n"
    if [ -d "./.venv" ]
	then
		printf "Removing old venv\n"
		rm -r ./.venv
	fi
	printf "Creating new venv\n"
	
	# Create venv at ./.venv
	virtualenv ./.venv --prompt "(borg-web) "
	source ./.venv/bin/activate
fi

print_action "Installing pip packages, this may take a while..."

# install required pip packages
yes | python -m pip install --upgrade wheel
yes | python -m pip install django gunicorn sass django-libsass django_compressor

print_action "Setting up static files and database"

# setup static files and database
python ./manage.py collectstatic --noinput --link
python ./manage.py migrate --noinput

deactivate
