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
    _inherit = 'appointment.config.settings'

    website_appoint_payment_mode = fields.Selection(
        [('before_appoint', 'Before Appointment'), ('after_appoint', 'After Appointment')],
        string= 'Appointment Payment Mode in Website',
        default = 'before_appoint',
    )

    @api.multi
    def set_values(self):
        super(ResConfigSettings, self).set_values()
        IrDefault = self.env['ir.default'].sudo()
        IrDefault.set('appointment.config.settings', 'website_appoint_payment_mode', self.website_appoint_payment_mode)
        return True

    @api.model
    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        IrDefault = self.env['ir.default'].sudo()
        res.update(
            {
            'website_appoint_payment_mode':IrDefault.get('appointment.config.settings', 'website_appoint_payment_mode'),
            }
        )
        return res
