Sanity check
============

A role that performs basic health checks for your instance and if they fail sends you an email, optionally 
if they pass it will notify Dead Man's snitch.

Example configuration:

    SANITY_CHECK_DISK_SPACE_PERCENTAGE: 20
    
    SANITY_CHECK_LIVE_PORTS:
      - host: localhost
        port: 80
        message: "Oh no! Http is down"
      - host: localhost
        port: 443
        message: "Oh no! Https is down"
    
    # If any of these return non-zero exit code whole check will fail
    SANITY_CHECK_COMMANDS:
      - command: echo 1
        message: "Echo broke, we are doomed!"
