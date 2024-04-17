# -*- coding: utf-8 -*-
{
    'name': "devis_sav",

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
    'depends': ['base','viseo_parc_auto','sale','viseo_hide_cost','sale_stock','sale_management','sale_crm','sale_margin','viseo_sale_refund'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/groups.xml',
        'views/views.xml',
        'views/test.xml',
        'views/templates.xml',
        'views/sequence.xml',
        'wizard/sale/sale_pdf.xml'
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
