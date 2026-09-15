#! /bin/bash
pg_dump -h {{ main_srv }} -d beamz -U barman_odoo -Fc -Z zstd:16 > /home/barman/dumps/$(date +%Y-%m-%d).dump
barman backup odoo-main
# Clear dumps older than 2 months, except the ones for mondays
find /home/barman/dumps/ -maxdepth 1 -type f -mtime +60 -exec sh -c 'day=$(date -r "$1" +%a); [ "$day" != "Mon" ] && echo "$1"' _ {} \; | xargs -n1 -r rm /home/barman/dumps/{}
