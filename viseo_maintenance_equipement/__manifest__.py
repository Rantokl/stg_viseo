# -*- coding: utf-8 -*-
{
    'name': "viseo_maintenance_equipement",

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
    'depends': ['base','mail','purchase','uom','viseo_sale','viseo_repair_order','viseo_repair'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/group.xml',
        'views/views.xml',
        'views/templates.xml',
        'views/sequence.xml',
        'views/expense.xml',
        'views/prelevement.xml',
        'wizard/invoice.xml',
        'wizard/additive_need.xml',
        'wizard/quotation_refuse.xml',
        'views/contrat.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
