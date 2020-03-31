from odoo import models, fields, api, _
from .. import shopify
import logging

_logger = logging.getLogger(__name__)

class ShopifyResPartnerEpt(models.Model):
    _name = "shopify.res.partner.ept"
    _description = 'Shopify Res Partner Ept'

    partner_id = fields.Many2one("res.partner", "partner ID")
    shopify_instance_id = fields.Many2one("shopify.instance.ept", "Instances")
    shopify_customer_id = fields.Char("Shopify Cutstomer Id")

