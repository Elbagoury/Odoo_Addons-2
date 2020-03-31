# -*- coding: utf-8 -*-
#################################################################################
#
#    Odoo, Open Source Management Solution
#    Copyright (C) 2019-Today Ascetic Business Solution <www.asceticbs.com>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#################################################################################
from ast import literal_eval
from odoo import api, models, fields

class ResPartner(models.Model):
    _inherit = 'res.partner'

    invoice_paid_amount = fields.Float(compute='_get_invoice_paid_amount', string='Invoice Paid Amount', help='This field will give the invoice paid amount of the particular customer.')

    #For getting the invoice paid amount of the customer
    def _get_invoice_paid_amount(self):
        for record in self:
            paid_amount = open_amount = total_amount = 0.0
            invoice_paid_ids = self.env['account.move'].sudo().search([('partner_id', '=', record.id),('state', '=', 'posted'),('type','in', ('out_invoice', 'out_refund'))])
            if invoice_paid_ids:
                for invoice in invoice_paid_ids:
                    if invoice.amount_residual == 0:
                        paid_amount += invoice.amount_total
            invoice_open_ids = self.env['account.move'].sudo().search([('partner_id', '=', record.id),('state', 'not in', ['draft', 'cancel','paid']),('type','in', ('out_invoice', 'out_refund'))])
            if invoice_open_ids:
                for invoice in invoice_open_ids:
                    if invoice.amount_residual > 0:
                        open_amount += (invoice.amount_total - invoice.amount_residual)
            total_amount = open_amount + paid_amount
            record.invoice_paid_amount = total_amount

    def open_partner_history(self):
        '''
        This function returns an action that display invoices/refunds made for the given partners.
        '''
        action = self.env.ref('account.action_move_out_invoice_type').read()[0]
        action['domain'] = literal_eval(action['domain'])
        action['domain'].append(('partner_id', 'child_of', self.ids))
        return action

