# -*- coding: utf-8 -*-
{
    'name': "Rendez-vous vehicle",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "Zo Lalaina",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','fleet','hr', 'viseo_parc_auto','viseo_repair_order'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/place_pond.xml',
        'views/atelier.xml',
        'views/sequence.xml',
        'views/table.xml',
        'views/typerdv.xml',
        'views/sale_order.xml'
        # 'views/tag_rfid.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
