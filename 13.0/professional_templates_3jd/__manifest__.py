# -*- coding: utf-8 -*-

{
    'name': '3JD Professionnal Templates',
    'author': 'Hodei',
    'version': '1.0.0',
    'category': 'Advanced Reporting',
    'sequence': 6,
    'summary': 'Add custom template for 3JD to professionnal templates',
    'description': """
        This module add several custom reports to professional templates:\n
    """,
    'depends': [
        'hodei_move_price',
        'professional_templates'],
    'website': '',
    'data': [
        'views/classic_template.xml',
        'views/company_address.xml',
        'views/company_address_noname.xml',
        'views/company_footer.xml',
        'views/delivery_lines.xml',
        'views/delivery_tva_template.xml',
        'views/invoice_lines.xml',
        'views/modern_template.xml',
        'views/order_lines.xml',
        'views/picking_lines.xml',
        'views/picking_tva_template.xml',
        'views/purchase_cubic_template.xml',
        'views/purchase_lines.xml',
        'views/rfq_cubic_template.xml',
        'views/rfq_lines.xml'
    ],
    'qweb': [
    ],
    'demo': [
    ],
    'installable': True,
    'auto_install': False,
}
