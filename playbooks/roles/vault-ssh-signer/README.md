# Ansible Role to create Vault SSH Certificates

Create a [Vault SSH Certificate](https://www.vaultproject.io/docs/secrets/ssh/signed-ssh-certificates.html)
named `ssh-signer-{{ vault_ssh_signer_ca }}` and the `core` role.

    roles:
      - role: vault-ssh-signer
        vars:
          vault_ssh_signer_ca: backup-pruner

It can then be used to sign ssh public keys with:

    vault write -field=signed_key \
          ssh-signer-backup-pruner/sign/core \
          public_key=@$HOME/.ssh/id_rsa.pub > signed.pub
