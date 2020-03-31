# -*- coding: utf-8 -*-

from odoo import fields, models
from dateutil import parser
import base64

class Attachment(models.Model):

    _inherit = 'ir.attachment'

    # Unlink attachment from odoo .
    def unlink(self):
        jira_id = self.jira_id
        output = super(Attachment, self).unlink()
        if jira_id:
            self.env['res.company'].search([],limit=1).delete('attachment/' + jira_id)
        return output
    # Create attachment while importing issues.
    def while_import_attachemnt(self, issue, response):
        if not self.search([('jira_id', '=', response['id'])]):
            created_date =parser.parse(response['created']).strftime("%Y-%m-%d %H:%M:%S")
            created_date = parser.parse(created_date)
            resp = self.env['res.company'].search([],limit=1).get_file(response['content']).content
            self.create(dict(datas=base64.b64encode(resp),
                name=response['filename'],
                res_model='project.task',
                res_id=issue.id,
                jira_id=response['id'],
                issue_id=issue.id,
                author_id=self.env['res.users'].get_user_by_dict(response['author']).id,
            ))

    jira_id = fields.Char(string='Jira ID')
    issue_id = fields.Many2one('project.task')
    author_id = fields.Many2one('res.users')
