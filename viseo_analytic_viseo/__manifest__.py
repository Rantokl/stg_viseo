# -*- coding: utf-8 -*-
{
    'name': "viseo_analytic_viseo",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Analytique pour viseo
    """,

    'author': "Zo Lalaina",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','account','viseo_substitute_leave','purchase'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/sequence.xml',
        'views/tableau.xml',
        'views/template_view.xml',
        'views/analytique.xml',
        'views/templates.xml',
        'wizard/child.xml',
        'views/analytique_template.xml',
        'views/test.xml',
    ],
    'qweb':['static/src/xml/analytique.xml',
            'static/src/xml/template.xml'],
    'assets': {
        'web.assets_backend': [
            'your_module_name/static/src/js/department_percentage_widget.js',
            'viseo_analytic_viseo/static/src/js/custom_template.js',# Assurez-vous que le chemin est correct
        ],
        'web.assets_frontend': [
            'viseo_analytic_viseo/static/src/js/custom_template.js',
        ],
    },
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
