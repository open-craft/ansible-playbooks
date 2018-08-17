#!/usr/bin/env bash
a2ensite 000-default.conf
service apache2 reload
certbot renew
a2dissite 000-default.conf
service apache2 reload