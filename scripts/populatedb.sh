#!/bin/bash
export ODOO_VER=20.0

echo $ODOO_VER
if [ ! -z "$1" ]
then
    export ODOO_VER=$1
fi
echo "Populating Odoo version $ODOO_VER"

dropdb ${ODOO_VER}open -p 5441
/datas/progs/odoo/$ODOO_VER/odoo-bin --addons-path=/datas/progs/odoo/$ODOO_VER/addons,/datas/progs/odoo/$ODOO_VER/odoo/addons,/datas/progs/enterprise/$ODOO_VER/,/datas/progs/openacademy -d ${ODOO_VER}open --db_port=5441 -i openacademy,populate --stop-after-init
/datas/progs/odoo/$ODOO_VER/odoo-bin populate  --addons-path=/datas/progs/odoo/$ODOO_VER/addons,/datas/progs/odoo/$ODOO_VER/odoo/addons,/datas/progs/enterprise/$ODOO_VER/,/datas/progs/openacademy -d ${ODOO_VER}open --db_port=5441 --scale=2 -b somecourses
