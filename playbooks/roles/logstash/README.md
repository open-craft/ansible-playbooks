Logstash
========

A role to install and configure a TLS-enabled Logstash service.

Expects input beats to provide TLS details from a common certificate authority.

Requirements
------------

N/A

Role Variables
--------------

See `defaults/main.yml`.

Dependencies
------------

N/A

Example Playbook
----------------

    - hosts: all
      roles:
         - logstash
