# noinspection PyStatementEffect
{
    'name': "Multi-Company Email",

    'sequence': 202,

    'summary': """ Changes user's email and signature to the ones defined in the current company """,

    'author': "Arxi",
    'website': "http://www.arxi.pt",

    'category': 'Extra Tools',
    'version': '13.0.0.0.1',
    'license': 'OPL-1',

    'price': 24.99,
    'currency': 'EUR',

    'depends': ['base'],

    'data': [
        'views/templates.xml',
    ],

    'images': [
        # 'static/description/banner.png',
    ],

    'application': True,
    'installable': True,
}
