# -*- coding: utf-8 -*-
from datetime import datetime

from odoo import http
from odoo.addons.website_sale.controllers import main as website_sale
from odoo.http import request
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT


class OrderDelieveryDuration(website_sale.WebsiteSale):

    def update_delivery_date(self, post, delivery_date_and_message):
        delivery_date = datetime.strptime(post.get('delivery_date'), '%m/%d/%Y')
        delivery_date = datetime.strftime(delivery_date.date(), DEFAULT_SERVER_DATETIME_FORMAT)
        delivery_date_and_message.update({'delivery_date': delivery_date})
        return delivery_date_and_message

    @http.route(['/shop/confirm_order'], type='http', auth="public", website=True)
    def confirm_order(self, **post):
        res = super(OrderDelieveryDuration, self).confirm_order(**post)
        order = request.website.sale_get_order()

        delivery_date_and_message = {}
        if (post.get('delivery_date') and post.get('delivery_message')):
            delivery_date_and_message = self.update_delivery_date(post, delivery_date_and_message)
            delivery_date_and_message.update({'delivery_note': post.get('delivery_message')})
        elif post.get('delivery_date'):
            delivery_date_and_message = self.update_delivery_date(post, delivery_date_and_message)
        elif post.get('delivery_message'):
            delivery_date_and_message = {'delivery_note': post.get('delivery_message')}

        if delivery_date_and_message:
            order.write(delivery_date_and_message)
        return res
