{
    'name': 'Bank Cheque Print BD',    
    'summary': ''' 
            Apps will create Accounting Vendors Payment Cheque Print 
        ''',
    "description": """This module will Print Vendors Payment Cheque """,
    'author': 'Metamorphosis',
    'company': 'Metamorphosis Limited',
    'license': 'AGPL-3',
    'website': 'http://metamorphosis.com.bd/',
    'category': 'Accounting',
    'sequence': 1,
    'version': '13.0.1.0.0',
    'depends': [
        'base', 'account', 'account_check_printing',
    ],
    'data': [
        
        'views/account_payment_check_button.xml',
        'views/print_check_wizard_view.xml',
        'reports/report.xml',
        'reports/payment_report.xml',
        'views/check_number_search_view.xml',
        
    ],
    'icon': "/bank_cheque_print_bd/static/description/icon.png",
    "images": ["static/description/banner.png"],
    'installable': True,
    "auto_install": False,
    'price':99.0,
    'currency':'EUR',
}