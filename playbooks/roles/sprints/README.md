Ansible role for deploying Sprints
============================================================

This role deploys [the application for sprint management][1].

It sets up standard server, installs Docker and docker-compose with `docker-compose` role
and deploys the application with docker-compose.

## Setup
The `.env` file, used by docker-compose is generated from `CUSTOM_ENV_TOKENS`.
Please set variables with `set-me-please` (and others, according to your needs) before performing the deployment.
The environment variables are described [here][2].

## TODO
- The way of obtaining Let's encrypt certificate by `common-server` role is handled in a hacky way here.
  We're stopping the Docker containers that are occupying port 80 and 443 to retrieve the certificate.
  It might be good to set up server-side proxy pointing to the locally-used Docker ports.
  We should also remember here that Let's Encrypt is set up in Docker with Traefik at the moment.
- Set up `traefik-exporter` or find another way of exporting service metrics. 

[1]: https://github.com/open-craft/sprints
[2]: https://github.com/open-craft/sprints/blob/master/config/settings/base.py
