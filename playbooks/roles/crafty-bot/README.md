# Ansible role for deploying Crafty Bot

This role deploys [the application][1] for sprint planning checklist automation.

It sets up standard server, installs Docker and docker-compose with 
`docker-compose` role and deploys the application with docker-compose.

## Setup

The `.env` file, used by docker-compose is generated from `CUSTOM_ENV_TOKENS`.
Please set variables with `set-me-please` (and others, according to your needs)
before performing the deployment.

The environment variables are described [here][2].

## About deployment

The [repository][1] does not contain the `docker-compose.yml` and `deploy.sh`
files, to reduce the double-bookeeping.

### Disk space usage

If you are planning to deploy this on an instance with its root partition size
of total 10GB (or less), you should consider moving the Docker data to an
external volume, because overlay2 takes a significant amount of space
in such case. To do this on an existing instance, use the following approach:

1. Create new volume (e.g. with 40GB).
2. Add new volume to `/etc/fstab` and mount it.
3. Copy Docker data to the new volume (we are using `/mnt/volume` in this example):

   ```bash
   systemctl stop docker.service

   echo -e '{\n    "graph": "/mnt/volume/docker\n}' > /etc/docker/daemon.json

   rsync -a --sparse --progress /var/lib/docker /mnt/volume/
   mv /var/lib/docker /var/lib/docker_old  # Backup (just in case).

   systemctl start docker.service  # Ensure that everything works correctly now.

   rm -r /var/lib/docker  # Remove backup.
   ```

[1]: https://gitlab.com/opencraft/dev/crafty-bot
[2]: https://gitlab.com/opencraft/dev/crafty-bot/-/blob/master/config/settings/base.py