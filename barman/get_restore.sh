#! /bin/bash
rm -rf /home/barman/odoo-restore
barman recover odoo-main latest /home/barman/odoo-restore/ --no-get-wal
tar -zcvf /home/barman/odoo-restore_$(date +%Y%m%d_%H%M%S).tar.gz odoo-restore
rm -rf /home/barman/odoo-restore
