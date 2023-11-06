# -*- coding: utf-8 -*-
from OdooLocust import OdooLocustUser, crm

class OdooCom(OdooLocustUser.OdooLocustUser):
    host = "localhost"
    database = "16open"
    login = "admin"
    password = "admin"
    port = 8069
    protocol = "jsonrpc"

    tasks = {crm.partner.ResPartner: 1, crm.lead.CrmLead: 2}