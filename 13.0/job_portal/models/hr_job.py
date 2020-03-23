# -*- coding: utf-8 -*-
# See LICENSE file for full copyright and licensing details.

from odoo import fields, models, api
from datetime import *
from odoo.exceptions import ValidationError


class HrJobType(models.Model):
    _name = "hr.job.type"

    name = fields.Char('Job Type')


class HrJob(models.Model):
    _inherit = 'hr.job'

    benefits_ids = fields.One2many('hr.job.benefits', 'job_benefits_id',
                                   string='Benefits')
    job_requirement_ids = fields.One2many('hr.job.requirement',
                                          'job_requirement_id',
                                          string='Requirements')
    job_by_area = fields.Char('Jobs by Functional Area')
    closing_date = fields.Date('Closing Date')
    notify_email = fields.Char('Application Notify Email')
    location_ids = fields.One2many('hr.job.location', 'job_location_id',
                                   string='Location')
    job_type_id = fields.Many2one('hr.job.type', string='Job Type')

    @api.model
    def create(self, vals):
        result = super(HrJob, self).create(vals)
        if not self.env.context.get('website_id'):
            try:
                closing_date = datetime.strptime(vals['closing_date'], "%Y-%m-%d").date()
                today = date.today()

                if today > closing_date:
                    raise ValidationError("Please enter proper closing date")
            except:
                pass

        try:
            return result
        except:
            raise ValidationError("Please Enter Fields Properly!")

    def write(self, vals):
        result = super(HrJob, self).write(vals)
        if not self.env.context.get('website_id'):
            if vals.get('closing_date'):
                closing_date = datetime.strptime(vals.get('closing_date'), "%Y-%m-%d").date()
                today = date.today()

                if today > closing_date:
                    raise ValidationError("Please enter proper closing date")
        try:
            return result
        except:
            raise ValidationError("Please Enter Fields Properly!")


class HrJobBenefits(models.Model):
    _name = "hr.job.benefits"

    name = fields.Char('Benefit')
    job_benefits_id = fields.Many2one('hr.job', string="Job")


class HrJobRequirement(models.Model):
    _name = "hr.job.requirement"

    name = fields.Char('Requirement')
    job_requirement_id = fields.Many2one('hr.job', string="Job")


class HrJobLocation(models.Model):
    _name = "hr.job.location"

    name = fields.Char('Location')
    job_location_id = fields.Many2one('hr.job', string="Job")
