# -*- coding: utf-8 -*-

from odoo import api, fields, models


class StockPicking(models.Model):
    _inherit = "stock.picking"

    digital_id = fields.Integer(compute='_get_digital_id', string='Digital Id', readonly=True)

    @api.depends('name')
    def _get_digital_id(self):
        try:
            self.digital_id = self.name.split('POI/LIV/')[1]
        except IndexError:
            self.digital_id = self.name.split('POI/REC/')[1]
