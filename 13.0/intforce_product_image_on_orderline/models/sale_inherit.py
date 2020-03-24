from odoo import api, fields, models, tools, _


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"
    product_image = fields.Binary(related='product_id.image_1920', string="Product Image")
    

    