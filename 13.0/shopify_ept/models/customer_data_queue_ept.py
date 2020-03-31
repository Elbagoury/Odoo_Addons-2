from odoo import models, fields, api, _

class ShopifyCustomerDataQueueEpt(models.Model):
    _name = "shopify.customer.data.queue.ept"
    _description = 'Shopify Synced Customer Data Ept'

    name = fields.Char(size=120, string='Name', readonly=True)
    shopify_instance_id = fields.Many2one('shopify.instance.ept', string='Instance')
    state = fields.Selection([('draft', 'Draft'), ('partially_completed', 'Partially Completed'),
                              ('completed', 'Completed'),('failed', 'Failed')], compute="_compute_queue_state",
                             default='draft', store=True)
    synced_customer_queue_line_ids = fields.One2many("shopify.customer.data.queue.line.ept",
                                                     "synced_customer_queue_id", "Customers")
    total_record_count = fields.Integer(string='Total Records Count',
                                        compute='_compute_total_record_count')
    draft_state_count = fields.Integer(string='Draft State Count',
                                       compute='_compute_total_record_count')
    fail_state_count = fields.Integer(string='Fail State Count',
                                      compute='_compute_total_record_count')
    done_state_count = fields.Integer(string='Done State Count',
                                      compute='_compute_total_record_count')
    cancel_state_count = fields.Integer(string='Cancel State Count',
                                        compute='_compute_total_record_count')
    common_log_book_id = fields.Many2one("common.log.book.ept", string='Log Book',
                                         help="""Related Log book which has all logs for current queue.""")
    common_log_lines_ids = fields.One2many(related="common_log_book_id.log_lines")

    @api.depends('synced_customer_queue_line_ids.state')
    def _compute_total_record_count(self):
        """
        Change the queue and queue line record state using this compute method
        :param results:
        :return:
        :author: Angel Patel @Emipro Technologies Pvt.Ltd on date 02/11/2019.
        :Task ID: 157065
        :Modify by Haresh Mori on date 25/12/2019, optimize the code
        """
        for record in self:
            queue_lines = record.synced_customer_queue_line_ids
            record.total_record_count = len(queue_lines)
            record.draft_state_count = len(queue_lines.filtered(lambda x:x.state == "draft"))
            record.done_state_count = len(queue_lines.filtered(lambda x:x.state == "done"))
            record.fail_state_count = len(queue_lines.filtered(lambda x:x.state == "failed"))
            record.cancel_state_count = len(queue_lines.filtered(lambda x:x.state == "cancel"))

    @api.depends('synced_customer_queue_line_ids.state')
    def _compute_queue_state(self):
        """
        Computes state from different states of queue lines.
        @author: Haresh Mori on Date 25-Dec-2019.
        """
        for record in self:
            if record.total_record_count == record.done_state_count + record.cancel_state_count:
                record.state = "completed"
            elif record.draft_state_count == record.total_record_count:
                record.state = "draft"
            elif record.total_record_count == record.fail_state_count:
                record.state = "failed"
            else:
                record.state = "partially_completed"

    @api.model
    def create(self, vals):
        """This method used to create a sequence for synced shopify data.
            @param : self,vals
            @author: Angel Patel @Emipro Technologies Pvt. Ltd on date 25/10/2019.
            :Task ID: 157065
        """
        seq = self.env['ir.sequence'].next_by_code('shopify.customer.data.queue.ept') or '/'
        vals.update({'name':seq or ''})
        return super(ShopifyCustomerDataQueueEpt, self).create(vals)
