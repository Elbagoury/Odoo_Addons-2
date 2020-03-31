# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.
##############################################################################

from odoo import api, fields, models, _

class account_move(models.Model):
	
	_inherit = 'account.move'
	_order = 'invoice_date_due'
	
	def _get_result(self):
		for aml in self:
			aml.result = 0.0
			aml.result = aml.amount_total_signed - aml.credit_amount 

	def _get_credit(self):
		for aml in self:
			aml.credit_amount = 0.0
			aml.credit_amount = aml.amount_total_signed - aml.amount_residual_signed

	credit_amount = fields.Float(compute ='_get_credit',   string="Credit/paid")
	result = fields.Float(compute ='_get_result',   string="Balance") #'balance' field is not the same


