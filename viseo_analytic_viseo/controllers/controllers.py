# -*- coding: utf-8 -*-
# from odoo import http

from odoo import http
from odoo.http import request

class ViseoAnalytiqueController(http.Controller):
    @http.route('/get_dynamic_table_data', type='json', auth='user')
    def get_dynamic_table_data(self):
        data = request.env['viseo.analytique.view'].get_dynamic_table_data()
        return data


# class ViseoAnalytic(http.Controller):
#     @http.route('/viseo_analytic/viseo_analytic/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/viseo_analytic/viseo_analytic/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('viseo_analytic.listing', {
#             'root': '/viseo_analytic/viseo_analytic',
#             'objects': http.request.env['viseo_analytic.viseo_analytic'].search([]),
#         })

#     @http.route('/viseo_analytic/viseo_analytic/objects/<model("viseo_analytic.viseo_analytic"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('viseo_analytic.object', {
#             'object': obj
#         })
