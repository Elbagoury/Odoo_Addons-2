# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.
{
    "name" : "Website Category Page",
    
    "author" : "Softhealer Technologies",
        
    "website": "https://www.softhealer.com",
    
    "support": "support@softhealer.com",

    "version": "13.0.1",

    "category": "eCommerce",
    
    "summary": "This module useful to show product category page.",
    
    "description": """This module useful to show category page for shop.
       Are you running the store with a large catalog of products? Wanna bring store usability to a new high level? This module is useful to show the category page for the shop. It provides easy catalog images to make the display of categories list more presentable. Grab user's attention on your store page, providing them with the immediate loadable categories listing. The default odoo category bar in the shop doesn't provide a user-friendly way to browse catalogs. Our extension allows you to use better navigation displaying all categories list on the category page. Our module is also useful to show the category name heading in the category page.
        Easy for customer to navigate different category.
        Shop Category page, Category page, E-commerce Category page, Odoo Category Page, Website Category page, 
        Shop Catalog page, Catalog page, E-commerce Catalog page, Odoo Catalog Page, Website Catalog page""",
        
    "depends" : ['website', 'website_sale'],
    
    "data" : [  
            'views/website_config_settings.xml',
            'views/website_product_category.xml',
            'views/website_shopby_category.xml',
            'data/website_category_menu.xml',
            ],
    
    "images": ['static/description/background.png', ],
                  
    "auto_install":False,
    "application" : True,
    "installable" : True,
    
    "price": 25,
    "currency": "EUR"   
}
