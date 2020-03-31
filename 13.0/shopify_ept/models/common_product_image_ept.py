from odoo import models, api
from .. import shopify
import urllib
import base64
import os

import base64
import hashlib
import json
import logging
import requests
from datetime import datetime, timedelta

from odoo import models, fields, api

_logger = logging.getLogger(__name__)


class ProductImageEpt(models.Model):
    _inherit = 'common.product.image.ept'

    @api.model
    def create(self, vals):
        """
         Inherited for adding images in Shopify products.
        @author: Bhavesh Jadav  on Date 17-Dec-2019.
        """
        result = super(ProductImageEpt, self).create(vals)
        shopify_product_image_obj = self.env["shopify.product.image.ept"]
        shopify_product_image_vals = {"odoo_image_id": result.id}

        if vals.get("product_id", False):
            shopify_variants = self.env['shopify.product.product.ept'].search_read(
                [('product_id', '=', vals.get("product_id"))], ["id", "shopify_template_id"])
            for shopify_variant in shopify_variants:
                shopify_product_image_vals.update({"shopify_variant_id": shopify_variant["id"],
                                                   "shopify_template_id": shopify_variant["shopify_template_id"][0]})
                shopify_product_image_obj.create(shopify_product_image_vals)
        elif vals.get("template_id", False):
            shopify_templates = self.env["shopify.product.template.ept"].search_read(
                [("product_tmpl_id", "=", vals.get("template_id"))], ["id"])
            for shopify_template in shopify_templates:
                shopify_product_image_vals.update({'shopify_template_id': shopify_template["id"]})
                shopify_product_image_obj.create(shopify_product_image_vals)
        return result

    def write(self, vals):
        """
         Inherited for adding images in Shopify products.
         @author: Bhavesh Jadav  on Date 17-Dec-2019.
        """
        result = super(ProductImageEpt, self).write(vals)
        shopify_product_images = self.env["shopify.product.image.ept"]
        for record in self:
            shopify_product_images += shopify_product_images.search([("odoo_image_id", "=", record.id)])
        if shopify_product_images:
            if vals.get("product_id", "") == False:
                shopify_product_images.write({'shopify_variant_id': False})
            elif vals.get("product_id", ""):
                for shopify_product_image in shopify_product_images:
                    shopify_variant = self.env["shopify.product.product.ept"].search_read(
                        [("product_id", "=", vals.get("product_id")),
                         ("shopify_template_id", "=", shopify_product_image.shopify_template_id.id)], ["id"])
                    if shopify_variant:
                        shopify_product_image.write({"shopify_variant_id": shopify_variant["id"]})
        return result

    # shopify_product_tmpl_id=fields.Many2one('shopify.product.template.ept', string='Shopify Product')
    # shopify_variant_ids=fields.Many2many('shopify.product.product.ept', 'shopify_product_image_rel', 'shopify_product_image_id', 'shopify_variant_id', 'Product Variants')
    # shopify_instance_id=fields.Many2one("shopify.instance.ept", string="Instance")
    # shopify_image_id=fields.Char("Shopify Image Id")

    def shopify_sync_product_images(self, instance, response_template, shopify_template, shopify_product,
                                    template_image_updated):
        """
        Author: Bhavesh Jadav 18/12/2019
        This method use for sync image from store and the add refrence in shopify.product.image.ept
        param:instance:use for the shopify instance its type should be object
        param:response_template usr for the product response its type should be dict
        param:shopify_template use for the shopify template  its type should be object
        param:shopify_product use for the shopify product its type should be object
        param: template_image_updated its boolean for the manage update template image only one time
        """
        common_product_image_obj = self.env["common.product.image.ept"]
        shopify_product_image_obj = shopify_product_images = need_to_remove = self.env["shopify.product.image.ept"]
        existing_common_template_images = {}
        for odoo_image in shopify_template.product_tmpl_id.ept_image_ids:
            if not odoo_image.image:
                continue
            key = hashlib.md5(odoo_image.image).hexdigest()
            if not key:
                continue
            existing_common_template_images.update({key: odoo_image.id})
        for image in response_template.get('images', {}):
            if image.get('src'):
                shopify_image_id = str(image.get('id'))
                url = image.get('src')
                variant_ids = image.get('variant_ids')
                if not variant_ids:
                    if template_image_updated:
                        continue
                    shopify_product_image = shopify_product_image_obj.search(
                        [("shopify_template_id", "=", shopify_template.id),
                         ("shopify_variant_id", "=", False),
                         ("shopify_image_id", "=", shopify_image_id)])
                    if not shopify_product_image:
                        try:
                            response = requests.get(url, stream=True, verify=False, timeout=10)
                            if response.status_code == 200:
                                image = base64.b64encode(response.content)
                                key = hashlib.md5(image).hexdigest()
                                if key in existing_common_template_images.keys():
                                    shopify_product_image = shopify_product_image_obj.create(
                                        {"shopify_template_id": shopify_template.id,
                                         "shopify_image_id": shopify_image_id,
                                         "odoo_image_id": existing_common_template_images[key]})
                                else:
                                    common_product_image = common_product_image_obj.create(
                                        {"name": shopify_template.name,
                                         "template_id": shopify_template.product_tmpl_id.id,
                                         "image": image,
                                         "url": url})
                                    shopify_product_image = shopify_product_image_obj.search([
                                        ("shopify_template_id", "=", shopify_template.id),
                                        ("odoo_image_id", "=", common_product_image.id)])
                                    if shopify_product_image:
                                        shopify_product_image.shopify_image_id = shopify_image_id
                        except Exception:
                            pass
                    shopify_product_images += shopify_product_image
                else:
                    variant_id = int(shopify_product.variant_id)
                    if variant_id in variant_ids:
                        existing_common_variant_images = {}
                        for odoo_image in shopify_product.product_id.ept_image_ids:
                            if not odoo_image.image:
                                continue
                            key = hashlib.md5(odoo_image.image).hexdigest()
                            if not key:
                                continue
                            existing_common_variant_images.update({key: odoo_image.id})

                        shopify_product_image = shopify_product_image_obj.search(
                            [("shopify_variant_id", "=", shopify_product.id),
                             ("shopify_image_id", "=", shopify_image_id)])
                        if not shopify_product_image:
                            try:
                                response = requests.get(url, stream=True, verify=False, timeout=10)
                                if response.status_code == 200:
                                    image = base64.b64encode(response.content)
                                    key = hashlib.md5(image).hexdigest()
                                    if key in existing_common_variant_images.keys():
                                        shopify_product_image = shopify_product_image_obj.create(
                                            {"shopify_template_id": shopify_template.id,
                                             "shopify_variant_id": shopify_product.id,
                                             "shopify_image_id": shopify_image_id,
                                             "odoo_image_id": existing_common_variant_images[key]})
                                    else:
                                        common_product_image = common_product_image_obj.create(
                                            {"name": shopify_template.name,
                                             "template_id": shopify_template.product_tmpl_id.id,
                                             "product_id": shopify_product.product_id.id,
                                             "image": image,
                                             "url": url})
                                        shopify_product_image = shopify_product_image_obj.search([
                                            ("shopify_template_id", "=", shopify_template.id),
                                            ("shopify_variant_id", "=", shopify_product.id),
                                            ("odoo_image_id", "=", common_product_image.id)])
                                        if shopify_product_image:
                                            shopify_product_image.shopify_image_id = shopify_image_id

                            except Exception:
                                pass
                        all_shopify_product_images = shopify_product_image_obj.search(
                            [("shopify_template_id", "=", shopify_template.id),
                             ("shopify_variant_id", "=", shopify_product.id)])
                        need_to_remove += (all_shopify_product_images - shopify_product_image)
        all_shopify_product_images = shopify_product_images.search(
            [("shopify_template_id", "=", shopify_template.id),
             ("shopify_variant_id", "=", False)])
        if shopify_product_images:
            need_to_remove += (all_shopify_product_images - shopify_product_images)
        need_to_remove.unlink()
        _logger.info("Images Updated for Variant {0}".format(shopify_product.name))
        return True

    # def shopify_sync_product_images(self, instance, shopify_template=False, image_response=False,
    #                                 import_data_id = False, shopify_tmpl_id = False):
    #     """This method used to Sync the shopify products image. You can see the shopify sync Images :
    #         @param : self, instance, shopify_template=False, image_response=False
    #         @return: True
    #         @author: Haresh Mori @Emipro Technologies Pvt. Ltd on date 15/10/2019.
    #     """
    #     shopify_product_obj = self.env['shopify.product.product.ept']
    #     comman_log_line_obj = self.env["common.log.lines.ept"]
    #     model = "common.product.image.ept"
    #     model_id = comman_log_line_obj.get_model_id(model)
    #     if not import_data_id and shopify_tmpl_id:
    #         instance.connect_in_shopify()
    #         try:
    #             images = shopify.Image().find(product_id=shopify_tmpl_id)
    #         except Exception as e:
    #             message = e
    #             comman_log_line_obj.shopify_create_log_line(message, model_id, import_data_id)
    #             return False
    #         image_response = [image.to_dict() for image in images]
    #     for image in image_response:
    #         if image.get('src'):
    #             variant_ids = image.get('variant_ids')
    #             shopify_image_id = image.get('id')
    #             shopify_variants = shopify_product_obj.search(
    #                 [('shopify_instance_id', '=', instance.id), ('variant_id', 'in', variant_ids),('shopify_template_id', '=', shopify_template.id)])
    #             if not shopify_variants:
    #                 product_id = shopify_template.shopify_product_ids and shopify_template.shopify_product_ids[0].product_id
    #             else:
    #                 product_id = shopify_variants and shopify_variants[0].product_id
    #             shopify_variants and shopify_variants.write({'shopify_image_id': shopify_image_id})
    #             odoo_product_ids = variant_ids and [shopify_variant.product_id for shopify_variant in
    #                                                 shopify_variants] or []
    #             shopify_product_ids = variant_ids and [
    #                 (6, 0, [shopify_variant.id for shopify_variant in shopify_variants])]
    #             shopify_gallery_image = self.search(
    #                 [('shopify_product_tmpl_id', '=', shopify_template.id),
    #                  ('shopify_image_id', '=', shopify_image_id)], limit=1)
    #             if not instance.is_image_url:
    #                 try:
    #                     (filename, header) = urllib.request.urlretrieve(image.get('src'))
    #                     with open(filename, 'rb') as f:
    #                         img = base64.b64encode(f.read())
    #                 except Exception:
    #                     continue
    #                 for products in odoo_product_ids:
    #                     products.write({'image_1920': img})
    #                 if shopify_gallery_image:
    #                     shopify_gallery_image.write({'position': image.get('position'), 'height': image.get('height'),
    #                     'width': image.get('width'),'image': img,
    #                     'shopify_variant_ids': shopify_product_ids and shopify_product_ids})
    #                 else:
    #                     shopify_gallery_image = self.search([('shopify_product_tmpl_id', '=', shopify_template.id),('position', '=', image.get('position'))], limit=1)
    #                     if shopify_gallery_image:
    #                         shopify_gallery_image.write({'position': image.get('position'), 'height': image.get('height'),'width': image.get('width'),'image': img,'shopify_variant_ids': shopify_product_ids and shopify_product_ids})
    #                     else:
    #                         self.create(
    #                         {'shopify_product_tmpl_id': shopify_template.id, 'shopify_instance_id': instance.id,
    #                         'image': img, 'shopify_image_id': image.get('id'), 'position': image.get('position'),
    #                         'height': image.get('height'), 'width': image.get('width'),
    #                         'shopify_variant_ids': shopify_product_ids and shopify_product_ids,
    #                         'product_id' : product_id and product_id.id or False,
    #                         'url': image.get('src')
    #                         })
    #                 if image.get('position') == 1:
    #                     shopify_template.product_tmpl_id.write({'image_1920': img})
    #                 if filename:
    #                     os.remove(filename)
    #             else:
    #                 if shopify_gallery_image:
    #                     shopify_gallery_image.write({'position': image.get('position'), 'height': image.get('height'),
    #                                                  'width': image.get('width'),
    #                                                  'shopify_variant_ids': shopify_product_ids and shopify_product_ids})
    #                 else:
    #                     self.create(
    #                         {'shopify_product_tmpl_id': shopify_template.id, 'shopify_instance_id': instance.id,
    #                          'url': image.get('src'), 'shopify_image_id': image.get('id'),
    #                          'position': image.get('position'), 'height': image.get('height'),
    #                          'width': image.get('width'),
    #                          'shopify_variant_ids': shopify_product_ids and shopify_product_ids,
    #                          'product_id' : product_id and product_id.id or False,
    #                          })
    #     return True
