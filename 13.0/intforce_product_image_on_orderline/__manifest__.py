
{
    'name': 'Product Image on Order Line Sales / Purchase / Invoice',
    'category': 'sale',
    'version': '13.0',
    'author': 'Intforce Software Private Limited',
    'website': 'https://intforce.co.in',
    'summary': "It will display product image in sale,purchase and invoice line, and on related report, sales order line numbering,",
    'description':
        """
- Display product image on sale and purchase order line.
- Display product image on invoice line
- Display product image on sale purchase and invoice report 
It will display product image in sale,purchase and invoice line, and on related report, sales order line numbering, product photo, product image, sale order, sale order and quotation extension with product images and line number, Sales order and Quotation extension with product images and line numbers
========================

        """,
    'depends': ['sale', 'purchase', 'account'],
    'application': True,
    'installable': True,
    'data': [
            'views/sale_view_inherit.xml',
            'views/sale_report_templates_inherit.xml',
            'views/purchase_view_inherit.xml',
            'views/purchase_order_templates_inherit.xml',
            'views/invoice_view_inherit.xml',
            'views/report_invoice_inherit.xml',
            ],
    
    "images":['static/description/Banner.png'],
	    
    'currency': 'USD',
    'price': 10.00,

}
