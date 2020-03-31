{
    "name": "Customized POS Receipt / POS Customized Receipt with Company Name, Logo, Customer details in POS Receipt and Reprint POS Receipt From Pos Order",
    "version": "13.0.2",
    "description": """
        print pos receipt from pos order Backend side.and also add company logo and customer detail in pos receipt.
    """,
    'price': 11,
    'currency': 'EUR',
    'license': 'OPL-1',
    "author" : "MAISOLUTIONSLLC",
    'sequence': 1,
    "email": 'apps@maisolutionsllc.com',
    "website":'http://maisolutionsllc.com/',
    'category':"Point of Sale",
    'summary':"RePrint POS Receipt From Pos Order Add Company Logo and Customer Detail in Pos Receipt.",
    "depends": [
        "base",
        "point_of_sale",
    ],
    "data": [
         'report/report_paperformat.xml', 
        'report/pos_report_template.xml',
        'report/pos_order.xml',
    ],
    'qweb': [
        'static/src/xml/pos_receipt.xml',
    ],
    'css': [],
    'js': [],
    'images': ['static/description/main_screenshot.png'],
    'demo': [],
    'installable': True,
    'auto_install': False,
    'application': True,
}

