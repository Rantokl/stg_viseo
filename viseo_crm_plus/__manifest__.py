# -*- coding: utf-8 -*-
{
    'name': "viseo_crm_plus",

    'summary': """
       The new CRM""",

    'description': """
        Long description of module's purpose
    """,

    'author': "My Company",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','crm','mail','portal','sale', 'viseo_stock', 'sale_management', 'viseo_repair_order'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/crm.xml',
        #'views/viseo_crm.xml',
        #'views/sale_order.xml',
        'views/pop_up.xml',
        'views/email.xml',
        'views/other.xml',
        'views/social_media.xml',
        'views/telephone.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
