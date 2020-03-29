from odoo import models, fields, api
import re


class Telephone(models.Model):
    _inherit = "res.partner"

    phone_field_sanitized = fields.Char(string="Telephone Sanitized", required=False, compute="_compute_telephone_field", store=True)
    mobile_field_sanitized = fields.Char(string="Mobile Sanitized", required=False, compute="_compute_mobile_field", store=True)

    # this runs whenever a new contact is created or edited
    # api.depends is needed when using store=True, depends also functions a bit like onchange.
    @api.depends('phone')
    def _compute_telephone_field(self):
        for record in self:
            if (record.phone is not False) and record.phone.strip():
                record.phone_field_sanitized = re.sub('[^0-9]', '', record.phone)
            else:
                record.phone_field_sanitized = ''

    @api.depends('mobile')
    def _compute_mobile_field(self):
        for record in self:
            if (record.mobile is not False) and record.mobile.strip():
                record.mobile_field_sanitized = re.sub('[^0-9]', '', record.mobile)
            else:
                record.mobile_field_sanitized = ''

    # This runs at the install time of the module.
    def init(self):
        recs = self.env['res.partner'].search([])
        for rec in recs:
            if (rec.phone is not False) and rec.phone.strip():
                rec.phone_field_sanitized = re.sub('[^0-9]', '', rec.phone)
            else:
                rec.phone_field_sanitized = ''
            if (rec.mobile is not False) and rec.mobile.strip():
                rec.mobile_field_sanitized = re.sub('[^0-9]', '', rec.mobile)
            else:
                rec.mobile_field_sanitized = ''
