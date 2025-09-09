#!/bin/bash
export ODOO_VER=19.0

echo $ODOO_VER
if [ ! -z "$1" ]
then
    export ODOO_VER=$1
fi
echo "Starting Odoo version $ODOO_VER"

/datas/progs/odoo/$ODOO_VER/odoo-bin --addons-path=/datas/progs/odoo/$ODOO_VER/addons,/datas/progs/odoo/$ODOO_VER/odoo/addons,/datas/progs/enterprise/$ODOO_VER/,/datas/progs/openacademy -d ${ODOO_VER}open --workers=1 --max-cron-threads=0 --limit-time-cpu=600 --limit-time-real=1200 --limit-memory-soft=2147483648 --limit-memory-hard=2147483648
