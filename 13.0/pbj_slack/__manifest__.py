{
    'name': "Slack Integration",
    'version': '13.0.2.0.0',
    'author': "Jake Robinson",
    'website': "https://programmedbyjake.com",
    'category': 'Integration',
    'summary': "Automated Slack Message from Odoo",
    'description': "Use Odoo's automated action feature to send custom message to your Slack. TEST",
    'depends': [
        'base',
        'base_automation',
    ],
    'data': [
        'data/ir_actions_server.xml',

        'security/ir.model.access.csv',

        'views/ir_actions_server.xml',
        'views/mail_slack_channel.xml',
        'views/mail_slack_message.xml',
        'views/res_users.xml',

        'views/menus.xml',
    ],
    'images': [
        'static/description/banner.png',
    ],
    'external_dependencies': {
        'python': [
            'slack'
        ]
    },
    'application': False,
    'installable': True,

    'license': 'OPL-1',
    'price': 300,
    'currency': 'EUR',
    'support': 'support@programmedbyjake.com',
}
