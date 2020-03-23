# -*- coding: utf-8 -*-
{
    'name': 'Website Delivery Duration Drc',
    'summary': 'Allow to customer pick a date and drop a message on confirm sale order.',
    'description': '''
            Allows to enter date and leave a message on website and it\'s managing can be done in sale order,
            stock picking and invoice.
        ''',
    'author': 'DRC Systems India Pvt. Ltd.',
    'website': 'www.drcsystems.com',
    'version': '1.3',
    'category': 'eCommerce',
    'depends': ['sale', 'sale_management', 'stock', 'website_sale', 'account'],
    'data': [
        'report/invoice_report.xml',
        'report/picking_report.xml',
        'report/sale_report.xml',
        'views/account_invoice_views.xml',
        'views/sale_order_views.xml',
        'views/stock_picking_views.xml',
        'views/templates.xml',
    ],
    'images': ['static/src/img/delivery-on-order.jpg'],
    'currency': 'EUR',
    'price': 35,
    'support': 'support@drcsystems.com',
}
