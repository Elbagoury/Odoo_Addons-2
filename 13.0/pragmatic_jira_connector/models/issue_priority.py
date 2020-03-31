# -*- coding: utf-8 -*-

from odoo import api, fields, models, exceptions


class IssuePriority(models.Model):

    _name = 'issue.priority'
    _description = 'Jira Issue Priority'

    def receive_all(self):
        priority = self.env['res.company'].search([],limit=1).get('priority').json()
        for prio in priority:
            self.process_response(prio)

    def process_response(self, response):
        priority_dict = dict(
            jira_id=response['id'],
            name=response['name'],
            description=response['description'],
        )
        priority_id = self.search([('jira_id', '=', priority_dict['jira_id'])])
        if not priority_id:
            priority_id = self.create(priority_dict)
        else:
            priority_id.write(priority_dict)
        return priority_id

    def key_operation(self, id):
        priority = self.search([('jira_id', '=', id)])
        if not priority:
            priority = self.process_response(
                self.env['res.company'].search([],limit=1).get('priority/' + id).json()
            )
        return priority

    jira_id = fields.Char(required=1)
    name = fields.Char(required=1)
    description = fields.Char(required=1)
