# -*- coding: utf-8 -*-

{
    'name': 'Product pack',
    'version': '13.0',
    'category': 'Product',
    'sequence': 6,
#     'author': 'Webveer',
    'website': 'http://www.pptssolutions.com',
    'author': 'PPTS [India] Pvt.Ltd.',
    'summary': 'Allows you to create pack product in Odoo.',
    'description': "Allows you to create pack product in Odoo.",
    'depends': ['product'],
    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
        # 'views/templates.xml'
    ],
    'qweb': [
        # 'static/src/xml/pos.xml',
    ],
#     'images': [
#         'static/description/product.jpg',
#     ],
    'installable': True,
    'application': True,
    'auto_install': False,
#     'website': '',
#     'price': 10,
#     'currency': 'EUR',
}
