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
