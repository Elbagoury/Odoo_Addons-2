from odoo import models, fields, api, _

class CommonLogBookEpt(models.Model):
    _inherit = "common.log.book.ept"

    shopify_instance_id = fields.Many2one("shopify.instance.ept", "Instance")

class CommonLogLineEpt(models.Model):
    _inherit = "common.log.lines.ept"
    shopify_product_data_queue_line_id = fields.Many2one("shopify.product.data.queue.line.ept",
                                                         "Product Queue Line")
    shopify_order_data_queue_line_id = fields.Many2one("shopify.order.data.queue.line.ept",
                                                       "Order Queue Line")
    shopify_customer_data_queue_line_id = fields.Many2one("shopify.customer.data.queue.line.ept",
                                                       "Customer Queue Line")


    def shopify_create_product_log_line(self, message, model_id, queue_line_id, log_book_id):
        """This method used to create a log line.
            @param : self, comman_log_id, message,model_id, import_data_id
            @return: log_line
            @author: Haresh Mori @Emipro Technologies Pvt. Ltd on date 22/10/2019.
        """
        vals = {'message':message,
                'model_id':model_id,
                'res_id':queue_line_id.id if queue_line_id else False,
                'shopify_product_data_queue_line_id':queue_line_id.id if queue_line_id else False,
                'log_line_id' : log_book_id.id if log_book_id else False
                }
        log_line = self.create(vals)
        return log_line

    def shopify_create_order_log_line(self, message, model_id, queue_line_id,log_book_id):
        """This method used to create a log line.
            @param : self, message, model_id, queue_line_id
            @return: log_line
            @author: Haresh Mori @Emipro Technologies Pvt. Ltd on date 11/11/2019.
        """
        vals = {'message':message,
                'model_id':model_id,
                'res_id':queue_line_id and queue_line_id.id or False,
                'shopify_order_data_queue_line_id':queue_line_id and queue_line_id.id or False,
                'log_line_id': log_book_id.id if log_book_id else False,
                }
        log_line = self.create(vals)
        return log_line

    def shopify_create_customer_log_line(self,message, model_id, queue_line_id,log_book_id):
        vals = {'message': message,
                'model_id': model_id,
                'res_id': queue_line_id and queue_line_id.id or False,
                'shopify_customer_data_queue_line_id': queue_line_id and queue_line_id.id or False,
                'log_line_id': log_book_id.id if log_book_id else False,
                }
        log_line = self.create(vals)
        return log_line

