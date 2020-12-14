# Ansible Role: Elasticsearch

An Ansible Role that installs Elasticsearch on Debian/Ubuntu.

## Important
If Elasticsearch is already installed in a server then ``Set bootstrap password`` will do nothing. But this is required to set up passwords for other build-in users like ``kibana_system``.

Therefore you need to create a new superuser in elasticsearch. Run the following command to add a new superuser -
```
/usr/share/elasticsearch/bin/elasticsearch-users useradd <USERNAME> -p <PASSWORD> -r superuserr
```

Then to change the password for ``kibana_system`` user following curl request -
```
curl -k -v https://127.0.0.1:9200/_security/user/kibana_system/_password -X POST -d '{"password": "<kibana_elasticsearch_password>"}' -H 'Content-Type: application/json' -u <SUPER-USER>:<SUPER-USER-PASSWORD>
```
You will find ``kibana_elasticsearch_password`` in the ansible secrets repository.

Replace ``<SUPER-USER>`` and ``<SUPER-USER-PASSWORD>`` with newly created super user's ``username`` and ``password`` accordingly.

## Role Variables

Available variables are listed below, along with default values (see `defaults/main.yml`):

    elasticsearch_network_host: localhost

Network host to listen for incoming connections on. By default we only listen on the localhost interface. Change this to the IP address to listen on a specific interface, or `0.0.0.0` to listen on all interfaces.

    elasticsearch_http_port: 9200

The port to listen for HTTP connections on.

    elasticsearch_script_inline: true
    elasticsearch_script_indexed: true

Whether to allow inline scripting against ElasticSearch. You should read the following link as there are possible security implications for enabling these options: [Enable Dynamic Scripting](https://www.elastic.co/guide/en/elasticsearch/reference/current/modules-scripting.html#enable-dynamic-scripting). Available options include: `true`, `false`, and `sandbox`.

## Example Playbook

    - hosts: search
      roles:
        - elasticsearch

## License

MIT / BSD

## Author Information

This role was created in 2014 by [Jeff Geerling](http://www.jeffgeerling.com/), author of [Ansible for DevOps](https://www.ansiblefordevops.com/).

It has been modified and adapted by and for OpenCraft.
