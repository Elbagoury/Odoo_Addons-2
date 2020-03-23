from odoo import api, fields, models


class ResUsers(models.Model):
    _inherit = 'res.users'

    slack_channel_id = fields.Many2one(string="Slack Private Channel", comodel_name='mail.slack.channel')

    def action_slack_update_channels(self):
        self.env['mail.slack.channel'].update_channels()
