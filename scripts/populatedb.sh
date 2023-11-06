#!/bin/bash
dropdb 16open
./odoo-bin --addons-path=./addons,./odoo/addons,../../enterprise/16.0/,/datas/progs/openacademy -d 16open -i openacademy --stop-after-init
./odoo-bin populate --size=medium --addons-path=./addons,./odoo/addons,../../enterprise/16.0/,/datas/progs/openacademy -d 16open
