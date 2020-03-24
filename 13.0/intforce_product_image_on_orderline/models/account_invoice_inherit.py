from odoo import api, fields, models, _



class AccountInvoiceLine(models.Model):
    _inherit = "account.move.line"  
    product_image = fields.Binary(related='product_id.image_1920', string="Product Image")