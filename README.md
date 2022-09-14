# Ansible Playbooks & Roles

This repository contains all OpenCraft playbooks and roles used to deploy many different types of servers.

## Submodules

We have several submodules defined in `.gitmodules` -- they're all either 3rd party roles, or those with CircleCI builds that run on their repositories separately.

If you need to update a submodule in this repository to point to a new commit hash, `cd` into it and `git checkout` that reference. You can then stage and commit those changes.

**WARNING: ansible-playbook will silently skip tasks in the roles defined as submodules if the submodules haven't been checked out!**
Be sure to run `git submodule update --init --recursive` to initialize the submodules.

For our own roles that are in this repository as submodules, they should be on the latest `master`. You can update them with `git submodule update --remote`.

## How to deploy or redeploy a load-balancing server

### Create an OpenStack instance if needed

1. Create a SoYouStart dedicated server (for production) or a OVH VM (for staging -- use the infrastructure map to find the correct region and account). This will be a vanilla Ubuntu image 16.04 or greater.

1. Add the host name of the new instance to the Ansible inventory in the file `hosts`:

        [load-balancer-v2-prod]
        load-balancer.host.name

1. Update the infrastructure map

1. Bootstrap the server. This means running the `bootstrap-dedicated.yml` playbook:

        ansible-playbook bootstrap-dedicated.yml -u ubuntu -l load-balancer.host.name

### Generate secrets for the new server

1. Go to https://deadmanssnitch.com/ and create two snitches, one for the
   backups and one for the sanity checks.  Add them to a file
   `host_vars/<hostname>/vars.yml`:

        TARSNAP_BACKUP_SNITCH: https://nosnch.in/<backup-snitch>
        SANITY_CHECK_SNITCH: https://nosnch.in/<sanity-check-snitch>

1. Generate a tarsnap master key and a subkey with only read and write
   permissions, and add it to the variables file:

        TARSNAP_KEY: |
          # START OF TARSNAP KEY FILE
          [...]
          # END OF TARSNAP KEY FILE

### Perform the deployment

For a new server, run these commands:

```
mkvirtualenv ansible
pip install -r requirements.txt
ansible-playbook deploy-all.yml -u ubuntu -l load-balancer.host.name
```

Then you will need to instruct the new server to join the Consul cluster and add the new load balancer to the DNS pool in Gandi. See the [load balancer](https://gitlab.com/opencraft/documentation/private/blob/master/ops/loadbalancing.md) documentation for details.

For an existing server, run these commands:

```
mkvirtualenv ansible
pip install -r requirements.txt
ansible-playbook -v deploy/playbooks/load-balancer-v2.yml -l load-balancer.host.name
```

**ALWAYS** use `--limit` and test each server after deployment, even if you have to make the same updates to all three. That's the whole point of having 3 highly available load balancers!

## How to deploy an ElasticSearch server

### Create an OpenStack instance

1. Create an OpenStack "vps-ssd-2" instance from a vanilla Ubuntu 16.04 (xenial)
   image.

1. Add the IP address and host name of the new instance to the Ansible inventory
   in the file `hosts` (create it if necessary):

        [elasticsearch]
        elasticsearch.host.name

### Generate secrets for the new server

1. Go to https://deadmanssnitch.com/ and create one snitch for the sanity checks.
   Add it to a file `host_vars/<hostname>/vars.yml`:

        SANITY_CHECK_SNITCH: https://nosnch.in/<sanity-check-snitch>

### Perform the deployment

Run these commands:

    mkvirtualenv ansible
    pip install -r requirements.txt
    ansible-playbook deploy-all.yml -u ubuntu -l elasticsearch

## Tarsnapper pruner server

Deploys a high-security server, has full access to most our tarsnapper backups.
This server is used only to delete old backups.

### How to deploy

`ansible-playbook deploy/deploy-all.yml -u ubuntu --extra-vars @private-extra-vars.yml -i hosts --private-key /path/to/backup_pruner.key`

### How to add new backup to be pruned

1. Get master key
1. Save master key to private.yml
1. Save cache directory and file for tarsnap key in the private yaml
1. Add new entry to `TARSNAPPER_JOBS`

### How to prune backups for individual servers

1. Login to the instance
1. Pruning scripts are named `tarsnap-{{ job.name }}.sh`
1. Following operations are supported:
   a. List archives `sudo tarsnap-{{ job.name }}.sh list`
   b. Expire archives `sudo tarsnap-{{ job.name }}.sh. expire`
   c. Expire archives (dry run) `tarsnap-{{ job.name }}.sh expire --dry-run`

## Deploy new MySQL database

This ansible repository deploys MySQL server on OpenStack provider.

### Create an OpenStack environment

1. Create a volume for data, as big as you need. It should be empty.
1. Create a security group for database servers. It should have following rules:
    1. Incoming traffic is allowed only for port 22.
    1. Outgoing traffic should be allowed.
    1. When you provision servers using the database allow them using their IP.
1. Create an instance using an appropriate image, such as Ubuntu 16.04. We suggest you use vanilla image from
   [ubuntu page](https://cloud-images.ubuntu.com/). This image might be small; MySQL
   data will be stored elsewhere.
1. Attach the data volume that you created earlier to the VM (go to `Volumes` -> data volume -> expand dropdown next to "Edit Volume" ->
   `Edit Attachments`).
1. Go to info page and note the instance public key, ssh to the instance and check whether public key matches,
   save public key to your ssh config.

### Generate secrets

1. Create `private-extra-vars.yml`, you'll put all the generated variables there
1. Generate root password, put it in the `private.yaml` for your host, under `mysql_root_password`.
1. Create a key, but store it somewhere safe (for example keepassx database), this key shouldn't end on the mysql server.
1. Generate tarsnap read write key from the master key, see [tarsnap-keymngmt](http://www.tarsnap.com/man-tarsnap-keymgmt.1.html),
   save this key in `MYSQL_TARSNAP_KEY`. **Note**: this key won't be able to delete the backups.
1. Go to dead man's snitch at https://deadmanssnitch.com/. Save it under `TARSNAP_BACKUP_SNITCH` in the `private.yml`.

### Perform deployment

    ansible-playbook deploy-all.yml -u ubuntu --extra-vars @private-extra-vars.yml

### Post deployment checkups

1. Check that backups are saved to tarsnap
1. Check contents of these backups.

### Run molecule tests

1. pip install -r test-requirements.txt
1. molecule test -s vault
