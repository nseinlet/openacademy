# -*- coding: utf-8 -*-
from odoo import models
from odoo.addons.base.populate.res_partner import Partner
from odoo.tools import populate

import names
import random

class Course(models.Model):
    _inherit = "openacademy.course"
    _populate_dependencies = ["res.users"]
    _populate_sizes = {"small": 100, "medium": 500, "large": 10000}

    def _populate_factories(self):
        user_ids = self.env.registry.populated_models["res.users"]

        def get_name(values=None, counter=0, **kwargs):
            return  '%s_%s' % ('course', counter)
        
        return [
            ("name", populate.compute(get_name)),
            ("responsible_id", populate.randomize(user_ids)),
        ]
    
class Session(models.Model):
    _inherit = "openacademy.session"
    _populate_dependencies = ["openacademy.course", "res.partner"]
    _populate_sizes = {"small": 1000, "medium": 5000, "large": 100000}

    def _populate_factories(self):
        partner_ids = self.env.registry.populated_models["res.partner"]
        course_ids = self.env.registry.populated_models["openacademy.course"]

        def get_name(values=None, counter=0, **kwargs):
            return  '%s_%s' % ('session', counter)
        
        def get_attendee_ids(values=None, counter=0, **kwargs):
            return [random.choice(partner_ids) for n in range(2, 20)]
        
        
        return [
            ("name", populate.compute(get_name)),
            ("course_id", populate.randomize(course_ids)),
            # ("instructor_id", populate.randomize(partner_ids)),
            ('seats', populate.randint(1, 100)),
            ('attendee_ids', populate.compute(get_attendee_ids)),
        ]
    
    def _populate(self, size):
        records = super()._populate(size)
        # set parent_ids
        self._populate_set_instructor(records)
        return records

    def _populate_set_instructor(self, records):
        for record in records:
            inst = record.attendee_ids[0]
            record.attendee_ids = record.attendee_ids[1:]
            record.instructor_id = inst
            if record.seats<len(record.attendee_ids):
                record.seats = len(record.attendee_ids)
