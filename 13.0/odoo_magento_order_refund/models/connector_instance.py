# -*- coding: utf-8 -*-
##########################################################################
#
#   Copyright (c) 2015-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>)
#   See LICENSE file for full copyright and licensing details.
#   License URL : <https://store.webkul.com/license.html/>
#
##########################################################################

from odoo import api, fields, models


class ConnectorInstance(models.Model):
    _inherit = "connector.instance"

    mob_adjustment_product = fields.Many2one('product.product', string="Adjustment Fee Product", config_parameter='odoo_magento_connect.mob_adjustment_product', help="""Service type product used for Credit memo adjustment purposes.""")
    
