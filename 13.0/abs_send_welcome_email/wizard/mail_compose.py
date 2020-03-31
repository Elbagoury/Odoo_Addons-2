# -*- coding: utf-8 -*-
#################################################################################
#
#    Odoo, Open Source Management Solution
#    Copyright (C) 2019-today Ascetic Business Solution <www.asceticbs.com>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#################################################################################
from odoo import api, fields, models,_

#create a new class for wizared view
class MailCompose(models.TransientModel):
    _name = "mail.compose"
    _description = 'Mail Compose'

    partner_ids = fields.Many2many('res.partner',string='Recipients')
    subject = fields.Char("Subject" )
    description = fields.Text("Description") 

    #create a function for update data in fields. 
    @api.model
    def default_get(self, fields):
        rec = super(MailCompose, self).default_get(fields)
        current_login_user = self.env.user  
        active_ids = self._context.get('active_ids')
        partner = self.env['res.partner'].browse(active_ids)
        if partner:
            test_table = " Dear {0},<br><br><p>Here is your Welcome Email.<br><br>Thank You.<br>{1}".format(partner.name,current_login_user.name)
            rec.update({'partner_ids': [(6, 0, partner.ids)],'subject':'Welcome Email','description':test_table})
        return rec

    #method to cretae and send the mail to new customer.
    def send_email(self):
        current_login_user = self.env.user  
        email_subject = self.subject
        email_description = self.description
        partner_list = []
        mail_dict = {}
        for record in self:
            for partner_id in record.partner_ids:
                if partner_id:
                    partner_list.append(partner_id.id)  
        if partner_list:
            mail_dict ={
                        'subject'       : email_subject,
                        'email_from'    : current_login_user.email,
                        'recipient_ids' : [(6,0,partner_list)],
                        'body_html'     : email_description,                  
                        }
            if mail_dict:
                mail_id = current_login_user.env['mail.mail'].create(mail_dict)
            if mail_id:
                mail_id.send()
