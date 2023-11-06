# -*- coding: utf-8 -*-
import odoolib

connection = odoolib.get_connection(
    hostname="localhost",
    database="16oa",
    login="admin",
    password="admin")
partner_model = connection.get_model("res.partner")
ids = partner_model.search([])
prtn_info = partner_model.read(ids[0], ["name"])

print(prtn_info["name"])