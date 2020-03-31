# -*- coding: utf-8 -*-

from odoo import api, fields, models, exceptions


class IssueStatus(models.Model):

    _inherit = 'project.task.type'

    def receive_all(self):
        status = self.env['res.company'].search([],limit=1).get('status').json()
        for s in status:
            self.process_response(s)

    def process_response(self, response):
        status_dict = dict(
            jira_id=response['id'],
            name=response['name'],
            description=response['description'],
            category_id=self.env['issue.status.category'].key_operation(response['statusCategory']['key']).id,
        )
        status = self.search([('jira_id', '=', status_dict['jira_id'])])
        if not status:
            status = self.create(status_dict)
        else:
            status.write(status_dict)
        return status

    def key_operation(self, id):
        status = self.search([('jira_id', '=', id)])
        if not status:
            status = self.process_response(
                self.env['res.company'].search([],limit=1).get('status/' + id).json()
            )
        return status

    def jira_dict(self, status_dict):
        status = self.search([('jira_id', '=', status_dict['id'])])
        if not status:
            status = self.process_response(status_dict)
        return status

    jira_id = fields.Char()
    category_id = fields.Many2one('issue.status.category')
