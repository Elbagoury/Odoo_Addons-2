# -*- coding: utf-8 -
from odoo import models


class SaleAdvancePaymentInvoice(models.TransientModel):

    _inherit = "sale.advance.payment.inv"

    def _create_invoice(self, order, so_line, amount):
        res = super(SaleAdvancePaymentInvoice, self)._create_invoice(order, so_line, amount)
        res.write({
            'delivery_date': order.delivery_date,
            'delivery_note': order.delivery_note
        })
        return res
