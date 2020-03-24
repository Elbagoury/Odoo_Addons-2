# Copyright 2020 Niraj Pajwani
{
    'name': 'Force delete invoices',
    'summary': 'Force delete invoices and payments',
    'version': '13.0.1.0.0',
    'category': 'Accounting',

    'description': """
Force delete invoices
===========================
- Allows to force delete invoices and related payments
    """,

    'author': "Niraj Pajwani",
    'depends': ['account'],
    'data': [
        'views/account_move_view.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': False,
}
