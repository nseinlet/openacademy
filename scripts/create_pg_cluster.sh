#!/bin/bash
# Drop existing clusters
sudo pg_dropcluster 18 odoo_secondary --stop
sudo rm -rf /etc/postgresql/18/odoo_secondary
sudo rm -rf /var/lib/postgresql/18/odoo_secondary
sudo pg_dropcluster 18 odoo_main --stop
sudo rm -rf /etc/postgresql/18/odoo_main
sudo rm -rf /var/lib/postgresql/18/odoo_main
#Create new clusters
sudo apt install postgresql-18 repmgr postgresql-18-repmgr
sudo pg_createcluster 18 odoo_main
sudo cp pg/main.conf /etc/postgresql/18/odoo_main/conf.d/
sudo pg_createcluster 18 odoo_secondary
sudo cp pg/secondary.conf /etc/postgresql/18/odoo_secondary/conf.d/
sudo pg_ctlcluster 18 odoo_main start
pg_lsclusters
sudo su - postgres -c "createuser -p 5441 nse -d -l -s -r"
sudo su - postgres -c "createuser -p 5441 barman_odoo -d -l -S"
psql -p 5441 -d postgres < pg/main.sql
#Create replication
repmgr -f pg/main_repmgr.conf primary  register
export PGPASSWORD=secret
pg_lsclusters
pgdir=$(pwd)
sudo su - postgres -c "export PGPASSWORD=secret && repmgr -h 127.0.0.1 -p 5441 -U repmgr -d  repmgr -f $pgdir/pg/secondary_repmgr.conf standby clone --force"
sudo pg_ctlcluster 18 odoo_secondary start
repmgr -f $pgdir/pg/secondary_repmgr.conf standby register
