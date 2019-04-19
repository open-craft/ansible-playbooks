#!/usr/bin/env bash
PATH=/usr/bin:/bin:/usr/sbin
a2ensite 000-default.conf
service apache2 reload
certbot renew
a2dissite 000-default.conf
service apache2 reload
