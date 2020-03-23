# -*- coding: utf-8 -*-
# See LICENSE file for full copyright and licensing details.

from odoo import fields, models, api
from odoo.exceptions import ValidationError
from datetime import *
from odoo.exceptions import UserError
from odoo.tools.translate import _


class HrApplicant(models.Model):
    _inherit = 'hr.applicant'

    middlename = fields.Char('Middle Name')
    lastname = fields.Char('Last Name')
    gender = fields.Selection([('male', 'Male'), ('female', 'Female')],
                              string="Gender")
    birthday = fields.Date('Date of Birth')
    place_of_birth = fields.Char('Place of Birth')
    country_of_birth_lt = fields.Many2one('res.country')
    marital = fields.Selection(
        [('single', 'Single'), ('married', 'Married'), ('widower', 'Widower'),
         ('divorced', 'Divorced')],
        'Marital Status')
    #   Citizenship & Other Info
    identification_id = fields.Char('Identification No')
    passport_id = fields.Char('Passport No')
    country_id = fields.Many2one('res.country')
    #   Permanent Address
    is_same_address = fields.Boolean('Same as Correspondence Address')
    street_ht = fields.Char('Street')
    street2_ht = fields.Char('Street2')
    city_ht = fields.Char('City')
    zip_ht = fields.Char('Zip')
    state_id_ht = fields.Many2one('res.country.state', string="State")

    #   Job reference
    ref_name = fields.Char('Referred by')
    ref_org = fields.Char('Organization')
    ref_rel = fields.Char('Relation')
    ref_contact = fields.Char('Contact Details')
    #   academic, experience, certifications histories
    academic_ids = fields.One2many('hr.academic', 'applicant_id',
                                   'Academic experiences',
                                   help="Academic experiences")
    experience_ids = fields.One2many('hr.experience', 'applicant_id',
                                     'Professional Experiences',
                                     help='Define Professional Experiences')
    certification_ids = fields.One2many('hr.certification', 'applicant_id',
                                        'Certifications',
                                        help="Certifications")

    @api.model
    def create(self, vals):
        result = super(HrApplicant, self).create(vals)
        bdate = False
        if not self.env.context.get('website_id'):
            if (self.salary_expected < 0):
                raise ValidationError("Please enter expected salary properly!")
            if (vals['salary_proposed'] < 0):
                raise ValidationError("Proposed salary does not accept negative value!")
            if vals['birthday']:
                bdate = datetime.strptime(str(vals['birthday']), "%Y-%m-%d").date()
            today = date.today()
            if bdate:
                diff = today - bdate
                if today <= bdate:
                    raise ValidationError("Please enter birth date properly!")
        try:
            return result
        except:
            raise ValidationError("Please Enter Fields Name Properly!")

    def write(self, vals):
        results = super(HrApplicant, self).write(vals)
        if not self.env.context.get('website_id'):
            curr_rec = self.browse(self.id)
            if vals.get('salary_expected') != None:
                if (vals.get('salary_expected') < 0):
                    raise ValidationError("Please enter expected salary properly!")

            if vals.get('salary_proposed') != None:
                if (vals.get('salary_proposed') < 0):
                    raise ValidationError("Please enter proposed salary properly!")

            if vals.get('birthday') != None:
                temp = datetime.strptime(vals.get('birthday'), "%Y-%m-%d").date()
                today = date.today()
                diff = today - temp
                if today <= temp:
                    raise ValidationError("Please enter birth date properly!")
        today = date.today()
        return results

    def create_employee_from_applicant(self):
        """ Create an hr.employee from the hr.applicants """
        employee = False
        for applicant in self:
            contact_name = False
            if applicant.partner_id:
                address_id = applicant.partner_id.address_get(['contact'])['contact']
                contact_name = applicant.partner_id.name_get()[0][1]
            else:
                new_partner_id = self.env['res.partner'].create({
                    'is_company': False,
                    'name': applicant.partner_name,
                    'email': applicant.email_from,
                    'phone': applicant.partner_phone,
                    'mobile': applicant.partner_mobile,
                    'country_id': applicant.country_id.id,
                })
                address_id = new_partner_id.address_get(['contact'])['contact']
            if applicant.job_id and (applicant.partner_name or contact_name):
                applicant.job_id.write({'no_of_hired_employee': applicant.job_id.no_of_hired_employee + 1})
                employee = self.env['hr.employee'].create({'birthday': applicant.birthday,
                                                           'gender': applicant.gender,
                                                           'marital': applicant.marital,
                                                           'zip_ht': applicant.zip_ht,
                                                           'state_id_ht': applicant.state_id_ht.id,
                                                           'country_id': applicant.country_id.id,
                                                           'city_ht': applicant.city_ht,
                                                           'mobile_phone': applicant.partner_mobile,
                                                           'street_ht': applicant.street_ht,
                                                           'street2_ht': applicant.street2_ht,
                                                           'identification_id': applicant.identification_id,
                                                           'name': applicant.partner_name or contact_name,
                                                           'job_id': applicant.job_id.id,
                                                           'address_home_id': address_id,
                                                           'work_email': applicant.email_from,
                                                           'passport_id': applicant.passport_id,
                                                           'work_phone': applicant.partner_phone,
                                                           'place_of_birth': applicant.place_of_birth,
                                                           'country_of_birth': applicant.country_of_birth_lt.id,
                                                           'department_id': applicant.department_id.id or False,
                                                           'address_id': applicant.company_id and applicant.company_id.partner_id
                                                                         and applicant.company_id.partner_id.id or False,
                                                           })
                applicant.write({'emp_id': employee.id})
                applicant.job_id.message_post(
                    body=_(
                        'New Employee %s Hired') % applicant.partner_name if applicant.partner_name else applicant.name,
                    subtype="hr_recruitment.mt_job_applicant_hired")

            else:
                raise UserError(_('You must define an Applied Job and a Contact Name for this applicant.'))
        for acad in applicant.academic_ids:
            self.env['hr.academic'].create({
                'name': acad.name,
                'employee_id': employee.id,
                'organization': acad.organization,
                'study_field': acad.study_field,
                'location': acad.location,
                'start_date': acad.start_date,
                'end_date': acad.end_date,
                'is_still': acad.is_still,
                'grade': acad.grade,
                'activities': acad.activities,
                'description': acad.description
            })
        for certificate in applicant.certification_ids:
            self.env['hr.certification'].create({
                'name': certificate.name,
                'employee_id': employee.id,
                'certification': certificate.certification,
                'organization': certificate.organization,
                'location': certificate.location,
                'start_date': certificate.start_date,
                'end_date': certificate.end_date,
                'is_still': certificate.is_still,
                'description': certificate.description
            })
        for experience in applicant.experience_ids:
            self.env['hr.experience'].create({
                'name': experience.name,
                'employee_id': employee.id,
                'type': experience.type,
                'organization': experience.organization,
                'location': experience.location,
                'start_date': experience.start_date,
                'end_date': experience.end_date,
                'is_still': experience.is_still,
                'description': experience.description,
                'referee_name': experience.referee_name,
                'referee_position': experience.referee_position,
                'referee_position': experience.referee_position
            })
        employee_action = self.env.ref('hr.open_view_employee_list')
        dict_act_window = employee_action.read([])[0]
        if employee:
            dict_act_window['res_id'] = employee.id
        dict_act_window['view_mode'] = 'form,tree'
        return dict_act_window
