# borg-web
Summarises [borg](https://borgbackup.readthedocs.io/en/stable/#what-is-borgbackup) backups using output from '[borg create](https://borgbackup.readthedocs.io/en/stable/usage/create.html#description)'.
Supersedes my previous project [borg-manager](https://github.com/georgelacey/borg-manager). 

## Summary
Borg web consists of two components, a client 'borg-client' and [Django](https://www.djangoproject.com/) web server 'borgweb',
json output from borg create is piped to the client, which sends it to the web server.
If no json is output, an error is assumed, which is then logged.

## Features:
* Parses json output from 'borg create --json'
* Stores repo and archive information in database
* Logs errors
* Hosts repo summary page

## Notes
This is a project used by me to keep track of borg backups on a locally hosted server, for this reason it is not suitable for use by you unless you know what you're doing
