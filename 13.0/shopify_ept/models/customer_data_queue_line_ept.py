from odoo import models, fields, api, _
from datetime import datetime, timedelta
import json
import logging

_logger = logging.getLogger("shopify_customer_queue_line_process")

class ShopifyCustomerDataQueueLineEpt(models.Model):
    _name = "shopify.customer.data.queue.line.ept"
    _description = 'Shopify Synced Customer Data Line'

    state = fields.Selection([('draft', 'Draft'), ('failed', 'Failed'), ('done', 'Done'),
                              ("cancel","Cancelled")],
                             default='draft')
    shopify_synced_customer_data = fields.Char(string='Shopify Synced Data')
    shopify_customer_data_id = fields.Text(string='Customer ID')
    synced_customer_queue_id = fields.Many2one("shopify.customer.data.queue.ept", string="Shopify Customer",
                                          ondelete="cascade")
    last_process_date = fields.Datetime('Last Process Date', readonly=True)
    shopify_instance_id = fields.Many2one('shopify.instance.ept', string='Instance')
    common_log_lines_ids = fields.One2many("common.log.lines.ept",
                                           "shopify_customer_data_queue_line_id",
                                           help="Log lines created against which line.")

    name = fields.Char(string="Customer", help="Shopify Customer Name")
    def to_process_customer_child_cron(self):
        """This method used to start the child process cron for process the synced shopify customer data.
            @param : self
            @author: Angel Patel @Emipro Technologies Pvt.Ltd on date 25/10/2019.
            :Task ID: 157065
        """
        child_cron_of_process = self.env.ref('shopify_ept.ir_cron_child_to_process_shopify_synced_customer_data')
        if child_cron_of_process and not child_cron_of_process.active:
            results = self.search([('state', '=', 'draft')], limit=100)
            if not results:
                return True
            child_cron_of_process.write({'active': True,
                                         'numbercall': 1,
                                         'nextcall': datetime.now() + timedelta(seconds=10)
                                         })
        return True

    @api.model
    def sync_shopify_customer_into_odoo(self, results=False):
        """
        Change the queue and queue line record state using this compute method
        :param results:
        :return:
        :author: Angel Patel @Emipro Technologies Pvt.Ltd on date 02/11/2019.
        :Task ID: 157065
        """
        partner_obj = self.env['res.partner']
        comman_log_obj = self.env["common.log.book.ept"]
        if not results:
            query = """select synced_customer_queue_id from shopify_customer_data_queue_line_ept  where state='draft' ORDER BY create_date ASC limit 1"""
            self._cr.execute(query)
            customer_data_queue_id = self._cr.fetchone()
            results = self.env['shopify.customer.data.queue.ept'].browse(customer_data_queue_id).synced_customer_queue_line_ids
        queue_id = results and results.synced_customer_queue_id if len(results.synced_customer_queue_id) == 1 else False
        if results and queue_id:
            if queue_id.common_log_book_id:
                log_book_id=queue_id.common_log_book_id
            else:
                log_book_id = comman_log_obj.create({'type': 'import',
                                                     'module': 'shopify_ept',
                                                     'shopify_instance_id': queue_id.shopify_instance_id.id,
                                                     'active': True})
            for line in results:
                instance = line.synced_customer_queue_id.shopify_instance_id
                partner = partner_obj.create_or_update_customer(
                    vals=json.loads(line.shopify_synced_customer_data), is_company=True, parent_id=False, type=False,
                    instance=instance,customer_data_queue_line_id=line,log_book_id=log_book_id)
                if partner:
                    line.update({'state': 'done'})
                else:
                    line.update({'state': 'failed'})
            _logger.info("Commit 100 shopify customer queue line")
            self._cr.commit()
            queue_id.common_log_book_id = log_book_id
            # draft_or_failed_queue_line = results.filtered(lambda line: line.state in ['draft', 'failed'])
            # if draft_or_failed_queue_line:
            #     queue_id.write({'state': "partially_completed"})
            # else:
            #     queue_id.write({'state': "completed"})
            if queue_id.common_log_book_id and not queue_id.common_log_book_id.log_lines:
                queue_id.common_log_book_id.unlink()