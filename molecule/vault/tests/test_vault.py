def test_vault(host):
    cmd = host.run("bash -c 'PS1=yes ; source /root/.bashrc ; vault status'")
    print(cmd.stdout)
    print(cmd.stderr)
    assert 'Initialized     true' in cmd.stdout
    assert cmd.rc == 0
