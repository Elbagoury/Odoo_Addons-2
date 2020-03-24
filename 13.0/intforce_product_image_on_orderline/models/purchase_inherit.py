from odoo import api, fields, models, tools, _


class PurchaseOrderLine(models.Model):
    _inherit = "purchase.order.line"
    product_image = fields.Binary(related='product_id.image_1920', string="Product Image")
    

    