#!/bin/bash

consul watch -type=keyprefix -prefix={{ haproxy_consul_certs_prefix }} \
    consul lock {{ haproxy_consul_lock_prefix }} \
        'rm -f {{ haproxy_ocim_certs_dir}}/* && consul kv get -keys {{ haproxy_consul_certs_prefix }}/ | { read -r; while read -r key; do consul kv get "$key" > "{{ haproxy_ocim_certs_dir}}/${key##*/}"; done; } && flock -n -E 0 /tmp/haproxy-reload-lock service haproxy reload'
