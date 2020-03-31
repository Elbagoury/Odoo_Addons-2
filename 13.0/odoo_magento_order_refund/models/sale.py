# -*- coding: utf-8 -*-
##############################################################################
#
# Copyright (c) 2015-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>)
# See LICENSE file for full copyright and licensing details.
# License URL : <https://store.webkul.com/license.html/>
#
##############################################################################

from odoo import _, api, fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    refunded = fields.Boolean("Refunded", help='This Status will be updated, only when order refund is done by `Refund Order` button.')
        
    def compute_delivery_return(self, return_items={}):
        if self.id:
            self = self.with_context(stock_from='magento')
            for picking_obj in self.picking_ids.filtered(lambda r: r.picking_type_code == 'outgoing'):
                if picking_obj.state == 'cancel':
                    continue
                if picking_obj.state not in ['done']:
                    # checking for partial deliveries.
                    if return_items:
                        refund_products = [int(p_id) for p_id in return_items.keys()]
                        for move in picking_obj.move_lines:
                            new_qty = 0
                            product_id = move.product_id.id
                            if product_id in refund_products:
                                cancelled_qty = float(return_items[str(product_id)])
                                new_qty = move.product_uom_qty - cancelled_qty
                                move.product_uom_qty = new_qty
                                message = "<b>Credit Memo Submitted at Magento, %s quantity of %s is cancelled from magento.</b>" % (cancelled_qty, move.product_id.name)
                                picking_obj.message_post(body=message)
                    else:
                        picking_obj.action_cancel()
                        message = "<b>Credit Memo Submitted at Magento Delivery order %s cancelled successfully.</b>" % picking_obj.name
                        self.message_post(body=message)
                    return True
                if picking_obj.state == 'done':
                    # New updated code for picking return
                    new_return_moves = []
                    fields = ['move_dest_exists',
                                'original_location_id',
                                'product_return_moves',
                                'parent_location_id',
                                'location_id']
                    stock_return_picking = self.env['stock.return.picking']
                    default_return_data = stock_return_picking.with_context(active_id=picking_obj.id).default_get(fields)
                    if return_items:
                        refund_products = [int(p_id) for p_id in return_items.keys()]
                        for res in default_return_data['product_return_moves']:
                            if res[2]['product_id'] in refund_products:
                                res[2]['quantity'] = return_items[str(res[2]['product_id'])]
                                new_return_moves.append(res)
                    if new_return_moves:
                        default_return_data.update({'product_return_moves': new_return_moves})
                    # Create Return Picking Wizard
                    stock_return_picking_obj = stock_return_picking.with_context(active_id=picking_obj.id).create(default_return_data)

                    # Create Final return picking
                    return_picking_res = stock_return_picking_obj.create_returns()
                    new_picking_obj = self.env['stock.picking'].browse(return_picking_res['res_id'])

                    # Transfer new returned picking
                    new_picking_obj.action_assign()
                    for pack in new_picking_obj.move_line_ids:
                        if pack.product_qty > 0:
                            pack.write({'qty_done': pack.product_qty})
                        else:
                            pack.unlink()
                    new_picking_obj.button_validate()
                    message = "<b>Credit Memo Submitted at Magento, delivery order %s returned successfully.</b>" % picking_obj.name
                    self.message_post(body=message)
                    return True
        return True

    def compute_refund(self, refund_items={}, other_refunds={}, reason="Refund"):
        status = True
        status_message = "Order Successfully Refunded !!!"
        order_ids = self.env['sale.order'].search([])
        for order_obj in order_ids:
            try:
                invoice_id = 0
                journal_id = 0
                invoice_name = ''
                for invoice_obj in order_obj.invoice_ids.filtered(lambda r: r.type == 'out_invoice'):
                    if invoice_obj.invoice_payment_state == 'paid' and order_obj.name == invoice_obj.invoice_origin:
                        invoice_id = invoice_obj.id
                        invoice_name = invoice_obj.name
                        journal_id = invoice_obj.journal_id.id
                paid_status = order_obj.is_invoiced
            except Exception as e:
                status = False
                status_message = "Error in Refund Order: %s" % str(e)
                return {
                    'status_message': status_message,
                    'status': status
                }
            if journal_id and invoice_id and paid_status:
                # Creating draft invoice refund
                invoice_model = self.env['account.move']
                refund_model = self.env['account.move.reversal']
                refund_obj = refund_model.create({'reason': reason})

                # fetching refund invoice
                refund_invoice_id = 0
                context = {'active_ids': invoice_id}
                
                """ def invoice_refund method would be remove in v13 version. So based on that it would be
                    find the test file it is take from the last invoice and reverse would be the false.
                    @author: Harshit Trivedi
                    @status: Last Update :~ 19NOV!9
                """
                refund_invoice_res = refund_obj.with_context(context).sorted(key=lambda inv: inv.id, reverse=False)[-1]
                  
                for domain in refund_invoice_res['domain']:
                    if domain[0] == 'id':
                        refund_invoice_id = domain[2][0]

                # settelment of refund items...
                if refund_items or other_refunds:
                    other_products = []
                    other_refund_data = {}
                    refund_products = [int(p_id) for p_id in refund_items.keys()]
                    discount_product_id = self.env['wk.skeleton'].get_magento_virtual_product_id({'name': 'Discount', 'order_id': self.id})
                    adjustment_product_id = self.env['wk.skeleton'].get_magento_virtual_product_id({'name': 'Adjustment Fee', 'order_id': self.id})
                    for service, amount in other_refunds.items():
                        service_product_id = self.env['wk.skeleton'].get_magento_virtual_product_id({'name': service, 'order_id': self.id})
                        other_products.append(service_product_id)
                        other_refund_data[str(service_product_id)] = amount

                    refund_invoice_obj = invoice_model.browse(refund_invoice_id)
                    for invoice_line in refund_invoice_obj.invoice_line_ids:
                        product_id = invoice_line.product_id.id
                        # removing extra items and it's quantity
                        if product_id in refund_products:
                            invoice_line.quantity = refund_items[str(product_id)]
                              
                        elif product_id in other_products:
                            refund_amount = other_refund_data[str(product_id)]
                            if refund_amount:
                                invoice_line.price_unit = refund_amount

                            refund_amount = other_refund_data.get(str(product_id), 0)
                            if product_id == discount_product_id and invoice_line.name in other_refunds :
                                refund_amount = other_refunds.get(invoice_line.name, 0)
                            elif product_id == discount_product_id:
                                invoice_line.unlink()
                            if refund_amount and invoice_line.exists():
                                invoice_line.price_unit = refund_amount
                        else:
                            invoice_line.unlink()
                adjustment_amount = other_refund_data.get(str(adjustment_product_id), 0)
                if adjustment_amount:
                    product = self.env['product.product'].browse(int(adjustment_product_id))
                    account = product.product_tmpl_id.get_product_accounts(refund_invoice_obj.fiscal_position_id)['income']
                    lineData = {
                        'name': 'Adjustment Fees',
                        'product_id': int(adjustment_product_id),
                        'quantity': 1,
                        'price_unit': adjustment_amount,
                        'invoice_id': refund_invoice_obj.id
                    }
                    if account:
                        lineData.update(account_id=account.id)
                    self.env['account.move.line'].create(lineData)

                # refund invoice payment
                if refund_invoice_id:
                    """ def action_invoice_open method would be remove in v13 version. So based on the code changes
                         it would be take the method action_post for the invoice process
                        @author: Harshit Trivedi
                        @status: Last Update :~ 19NOV19
                    """
                    invoice_model.browse(refund_invoice_id).action_post()
                    
                    ctx = {'default_invoice_ids': [[4, refund_invoice_id, None]],
                           'active_model': 'account.move',
                           'journal_type': 'sale',
                           'search_disable_custom_filters': True,
                           'active_ids': [refund_invoice_id],
                           'active_id': refund_invoice_id}
                    context.update(ctx)
                    # Getting all default field values for Payment Wizard
                    fields = ['communication', 'currency_id',
                              'invoice_ids', 'payment_difference',
                               'partner_id', 'payment_method_id',
                               'payment_difference_handling', 'journal_id',
                               'state', 'writeoff_account_id',
                               'payment_date', 'partner_type',
                               'hide_payment_method', 'payment_method_code',
                               'amount', 'payment_type' ]
                   
                    default_vals = self.env['account.payment'].with_context(context).default_get(fields)
                    payment_method_id = self.env['wk.skeleton'].with_context(context).get_default_payment_method(journal_id)
                    default_vals.update({'journal_id': journal_id, 'payment_method_id': payment_method_id })
                    payment = self.env['account.payment'].with_context(context).create(default_vals)
                    payment.with_context(context).post()
                    message = "<b>Credit Memo Submitted at Magento, Invoice %s refunded successfully.</b>" % invoice_name
                    self.message_post(body=message)
                    self.write({'refunded': True})
            else:
                status = False
                status_message = "You Cannot refund an Unpaid Order."
            return {'status_message': status_message, 'status': status}

class AccountMove(models.Model):
    _inherit = 'account.move'
    
   
          
