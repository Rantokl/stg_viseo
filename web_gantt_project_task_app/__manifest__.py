# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Web Ganttt viseo',
    'category': 'Hidden',
    'description': """
Odoo Web Gantt chart view viseo.
=============================

""",
    "version" : "13.0.1.0",
    "depends": ['web', 'viseo_project_project'],
    "data": [
        'views/web_gantt_templates.xml',
        'views/web_gantt_project_task_app_view.xml',
        'views/inherited_form_view.xml',
    ],
    'qweb': [
        'static/src/xml/web_gantt.xml',
    ],
    'auto_install': False,
    "license": "GPL-3",
}



# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
