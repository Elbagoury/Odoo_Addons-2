from odoo import api, fields, models
from odoo.exceptions import MissingError, UserError

import os

import slack


class MailSlackMessage(models.Model):
    _name = 'mail.slack.message'
    _description = "Slack Message"

    user_id = fields.Many2one(string="Sender", comodel_name='res.users')
    channel_id = fields.Many2one(string="Channel", comodel_name='mail.slack.channel', ondelete="set null")
    content = fields.Text(string="Message")
    sent = fields.Boolean(string="Message Sent")

    @api.model
    def create(self, vals):
        """Attempt to send the message when created"""
        # TODO: Create cron to attempt to send failed messages
        res = super(MailSlackMessage, self).create(vals)
        res.try_send()
        return res

    @api.model
    def get_slack_token(self):
        """Get the slack token, using environment variables followed by config parameters"""
        token = os.getenv('SLACK_BOT_TOKEN', self.env['ir.config_parameter'].sudo().get_param('SLACK_BOT_TOKEN'))
        if not token:
            raise UserError("Slack API token not found.\nPlease add an environment variable or system parameter for SLACK_BOT_TOKEN.")
        return token

    @api.model
    def get_slack_signing_secret(self):
        """Get the slack signing secret, using environment variables followed by config parameters"""
        token = os.getenv('SLACK_SIGNING_SECRET', self.env['ir.config_parameter'].sudo().get_param('SLACK_SIGNING_SECRET'))
        if not token:
            raise UserError("Slack Signing token not found.\nPlease add an environment variable or system parameter for SLACK_SIGNING_SECRET.")
        return token

    @api.model
    def send_message(self, channel, message):
        """Create a new message to send"""
        if not channel:
            raise MissingError("Channel is required to send Slack Message")
        if not message:
            raise MissingError("A message is required to send")

        self.sudo().create({
            'channel_id': channel.id,
            'content': message,
            'user_id': self.env.user.id,
        })

    def try_send(self):
        """Attempt to send the message, but don't raise the exception if an error occurs"""
        for rec in self:
            try:
                client = slack.WebClient(token=self.get_slack_token())
                client.chat_postMessage(
                    channel=rec.channel_id.code,
                    text=rec.content,
                )
            except:
                pass
            else:
                rec.sent = True
