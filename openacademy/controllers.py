# -*- coding: utf-8 -*-
from odoo import http

class Academy(http.Controller):
    @http.route('/academy/academy/', auth='public', website=True)
    def index(self, **kw):
        Teachers = http.request.env['res.partner']
        return http.request.render('openacademy.index', {
            'teachers': Teachers.search([('instructor', '=', True)])
        })
        
    @http.route('/academy/<model("res.partner"):teacher>/', auth='public', website=True)
    def teacher(self, teacher):
        return http.request.render('openacademy.biography', {
            'person': teacher
        })
        
