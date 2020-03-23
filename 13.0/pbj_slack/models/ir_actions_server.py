from odoo import api, fields, models
from odoo.exceptions import UserError

from mako.template import Template as mako_template


class IrActionsServer(models.Model):
    _inherit = 'ir.actions.server'

    state = fields.Selection(selection_add=[('slack', "Send Slack Message")])
    slack_channel_type = fields.Selection(string="Slack Type", default='channel', selection=[
        ('channel', "Message Channel"),
        ('user', "Direct Message User"),
    ])
    slack_channel_id = fields.Many2one(string="Slack Channel", comodel_name='mail.slack.channel')
    slack_user_field_id = fields.Many2one(string="Slack User Field", comodel_name='ir.model.fields')
    slack_message = fields.Text(string="Slack Message")

    def run_action_slack(self, action, eval_context=None):
        """Create a new slack message based on the context"""
        eval_context = eval_context or {}
        message = mako_template(self.slack_message or '').render(**eval_context)
        channel = False
        if self.slack_channel_type == 'channel':
            channel = self.slack_channel_id
        elif self.slack_channel_type == 'user':
            record = eval_context.get('record')
            if record:
                field = self.slack_user_field_id
                if field:
                    user = getattr(record, field.name)
                    if user:
                        channel = user.slack_channel_id
        else:
            raise UserError("An automated slack action requires a slack type.")
        if channel:
            self.env['mail.slack.message'].send_message(channel, message)

    def action_update_channels(self):
        """Update the slack channel list"""
        self.env['mail.slack.channel'].update_channels()
