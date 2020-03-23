{
    #Product Info
    'name': 'Import Stock Inventory Adjustment From Xlsx/Xls/CSV',
    'version': '1.0',
    'license': 'OPL-1',    
    'category': 'stock',
    'summary' : 'Import Stock Inventory Adjustment Which Help You To Adjust Your Inventory Adjustments With In Few Minutes. You Can Prepare The Xlsx/Xls/CSV File For The Import Time.',
    
    #Writer
    'author': 'YoungWings Technologies',
    'maintainer': 'YoungWings Technologies',
    
    #Dependencies
    'depends': ['stock'],
    
    #View
    'data': [
            'security/ir.model.access.csv',
            'data/stock_invenotry_seq.xml',
            'wizard/ywt_import_stock_inventory_views.xml',
            'view/ywt_import_stock_inventory_log_views.xml'],
              
     
    #Banner     
    "images": ["static/description/banner.png"],
    
    #Technical 
    'installable': True,
    'auto_install': False,
    'application' : True,
    'price':10,
    'currency': 'EUR'
    
}
