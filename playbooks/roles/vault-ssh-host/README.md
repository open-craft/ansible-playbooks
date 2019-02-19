# Ansible Role to install Vault SSH Certificates

Fetch the {{ vault_ssh_signer_ca }} [Vault SSH
Certificate](https://www.vaultproject.io/docs/secrets/ssh/signed-ssh-certificates.html)
from {{ vault_host }} and install it as a `TrustedUserCAKeys` in the
SSH server configuration /etc/ssh/sshd_config.

    roles:
      - role: vault-ssh-host
        vars:
          vault_ssh_signer_ca: backup-pruner

A public ssh key signed by the Vault signer will be granted access.


    $ vault write -field=signed_key \
          ssh-signer-backup-pruner/sign/core \
          public_key=@$HOME/.ssh/id_rsa.pub > signed.pub
    $ ssh -i signed.pub ubuntu@backup-pruner.opencraft.com
