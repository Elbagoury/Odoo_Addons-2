# -*- coding: utf-8 -*-
# See LICENSE file for full copyright and licensing details.

from datetime import *
from odoo import api, fields, models
from odoo.exceptions import ValidationError


class HrCertification(models.Model):
    _name = 'hr.certification'
    _inherit = 'hr.curriculum'

    certification = fields.Char(string='Certification Number',
                                help='Certification Number')

    @api.constrains('start_date', 'end_date')
    def validate_dates(self):
        if not self.env.context.get('website_id'):
            if self.end_date:
                today = date.today()

                for dates in self:
                    s_date = datetime.strptime(str(dates.start_date), '%Y-%m-%d').date()
                    e_date = datetime.strptime(str(dates.end_date), '%Y-%m-%d').date()
                    if s_date > today:
                        raise ValidationError("Start date should be "
                                              "less than today "
                                              "in details!")
                    if e_date > today:
                        raise ValidationError("End date should be less "
                                              "than start"
                                              " date in details!")
                    if s_date > e_date:
                        raise ValidationError("End date should be greater"
                                              " than"
                                              " start date in details!")

    def write(self, vals):
        if vals.get("is_still"):
            vals.update({'end_date': None})
        result = super(HrCertification, self).write(vals)

        return result
