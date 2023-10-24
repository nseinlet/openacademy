# -*- coding: utf-8 -*-
from datetime import timedelta

from odoo import models, fields, api, _
from odoo.tools import populate


class Course(models.Model):
    _name = 'openacademy.course'
    _populate_sizes = {"small": 100, "medium": 2000, "large": 10000}
    _populate_dependencies = ["custom.some_other_model"]

    name = fields.Char(string="Title", required=True)
    description = fields.Text()
    responsible_id = fields.Many2one('res.users',
        ondelete='set null', string="Responsible", index=True)
    session_ids = fields.One2many(
        'openacademy.session', 'course_id', string="Sessions")
    session_count = fields.Integer(compute='_compute_session_stats', store=True, compute_sudo=False)
    session_filled_seats = fields.Float(compute='_compute_session_stats', compute_sudo=False)
    attended = fields.Boolean(compute='_compute_attended', search='_search_attended')
    
    def copy(self, default=None):
        default = dict(default or {})

        copied_count = self.search_count(
            [('name', '=like', _(u"Copy of {}%").format(self.name))])
        if not copied_count:
            new_name = _(u"Copy of {}").format(self.name)
        else:
            new_name = _(u"Copy of {} ({})").format(self.name, copied_count)

        default['name'] = new_name
        return super(Course, self).copy(default)
    
    @api.depends('session_ids')
    def _compute_session_stats(self):
        for course in self:
            course.session_count = len(course.session_ids)
            course.session_filled_seats = sum(course.session_ids.mapped('taken_seats')) / course.session_count if course.session_count else 0.0

    @api.depends('session_ids.attendee_ids')
    def _compute_attended(self):
        for course in self:
            course.attended = any(course.session_ids.mapped('is_participant'))

    def _search_attended(self, operator, value):
        return [('session_ids.is_participant', operator, value)]
    
    def _populate_factories(self):
        # Record ids of previously populated models are accessible in the registry
        some_other_ids = self.env.registry.populated_models["custom.some_other_model"]

        def get_some_field(values=None, random=None, **kwargs):
            """ Choose a value for some_field depending on other fields values.

            :param dict values:
            :param random: seeded :class:`random.Random` object
            """
            field_1 = values['field_1']
            if field_1 in [value2, value3]:
                return random.choice(some_field_values)
            return False

        return [
            ("field_1", populate.randomize([value1, value2, value3])),
            ("field_2", populate.randomize([value_a, value_b], [0.5, 0.5])),
            ("some_other_id", populate.randomize(some_other_ids)),
            ("some_field", populate.compute(get_some_field, seed="some_field")),
            ('active', populate.cartesian([True, False])),
        ]
        
    _sql_constraints = [
        ('name_description_check',
         'CHECK(name != description)',
         "The title of the course should not be the description"),

        ('name_unique',
         'UNIQUE(name)',
         "The course title must be unique"),
    ]
    