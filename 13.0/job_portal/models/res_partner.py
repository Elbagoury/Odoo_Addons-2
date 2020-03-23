# -*- coding: utf-8 -*-
# See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class ResPartnerPortal(models.Model):
    """This class is defined to enhance ResUsers Class to enhance portal."""

    _inherit = 'res.partner'

    middlename = fields.Char('Middle Name')
    lastname = fields.Char('Last Name')
    academic_ids = fields.One2many('hr.academic', 'partner_id',
                                   'Academic experiences',
                                   help="Academic experiences")
    experience_ids = fields.One2many('hr.experience', 'partner_id',
                                     ' Professional Experiences',
                                     help='Professional Experiences')
    certification_ids = fields.One2many('hr.certification', 'partner_id',
                                        'Certifications',
                                        help="Certifications")

    def write(self, values):
        reserved_fields = ['contact_referee', 'position_referee', 'location', 'start_date', 'end_date',
                           'job_position', 'organization', 'opr_id', 'tr_no', 'is_still', 'study_field', 'name_referee',
                           'grade', 'description', 'certification', 'operation_type', 'qualification']
        for reserved_field in reserved_fields:
            if values.get(reserved_field) or values.get(reserved_field) == '':
                del values[reserved_field]
        res = super(ResPartnerPortal, self).write(values)
        return res
