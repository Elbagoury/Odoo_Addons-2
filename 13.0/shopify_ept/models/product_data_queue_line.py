from odoo import models, fields, api, _
from datetime import datetime, timedelta

class ShopifyProductDataqueueLineEpt(models.Model):
    _name = "shopify.product.data.queue.line.ept"
    _description = 'Shopify Product Data Queue Line Ept'

    shopify_instance_id = fields.Many2one('shopify.instance.ept', string='Instance')
    last_process_date = fields.Datetime('Last Process Date', readonly=True)
    synced_product_data = fields.Text(string='Synced Product Data')
    product_data_id = fields.Char(string='Product Data Id')
    state = fields.Selection([('draft', 'Draft'), ('failed', 'Failed'), ('done', 'Done'),
                              ("cancel","Cancelled")],
                             default='draft')
    product_data_queue_id = fields.Many2one('shopify.product.data.queue.ept',
                                            string='Product Data Queue', required=True,
                                            ondelete='cascade', copy=False)
    common_log_lines_ids = fields.One2many("common.log.lines.ept",
                                           "shopify_product_data_queue_line_id",
                                           help="Log lines created against which line.")
    name = fields.Char(string="Product", help="It contain the name of product")

    def auto_start_child_process_for_product_queue(self):
        """This method used to start the child process cron for process the product queue line data.
            @param : self
            @return: True
            @author: Haresh Mori @Emipro Technologies Pvt.Ltd on date 25/10/2019.
        """
        child_product_cron = self.env.ref('shopify_ept.ir_cron_child_to_process_product_queue_line')
        if child_product_cron and not child_product_cron.active:
            results = self.search([('state', '=', 'draft')], limit=100)
            if not results:
                return True
            child_product_cron.write({'active':True,
                                      'numbercall':1,
                                      'nextcall':datetime.now() + timedelta(seconds=10)
                                      })
        return True

    def auto_import_product_queue_line_data(self):
        """- This method used to process synced shopify product data in batch of 100 queue lines.
           - This method is called from cron job.
            @param : self
            @author: Haresh Mori @Emipro Technologies Pvt.Ltd on date 05/10/2019.
            Task_id : 157110
        """
        # change by bhavesh jadav 03/12/2019 for process  only one queue data at a time
        query = """select product_data_queue_id from shopify_product_data_queue_line_ept where state='draft' ORDER BY create_date ASC limit 1"""
        self._cr.execute(query)
        product_data_queue_id = self._cr.fetchone()
        product_data_queue_line_ids = self.env['shopify.product.data.queue.ept'].browse(product_data_queue_id).product_data_queue_lines
        product_data_queue_line_ids.process_product_queue_line_data()


    def process_product_queue_line_data(self):
        """
            -This method processes product queue lines.
             @param : self
             @author: Haresh Mori @Emipro Technologies Pvt.Ltd on date 05/10/2019.
             Task_id : 157110
         """
        shopify_product_template_obj = self.env['shopify.product.template.ept']
        comman_log_obj = self.env["common.log.book.ept"]
        shopify_tmpl_id = False

        product_queue_dict = {}
        queue_id = self.product_data_queue_id if len(self.product_data_queue_id) == 1 else False
        if queue_id:
            if queue_id.common_log_book_id:
                log_book_id=queue_id.common_log_book_id
            else:
                log_book_id=comman_log_obj.create({'type': 'import',
                                                   'module':'shopify_ept',
                                                   'shopify_instance_id':queue_id.shopify_instance_id.id,
                                                   'active':True})
            commit_count = 0
            for product_queue_line in self:
                commit_count += 1
                shopify_product_template_obj.shopify_sync_products(product_queue_line,shopify_tmpl_id,
                                                                       product_queue_line.shopify_instance_id,log_book_id)
                if commit_count == 10:
                    self._cr.commit()
                    commit_count = 0
            queue_id.common_log_book_id = log_book_id
            # draft_or_failed_queue_line = self.filtered(lambda line: line.state in ['draft', 'failed'])
            # if draft_or_failed_queue_line:
            #     queue_id.write({'state': "partially_completed"})
            # else:
            #     queue_id.write({'state': "completed"})
            if queue_id.common_log_book_id and not queue_id.common_log_book_id.log_lines:
                queue_id.common_log_book_id.unlink()
            return True
