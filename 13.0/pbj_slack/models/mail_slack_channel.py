from odoo import api, fields, models
from odoo.exceptions import AccessError, ValidationError

import slack


class MailSlackChannel(models.Model):
    _name = 'mail.slack.channel'
    _description = 'Slack Channel'

    active = fields.Boolean(string="Active", default=True)
    name = fields.Char(string="Name", required=True)
    code = fields.Char(string="Code", required=True)
    topic = fields.Char(string="Topic")
    member_count = fields.Integer(string="Member Count")
    private = fields.Boolean(string="Private")
    type = fields.Selection(string="Type", required=True, default='channel', selection=[
        ('channel', "Channel"),
        ('user', "User"),
    ])

    @api.model
    def update_channels(self):
        """Syncs channel data from slack, creating, updating and deleting as required."""

        # Connect to Slack
        client = slack.WebClient(token=self.env['mail.slack.message'].get_slack_token())

        # Get Channels
        try:
            conversations = client.conversations_list(limit=1000)  # Slack does not allow limit greater than 1000
        except slack.errors.SlackApiError:
            raise AccessError("Connection to Slack Failed, please check your bot token and firewall settings.")
        if not hasattr(conversations, 'data') or 'channels' not in conversations.data:
            raise ValidationError("Slack returned malformed data.")

        # Get Users
        try:
            users = client.users_list(limit=1000)  # Slack does not allow limit greater than 1000
        except:
            raise AccessError("Connection to Slack Failed, please check your bot token and firewall settings.")
        if not users.get('members'):
            raise ValidationError("Slack returned malformed data.")

        # Gather a dataset of all channels on Slack.
        slack_data = {}
        slack_channels = conversations.data['channels']
        for channel in slack_channels:
            slack_data.update({channel['id']: {
                'code': channel['id'],
                'name': channel['name'],
                'active': not channel['is_archived'],
                'topic': channel['topic']['value'],
                'member_count': channel['num_members'],
                'private': channel['is_private'],
                'type': 'channel'
            }})
        slack_members = users.get('members')
        for member in slack_members:
            slack_data.update({member['id']: {
                'code': member['id'],
                'name': "Private: {}".format(member['name']),
                'active': not member['deleted'],
                'topic': "Private Channel with {}".format(member.get('real_name', member.get('name', 'Unknown'))),
                'member_count': 1,
                'private': True,
                'type': 'user'
            }})
        slack_keys = set(slack_data.keys())

        # Gather a matching dataset of existing channels
        odoo_data = {}
        odoo_channels = self.with_context(active_search=False).search_read([], ['name', 'code', 'active', 'topic', 'member_count', 'private'])
        for channel in odoo_channels:
            odoo_data.update({channel['code']: {
                'code': channel['code'],
                'name': channel['name'],
                'active': channel['active'],
                'topic': channel['topic'],
                'member_count': channel['member_count'],
                'private': channel['private'],
            }})
        odoo_keys = set(odoo_data.keys())

        # Delete any channels that no longer exist in Slack
        to_delete = odoo_keys - slack_keys
        self.search([('code', 'in', list(to_delete))]).sudo().unlink()

        # Add any channels that don't yet exist in Odoo
        to_add = slack_keys - odoo_keys
        for key in to_add:
            self.sudo().create(slack_data[key])

        # Update any channels in Odoo if they differ from the Slack data
        to_update = odoo_keys.intersection(slack_keys)
        for key in to_update:
            channel_datum = slack_data[key]
            existing_datum = odoo_data[key]
            differences = {k: channel_datum[k] for k in existing_datum.keys() if channel_datum[k] != existing_datum[k]}
            if differences:
                self.with_context(active_search=False).search([('code', '=', key)]).sudo().write(differences)

# esto es una prueba