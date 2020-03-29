from odoo import fields, models, api


class MpnBrandCode(models.Model):
    _inherit = "product.template"

    upware_brand_id = fields.Many2one("upware.brand", string="Merk")
    upware_mpn = fields.Char(string="MPN")
