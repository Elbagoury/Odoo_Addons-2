# -*- coding: utf-8 -*-
#################################################################################
# Author      : Webkul Software Pvt. Ltd. (<https://webkul.com/>)
# Copyright(c): 2015-Present Webkul Software Pvt. Ltd.
# License URL : https://store.webkul.com/license.html/
# All Rights Reserved.
#
#
#
# This program is copyright property of the author mentioned above.
# You can`t redistribute it and/or modify it.
#
#
# You should have received a copy of the License along with this program.
# If not, see <https://store.webkul.com/license.html/>
#################################################################################

from odoo import api, fields, models, _
import logging
_logger = logging.getLogger(__name__)

class ResConfigSettings(models.TransientModel):
    _name = 'appointment.config.settings'
    _inherit = 'res.config.settings'

    @api.model
    def _default_journal(self):
        obj = self.env["account.journal"].search([('name', '=', _('Customer Invoices'))])
        return obj[0] if obj else self.env["account.journal"]

    appoint_product_ids = fields.Many2many(comodel_name='product.product', string= 'Product')
    enable_notify_reminder = fields.Boolean("Enable to send mail reminder before appointment")
    notify_reminder_mail_template = fields.Many2one(
        "mail.template", string="Mail Notification Reminder", domain="[('model_id.model','=','appointment')]")
    enable_notify_customer_on_approve_appoint = fields.Boolean("Enable to send mail on Appointment Confirmation")
    notify_customer_on_approve_appoint = fields.Many2one(
        "mail.template", string="Appointment Confirmation Mail", domain="[('model_id.model','=','appointment')]")
    enable_notify_customer_on_reject_appoint = fields.Boolean("Enable to send mail on Appointment Reject")
    notify_customer_on_reject_appoint = fields.Many2one(
        "mail.template", string="Appointment Reject Mail", domain="[('model_id.model','=','appointment')]")
    appoint_journal_account = fields.Many2one("account.journal", string="Appointment Journal", default=_default_journal,)
    allow_multi_appoints = fields.Boolean("Allow Multiple Appointments",
        default=True,
        help="If it is enabled then Group Members can handle multiple appointments in a particular timeslot,\
         if not then group members can handle only a single appointment in a given time slot.This setting can also be managed\
         member wise for each member from thier profile.")

    @api.multi
    def set_values(self):
        super(ResConfigSettings, self).set_values()
        IrDefault = self.env['ir.default'].sudo()
        IrDefault.set('appointment.config.settings', 'appoint_product_ids', self.appoint_product_ids.ids)
        IrDefault.set('appointment.config.settings', 'enable_notify_reminder', self.enable_notify_reminder)
        IrDefault.set('appointment.config.settings', 'notify_reminder_mail_template', self.notify_reminder_mail_template.id)
        IrDefault.set('appointment.config.settings', 'enable_notify_customer_on_approve_appoint', self.enable_notify_customer_on_approve_appoint)
        IrDefault.set('appointment.config.settings', 'notify_customer_on_approve_appoint', self.notify_customer_on_approve_appoint.id)
        IrDefault.set('appointment.config.settings', 'enable_notify_customer_on_reject_appoint', self.enable_notify_customer_on_reject_appoint)
        IrDefault.set('appointment.config.settings', 'notify_customer_on_reject_appoint', self.notify_customer_on_reject_appoint.id)
        IrDefault.set('appointment.config.settings', 'appoint_journal_account', self.appoint_journal_account.id)
        IrDefault.set('appointment.config.settings', 'allow_multi_appoints', self.allow_multi_appoints)
        return True

    @api.model
    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        appoint_reminder_mail_template = self.env['ir.model.data'].get_object_reference(
            'wk_appointment', 'reminder_mail_to_customer')[1]
        notify_customer_on_approve_appoint = self.env['ir.model.data'].get_object_reference(
            'wk_appointment', 'appoint_mgmt_email_template_to_customer')[1]
        notify_customer_on_reject_appoint = self.env['ir.model.data'].get_object_reference(
            'wk_appointment', 'appoint_mgmt_reject_email_template_to_customer')[1]
        IrDefault = self.env['ir.default'].sudo()
        product_ids = IrDefault.get('appointment.config.settings', 'appoint_product_ids')
        appoint_product_ids = []
        if product_ids:
            for i in product_ids:
                if self.env['product.product'].browse(i).exists():
                    appoint_product_ids.append(i)
        res.update(
            {
            'appoint_product_ids': appoint_product_ids,
            'enable_notify_reminder':IrDefault.get('appointment.config.settings', 'enable_notify_reminder'),
            'notify_reminder_mail_template':IrDefault.get('appointment.config.settings', 'notify_reminder_mail_template')
                or appoint_reminder_mail_template,
            'enable_notify_customer_on_approve_appoint':IrDefault.get('appointment.config.settings', 'enable_notify_customer_on_approve_appoint'),
            'notify_customer_on_approve_appoint':IrDefault.get('appointment.config.settings', 'notify_customer_on_approve_appoint')
                or notify_customer_on_approve_appoint,
            'enable_notify_customer_on_reject_appoint':IrDefault.get('appointment.config.settings', 'enable_notify_customer_on_reject_appoint'),
            'notify_customer_on_reject_appoint':IrDefault.get('appointment.config.settings', 'notify_customer_on_reject_appoint')
                or notify_customer_on_reject_appoint,
            'appoint_journal_account':IrDefault.get('appointment.config.settings', 'appoint_journal_account') or self._default_journal().id,
            'allow_multi_appoints':IrDefault.get('appointment.config.settings', 'allow_multi_appoints'),
            }
        )
        return res
