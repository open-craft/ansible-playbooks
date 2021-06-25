# Mail server + Mailman 3

Ansible role for a mail server with a Mailman 3 mailing list.

See [./defaults/main.yml](./defaults/main.yml) for documentation of used variables.

Only tested on Ubuntu 18.04 LTS.

All postfix configuration is controlled via templated files in this role,
with no mysql configuration.
So postfix is fully defined by this ansible role.

Mailman3 is also fully configured by this role.
However, user accounts and mailing list configuration are configured manually by either Postorius or `mailman shell`.
This configuration is stored in the postgres database defined by the `MAILMAN_POSTGRES_*` variables.
