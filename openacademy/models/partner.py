# -*- coding: utf-8 -*-
from datetime import datetime

from odoo import fields, models, api


class Partner(models.Model):
    _inherit = 'res.partner'

    last_name = fields.Char()
    full_name = fields.Char(compute='_compute_full_name', store=True)
    full_name_inv = fields.Char(compute='_compute_full_name', store=False)
    uppercase_name = fields.Char(compute='_compute_uppercase_name', store=False)
    instructor = fields.Boolean("Instructor", default=False)
    biography = fields.Html()
    session_ids = fields.Many2many('openacademy.session',
        string="Attended Sessions", readonly=True)
    next_session_ids = fields.Many2many('openacademy.session',
        string="Five next Sessions", readonly=True, compute='_compute_next_session_ids')
    full_session_count = fields.Many2many('openacademy.session',
        string="Full Sessions", readonly=True, compute='_compute_full_session_ids')
    
    @api.depends('session_ids')
    def _compute_next_session_ids(self):
        for partner in self:
            partner.next_session_ids = self.env['openacademy.session'].search([('is_participant', '=', True), ('start_date', '>', datetime.now())], limit=5, order='start_date desc')
        
    @api.depends('session_ids')
    def _compute_full_session_ids(self):
        for partner in self:
            partner.full_session_count = self.env['openacademy.session'].search_count([('is_participant', '=', True), ('taken_seats', '=', 100.0)])

    @api.depends('name', 'last_name')
    def _compute_full_name(self):
        for partner in self:
            partner.full_name = partner.name + ' ' + (partner.last_name or '')
            partner.full_name_inv = (partner.last_name or '') + ' ' + partner.name
    
    @api.depends('name', 'last_name')
    def _compute_uppercase_name(self):
        for i in range(0, len(self)):
            self[i].uppercase_name = (' '.join([self[i].name, self[i].last_name])).upper()