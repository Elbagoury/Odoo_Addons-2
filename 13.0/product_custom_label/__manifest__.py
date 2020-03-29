# Copyright 2019 VentorTech OU
# Part of Ventor modules. See LICENSE file for full copyright and licensing details.

{
    'name': 'Product Label Custome',
    "version": "13.0.1.0.0",
    'author': 'Yousuf Hussein',
    'license': 'LGPL-3',
    'installable': True,
    'summary': 'Change in the Product Label report',
    'depends': [
        'product',
    ],
    'data': [
        # 'security/ir.model.access.csv',
        'report/product_label_template.xml',
        'report/product_label.xml',
        'report/product_label_report.xml',
    ],
}
