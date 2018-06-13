# Ansible Role for Nomad

Used for deploying Nomad server and clients, depending on the `nomad_server` or `nomad_client` variable being set.

## Requirements

N/A

## Role Variables

See `defaults/main.yml`.

## Dependencies

None.

## Example Playbook

Including an example of how to use your role (for instance, with variables passed in as parameters) is always nice for users too:

    - hosts: nomad-servers
      roles:
        - role: nomad
          nomad_server: true

    - hosts: nomad-clients
      roles:
        - role: nomad
          nomad_client: true

## License

AGPLv3
