# -*- coding: utf-8 -*-
##########################################################################
# Author      : Webkul Software Pvt. Ltd. (<https://webkul.com/>)
# Copyright(c): 2015-Present Webkul Software Pvt. Ltd.
# All Rights Reserved.
#
#
#
# This program is copyright property of the author mentioned above.
# You can`t redistribute it and/or modify it.
#
#
# You should have received a copy of the License along with this program.
# If not, see <https://store.webkul.com/license.html/>
##########################################################################

{
    'name': 'MOB Order Refund',
    'version': '2.4.1',
    'category': 'Generic Modules',
    'sequence': 2,
    'summary': 'Basic Sale Order Refund Module',
    'description': """
        This module allow to refund order invoice and return delivery order
        when credit memo will be generated at magento.

This module works very well with latest version of magento 2.* and Odoo 12.0
------------------------------------------------------------------------------
    """,
    'data': [
        'views/sale_view.xml',
        'views/connector_instance_view.xml',
    ],

    'author': 'Webkul Software Pvt. Ltd.',
    'website': 'https://store.webkul.com/Magento-MOB-Credit-Memo.html',
    'depends': ['odoo_magento_connect'],
    'installable': True,
    'auto_install': False,
    'pre_init_hook': 'pre_init_check',
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
