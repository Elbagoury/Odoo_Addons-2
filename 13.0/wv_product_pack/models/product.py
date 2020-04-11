# -*- coding: utf-8 -*-

from odoo import fields, models,tools,api

class product_pack(models.Model):
    _name = 'product.pack'

    product_id = fields.Many2one('product.product','Product')
    wv_product_id = fields.Many2one('product.product','Product')
    qty = fields.Float("Quantity",default=1)
    image = fields.Binary("Image")


class product_product(models.Model):
    _inherit = 'product.template'
    
    is_pack = fields.Boolean('Is Pack')
    fix_pack_id = fields.One2many('product.pack','product_id',string="Pack")
    pack_total_price = fields.Float("Pack Total Price",compute='_get_total_pack_price', readonly=True)

    @api.depends('fix_pack_id.wv_product_id', 'fix_pack_id.wv_product_id')
    def _get_total_pack_price(self):
        for product in self:
            pack_total_price = 0.00
            for pack_pro in product.fix_pack_id:
                pack_total_price += pack_pro.wv_product_id.lst_price * pack_pro.qty
            product.pack_total_price = pack_total_price
