from odoo import fields, models, api
from odoo.exceptions import ValidationError


class UpwareBrand(models.Model):
    _name = "upware.brand"
    _description = "Upware Categorie"

    name = fields.Char('Merk')
    code = fields.Char('Code')
