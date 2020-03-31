from datetime import datetime, timedelta
import logging
from odoo import models, fields
from odoo.addons.shopify_ept.shopify.pyactiveresource.util import xml_to_dict
import json

_logger = logging.getLogger("Shopify_queue_process===(Emipro): ")


class ShopifyOrderDataQueueLineEpt(models.Model):
    _name = "shopify.order.data.queue.line.ept"
    _description = "Shopify Order Data Queue Line EPT"

    shopify_order_data_queue_id = fields.Many2one("shopify.order.data.queue.ept", ondelete='cascade')
    shopify_instance_id = fields.Many2one('shopify.instance.ept', string='Instance',
                                          help="Order imported from this Shopify Instance.")
    state = fields.Selection([("draft", "Draft"), ("failed", "Failed"), ("done", "Done"),
                              ("cancel","Cancelled")],default="draft", copy=False)
    shopify_order_id = fields.Char(help="Id of imported order.", copy=False)
    sale_order_id = fields.Many2one("sale.order", copy=False,
                                    help="Order created in Odoo.")
    order_data = fields.Text(help="Data imported from Shopify of current order.", copy=False)
    # shopify_product = fields.Text(help="Shopify Product Name", copy=False)
    customer_name= fields.Text(string="Customer Name" ,help="Shopify Customer Name", copy=False)

    customer_email = fields.Text(string="Customer Email",help="Shopify Customer Email", copy=False)

    processed_at = fields.Datetime(help="Shows Date and Time, When the data is processed",
                                   copy=False)
    shopify_order_common_log_lines_ids = fields.One2many("common.log.lines.ept",
                                                         "shopify_order_data_queue_line_id",
                                                         help="Log lines created against which line.")
    name = fields.Char(string='Name', help="Order Name")

    def create_order_data_queue_line(self, order_ids, instance):
        """This method used to create order data queue lines. it's split the queue after 50 order queue lines
            @param : order_ids, instance
            @author: Haresh Mori @Emipro Technologies Pvt. Ltd on date 06/11/2019.
            Task Id : 157350
        """
        count = 0
        one_time_create = True
        order_ids.reverse()
        order_queue_list = []
        for order_id in order_ids:
            if one_time_create:
                order_queue_id = self.shopify_create_order_queue(instance)
                order_queue_list.append(order_queue_id.id)
                _logger.info('Shopify Order Queue created. Queue name is  {}'.format(
                    order_queue_id.name))
                one_time_create = False
            order_queue_line_vals = {}
            result = xml_to_dict(order_id.to_xml())
            try:
                customer_name = "%s %s" % (result.get('order').get('customer').get('first_name'), result.get('order').get('customer').get('last_name'))
                customer_email = result.get('order').get('customer').get('email')
                if customer_name == 'None None':
                    customer_name = result.get('order').get('customer').get('default_address').get('name')
            except:
                customer_name=False
                customer_email=False

            data = json.dumps(result)
            order_queue_line_vals.update(
                {'shopify_order_id': result.get('order').get('id') if result.get('order') else False,
                 'shopify_instance_id': instance and instance.id or False,
                 'order_data': data,
                 'name': result.get('order').get('name') or '',
                 'customer_name': customer_name,
                 'customer_email':customer_email,
                 'shopify_order_data_queue_id': order_queue_id and order_queue_id.id or False,
                 'state': 'draft'})
            self.create(order_queue_line_vals)
            count = count + 1
            if count == 50:
                count = 0
                one_time_create = True
        return order_queue_list

    def shopify_create_order_queue(self, instance):
        """This method used to create a order queue as per the split requirement of the
        queue. It is used for process the queue manually.
            @param : self, insatnce.
            @author: Haresh Mori @Emipro Technologies Pvt. Ltd on date 11/11/2019.
            Task Id :
        """
        oredr_queue_vals = {
            'shopify_instance_id': instance and instance.id or False,
            'state': 'draft',
        }
        order_queue_data_id = self.env["shopify.order.data.queue.ept"].create(oredr_queue_vals)

        return order_queue_data_id

    def auto_start_child_process_for_order_queue(self):
        """This method used to start the child process cron for process the order queue line data.
            @param : self
            @return: True
            @author: Haresh Mori @Emipro Technologies Pvt.Ltd on date 07/10/2019.
        """
        child_order_queue_cron = self.env.ref(
            'shopify_ept.ir_cron_child_to_process_order_queue')
        if child_order_queue_cron and not child_order_queue_cron.active:
            results = self.search([('state', '=', 'draft')], limit=100)
            if not results:
                return True
            child_order_queue_cron.write({'active': True,
                                          'numbercall': 1,
                                          'nextcall': datetime.now() + timedelta(seconds=10)
                                          })
        return True

    def auto_import_order_queue_data(self):
        """- This method used to process synced shopify order data in batch of 50 queue lines.
           - This method is called from cron job.
            @param : self
            @author: Haresh Mori @Emipro Technologies Pvt.Ltd on date 07/10/2019.
            Task Id : 157350
        """
        # change by bhavesh jadav 02/12/2019 for process  only one queue data at a time
        query = """select shopify_order_data_queue_id from shopify_order_data_queue_line_ept where state='draft' ORDER BY create_date ASC limit 1"""
        self._cr.execute(query)
        order_queue_id = self._cr.fetchone()
        order_data_queue_line_ids = self.env['shopify.order.data.queue.ept'].browse(
            order_queue_id).order_data_queue_line_ids.filtered(lambda x:x.state == 'draft')
        order_data_queue_line_ids.process_import_order_queue_data()

    def process_import_order_queue_data(self):
        """
             -This method processes order queue lines.
            @param : self
            @author: Haresh Mori @Emipro Technologies Pvt.Ltd on date 07/10/2019.
            Task Id : 157350
        """
        sale_order_obj = self.env['sale.order']
        comman_log_obj = self.env["common.log.book.ept"]
        order_queue_dict = {}
        queue_id = self.shopify_order_data_queue_id if len(self.shopify_order_data_queue_id) == 1 else False
        if queue_id:
            if queue_id.shopify_order_common_log_book_id:
                log_book_id = queue_id.shopify_order_common_log_book_id
            else:
                log_book_id = comman_log_obj.create({'type': 'import',
                                                     'module': 'shopify_ept',
                                                     'shopify_instance_id': queue_id.shopify_instance_id.id,
                                                     'active': True})
            commit_count = 0
            for order_queue_line in self:
                commit_count += 1
                if commit_count == 5:
                    # This is used for commit every 5 orders
                    self._cr.commit()
                    commit_count = 0
                sale_order_obj.import_shopify_orders(order_queue_line, log_book_id)
            queue_id.shopify_order_common_log_book_id = log_book_id
            # draft_or_failed_queue_line = self.filtered(lambda line: line.state in ['draft', 'failed'])
            # if draft_or_failed_queue_line:
            #     queue_id.write({'state': "partially_completed"})
            # else:
            #     queue_id.write({'state': "completed"})
            if queue_id.shopify_order_common_log_book_id and not queue_id.shopify_order_common_log_book_id.log_lines:
                queue_id.shopify_order_common_log_book_id.unlink()
            if queue_id.shopify_instance_id.is_shopify_create_schedule:
                self.env['shopify.order.data.queue.ept'].create_schedule_activity(queue_id)
            return True
