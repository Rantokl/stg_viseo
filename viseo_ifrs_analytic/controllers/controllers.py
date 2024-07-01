# -*- coding: utf-8 -*-
# from odoo import http


# class ViseoIfrsAnalytic(http.Controller):
#     @http.route('/viseo_ifrs_analytic/viseo_ifrs_analytic/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/viseo_ifrs_analytic/viseo_ifrs_analytic/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('viseo_ifrs_analytic.listing', {
#             'root': '/viseo_ifrs_analytic/viseo_ifrs_analytic',
#             'objects': http.request.env['viseo_ifrs_analytic.viseo_ifrs_analytic'].search([]),
#         })

#     @http.route('/viseo_ifrs_analytic/viseo_ifrs_analytic/objects/<model("viseo_ifrs_analytic.viseo_ifrs_analytic"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('viseo_ifrs_analytic.object', {
#             'object': obj
#         })
