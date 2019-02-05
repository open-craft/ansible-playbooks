Kibana
======

A role to install Kibana which allows us to view logs stored in Elasticsearch.

Requirements
------------

N/A

Role Variables
--------------

See `defaults/main.yml`.

Dependencies
------------

See `meta/main.yml`.

Example Playbook
----------------

    - hosts: all
      roles:
         - kibana
