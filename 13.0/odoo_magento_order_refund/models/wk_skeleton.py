# -*- coding: utf-8 -*-
##############################################################################
#
# Copyright (c) 2015-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>)
# See LICENSE file for full copyright and licensing details.
# License URL : <https://store.webkul.com/license.html/>
#
##############################################################################

from odoo import api, models


class WkSkeleton(models.TransientModel):
    _inherit = 'wk.skeleton'

    @api.model
    def get_magento_virtual_product_id(self, data):
        odoo_product_id = False
        virtual_name = data.get('name')[0]
        if virtual_name == 'A':
            instance_id = self.env['connector.instance'].search([('active', '=', True)], limit=1)
            odoo_product_id = instance_id.mob_adjustment_product
            if not odoo_product_id:
                temp_dict = {
                    'sale_ok' : False,
                    'name' : 'Adjustment Fee',
                    'type' : 'service',
                    'list_price' : 0.0,
                    'description': 'Service Type product used by Magento Odoo Bridge for Adjustment Fees.'
                }
                odoo_product_id = self.env['product.product'].create(temp_dict).id
            else:
                odoo_product_id = odoo_product_id and int(odoo_product_id)
            return odoo_product_id
        else:
            return super(WkSkeleton, self).get_magento_virtual_product_id(data)
