# -*- coding: utf-8 -*-

from odoo import api, fields, models, exceptions


class JiraProjectType(models.Model):

    _name = 'jira.type'
    _description = 'Jira Project Type'

    def receive_all(self):
        response = self.env['res.company'].search([],limit=1).get('project/type').json()
        for pt in response:
            self.process_response(pt)

    def process_response(self, response):
        project_type_dict = dict(
            key=response['key'],
            name=response['formattedKey'],
            description=response['descriptionI18nKey'],
        )
        project_type = self.env['jira.type'].search([('key', '=', response['key'])])
        if not project_type:
            project_type = self.env['jira.type'].create(project_type_dict)
        else:
            project_type.write(project_type_dict)
        return project_type

    def key_operation(self, key):
        project_type = self.search([('key', '=', key)])
        if not project_type:
            response = self.env['res.company'].search([],limit=1).get('project/type/' + key).json()
            project_type = self.process_response(response)
        return project_type

    name = fields.Char(required=1)
    key = fields.Char(required=1)
    description = fields.Char()
