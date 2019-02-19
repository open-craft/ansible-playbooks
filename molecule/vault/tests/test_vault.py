import json

testinfra_hosts = ['vault-host']

def test_vault_deploy(host):
    cmd = host.run(". /home/ubuntu/.vault-env ; vault status --format json")
    print(cmd.stdout)
    print(cmd.stderr)
    assert json.loads(cmd.stdout)['initialized'] is True
    assert cmd.rc == 0


def test_vault_ssh_signer(host):
    cmd = host.run("""
    set -ex
    . /home/ubuntu/.vault-env
    export VAULT_TOKEN=testtoken
    vault secrets list | grep '^ssh-signer-backup-pruner/'
    vault read ssh-signer-backup-pruner/config/ca
    """)
    print(cmd.stdout)
    print(cmd.stderr)
    assert cmd.rc == 0


def test_vault_ssh_client(host):
    cmd = host.run("""
    set -ex
    . /home/ubuntu/.vault-env
    export VAULT_TOKEN=testtoken
    vault write -field=signed_key ssh-signer-backup-pruner/sign/core public_key=@/etc/ssh/ssh_host_rsa_key.pub > /tmp/signed.pub
    chmod 600 /tmp/signed.pub
    ssh -oStrictHostKeyChecking=no -i /tmp/signed.pub -i /etc/ssh/ssh_host_rsa_key ubuntu@backup-pruner true
    """)
    print(cmd.stdout)
    print(cmd.stderr)
    assert cmd.rc == 0
