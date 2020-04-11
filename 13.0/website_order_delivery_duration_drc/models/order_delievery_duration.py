# -*- coding: utf-8 -
from odoo import fields, models


class SaleOrderDeliveryTime(models.Model):

    _inherit = "sale.order"

    delivery_date = fields.Date()
    delivery_note = fields.Text(translate=True)

    def _prepare_invoice(self):

        res = super(SaleOrderDeliveryTime, self)._prepare_invoice()
        res.update({
            'delivery_date': self.delivery_date,
            'delivery_note': self.delivery_note
        })
        return res


class AccountInvoiceDelievryTime(models.Model):

    _inherit = "account.move"

    delivery_date = fields.Date()
    delivery_note = fields.Text(translate=True)


class StockPickingDelievryTime(models.Model):

    _inherit = "stock.picking"

    delivery_date = fields.Date()
    delivery_note = fields.Text(translate=True)


class StockMoveDeliveryTime(models.Model):

    _inherit = "stock.move"

    def _assign_picking(self):
        Picking = self.env['stock.picking'].sudo()
        self.recompute()
        for move in self:
            if move.group_id:
                SaleOrder_ID = self.env['sale.order'].sudo().search([('name', '=', move.group_id.name)])
            if SaleOrder_ID:
                picking = Picking.search([
                    ('group_id', '=', move.group_id.id),
                    ('location_id', '=', move.location_id.id),
                    ('location_dest_id', '=', move.location_dest_id.id),
                    ('picking_type_id', '=', move.picking_type_id.id),
                    ('printed', '=', False),
                    ('state', 'in', ['draft', 'confirmed', 'waiting', 'partially_available', 'assigned'])], limit=1)
                if not picking:
                    picking = Picking.create(move._get_new_picking_values())

                picking.write({
                    'delivery_date': SaleOrder_ID.delivery_date,
                    'delivery_note': SaleOrder_ID.delivery_note
                })
                move.write({'picking_id': picking.id})
        return True
