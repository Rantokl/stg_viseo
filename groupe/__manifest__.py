# -*- coding: utf-8 -*-

{
    'name': "Groupe",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

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
    'depends': ['base','purchase','viseo_import_followup'],

    # always loaded
    'data': [
        #'security/ir.model.access.csv',
        'views/groupPO.xml',
        #'views/validation_po.xml',
        'views/assigned_users.xml',
        'views/smartbutton.xml',
        'views/etd_eta.xml',
        'views/statePO.xml',
        #'views/smartBROUILLON.xml',
        #'views/templates.xml',
    ],
    
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
