# -*- coding: utf-8 -*-
{
    'name': "FICHE TECHNIQUE",

    'summary': """
        Fiche technique pour parc auto""",

    'description': """
        PRINT PDF POUR LES DOCUMENTS RH
    """,

    'author': "My Company",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','web','sale','hr','viseo_parc_auto'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/view.xml',
        'report/report.xml',
        'report/ocentrade.xml',
        'report/continental.xml',
        'report/menu.xml',

        'views/templates.xml',
        'views/body.xml',
        

    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'auto-install':False,
    'license':'LGPL-3',
    'application':False,
    'sequence':-80,
}
