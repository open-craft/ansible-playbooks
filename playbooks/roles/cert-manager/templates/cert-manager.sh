#!/bin/bash

# This script watches a Consul KV path that is used to detect whether we need
# to re-request certificates.

consul watch -type=keyprefix -prefix={{ cert_manager_consul_watch_prefix }} \
    consul lock {{ cert_manager_consul_lock_prefix }} \
        pipenv run python manage_certs.py {% if cert_manager_stage %}--letsencrypt-use-staging{% endif %} \
            --contact-email {{ cert_manager_email }} \
            --log-level {{ cert_manager_log_level }} \
            --webroot-path {{ cert_manager_webroot_path }} \
            --consul-ocim-prefix {{ cert_manager_consul_ocim_prefix }} \
            --consul-certs-prefix {{ cert_manager_consul_certs_prefix }}
