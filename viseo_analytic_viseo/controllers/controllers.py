# -*- coding: utf-8 -*-
# from odoo import http


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
