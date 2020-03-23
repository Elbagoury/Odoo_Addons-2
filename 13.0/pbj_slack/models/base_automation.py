from odoo import api, fields, models


class BaseAutomation(models.Model):
    _inherit = 'base.automation'

    def action_update_channels(self):
        """Update the slack channel list"""
        self.env['mail.slack.channel'].update_channels()
