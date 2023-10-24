# -*- coding: utf-8 -*-
from datetime import timedelta

from odoo import models, fields, api, exceptions, _
    
class Session(models.Model):
    _name = 'openacademy.session'
    _order = 'course_id, instructor_id, start_date desc, id'

    name = fields.Char(required=True)
    start_date = fields.Date(default=fields.Date.today)
    duration = fields.Float(digits=(6, 2), help="Duration in days")
    seats = fields.Integer(string="Number of seats")
    active = fields.Boolean(default=True)
    color = fields.Integer()
    instructor_id = fields.Many2one('res.partner', string="Instructor",
        domain=['|', ('instructor', '=', True),
                     ('category_id.name', 'ilike', "Teacher")])
    course_id = fields.Many2one('openacademy.course',
        ondelete='cascade', string="Course", required=True)
    attendee_ids = fields.Many2many('res.partner', string="Attendees")
    taken_seats = fields.Float(string="Taken seats", compute='_taken_seats')
    end_date = fields.Date(string="End Date", store=True,
        compute='_get_end_date', inverse='_set_end_date')
    hours = fields.Float(string="Duration in hours",
                         compute='_get_hours', inverse='_set_hours')
    attendees_count = fields.Integer(
        string="Attendees count", compute='_get_attendees_count', store=True)
    state = fields.Selection([
         ('draft', "Draft"),
         ('confirmed', "Confirmed"),
         ('done', "Done"),
        ],
        default='draft')
    is_participant = fields.Boolean(compute='_compute_is_participant', search='_search_is_participant')
    average_participation_rate = fields.Float(compute='_compute_average_participation_rate')
    same_instructor_count = fields.Integer(compute='_compute_same_instructor_count')

    def action_draft(self):
        for rec in self:
            rec.state = 'draft'

    def action_confirm(self):
        for rec in self:
            rec.state = 'confirmed'

    def action_done(self):
        for rec in self:
            rec.state = 'done'
        
    @api.depends('seats', 'attendee_ids')
    def _taken_seats(self):
        for rec in self:
            if not rec.seats:
                rec.taken_seats = 0.0
            else:
                rec.taken_seats = 100.0 * len(rec.attendee_ids) / rec.seats

    @api.onchange('seats', 'attendee_ids')
    def _verify_valid_seats(self):
        if self.seats < 0:
            return {
                'warning': {
                    'title': "Incorrect 'seats' value",
                    'message': "The number of available seats may not be negative",
                },
            }
        if self.seats < len(self.attendee_ids):
            return {
                'warning': {
                    'title': _("Too many attendees"),
                    'message': _("Increase seats or remove excess attendees"),
                },
            }

    @api.depends('start_date', 'duration')
    def _get_end_date(self):
        for rec in self:
            if not (rec.start_date and rec.duration):
                rec.end_date = rec.start_date
                continue

            # Add duration to start_date, but: Monday + 5 days = Saturday, so
            # subtract one second to get on Friday instead
            start = fields.Datetime.from_string(rec.start_date)
            duration = timedelta(days=rec.duration, seconds=-1)
            rec.end_date = start + duration

    def _set_end_date(self):
        for rec in self:
            if not (rec.start_date and rec.end_date):
                continue

            # Compute the difference between dates, but: Friday - Monday = 4 days,
            # so add one day to get 5 days instead
            start_date = fields.Datetime.from_string(rec.start_date)
            end_date = fields.Datetime.from_string(rec.end_date)
            rec.duration = (end_date - start_date).days + 1
        
    @api.depends('duration')
    def _get_hours(self):
        for rec in self:
            rec.hours = rec.duration * 24

    def _set_hours(self):
        for rec in self:
            rec.duration = rec.hours / 24
        
    @api.depends('attendee_ids')
    def _get_attendees_count(self):
        for rec in self:
            rec.attendees_count = len(rec.attendee_ids)
        
    @api.constrains('instructor_id', 'attendee_ids')
    def _check_instructor_not_in_attendees(self):
        for rec in self:
            if rec.instructor_id and rec.instructor_id in rec.attendee_ids:
                raise exceptions.ValidationError(_("A session's instructor can't be an attendee"))
            
    def write(self, vals):
        res = super(Session, self).write(vals)
        for rec in self:
            if rec.taken_seats > 50 and rec.state == 'draft':
                rec.state = 'confirmed'
        return res
    
    @api.depends('attendee_ids')
    def _compute_is_participant(self):
        for rec in self:
            rec.is_participant = False
        if self.ids:
            self.env.flush_all()
            self.env.cr.execute(
                """
                SELECT openacademy_session_id FROM openacademy_session_res_partner_rel WHERE openacademy_session_id IN %s AND res_partner_id = %s
                """,
                (tuple(self.ids), self.env.user.partner_id.id)
            )
            sess_ids = [rec.session_id for rec in self.env.cr.fetchall()]
            for rec in self:
                rec.is_participant = rec.id in sess_ids

    def _search_is_participant(self, operator, value):
        self.env.flush_all()
        query = """
            SELECT s.id
              FROM openacademy_session s
                  ,openacademy_session_res_partner_rel rel
                  ,res_partner p
             WHERE rel.openacademy_session_id = s.id
               AND p.id = rel.res_partner_id 
               AND p.id
            """
        if (operator == '=' and value) or (operator == '!=' and not value):
            query += " = %s"
        else:
            query += " != %s"
        self.env.cr.execute(
            query,
            (self.env.user.partner_id.id,)
        )
        sess_ids = [rec[0] for rec in self.env.cr.fetchall()]
        return [('id', 'in', sess_ids)]
        
    @api.depends('attendee_ids')
    def _compute_average_participation_rate(self):
        for rec in self:
            res = 0
            if len(rec.attendee_ids) == 0:
                rec.average_participation_rate = 0
                continue
            for att in rec.attendee_ids:
                res += self.env['openacademy.session'].search_count([('attendee_ids', '=', att.id)])
            rec.average_participation_rate = res / len(rec.attendee_ids)

    @api.depends('instructor_id')
    def _compute_same_instructor_count(self):
        for rec in self:
            rec.same_instructor_count = self.search_count([('instructor_id', '=', rec.instructor_id.id)])
