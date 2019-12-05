## Adding certs

1. Encrypt them. `ansible-vault encrypt clients.new.cert.pem` Use the [right password](https://vault.opencraft.com:8200/ui/vault/secrets/secret/show/core/Ansible%20Vault).
1. Encode the filename. `echo -n "clients.new.cert" | base64`
1. Rename the file. Ensure no "/"s in the filename. Ensure file ends with `.pem`
1. Run the playbook. `ansible-playbook -v deploy/playbooks/load-balancer-v2.yml -l haproxy-<...>.net.opencraft.hosting`