# -*- coding: utf-8 -*-
# from odoo import http


# class ViseoCustomDashboard(http.Controller):
#     @http.route('/viseo_custom_dashboard/viseo_custom_dashboard/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/viseo_custom_dashboard/viseo_custom_dashboard/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('viseo_custom_dashboard.listing', {
#             'root': '/viseo_custom_dashboard/viseo_custom_dashboard',
#             'objects': http.request.env['viseo_custom_dashboard.viseo_custom_dashboard'].search([]),
#         })

#     @http.route('/viseo_custom_dashboard/viseo_custom_dashboard/objects/<model("viseo_custom_dashboard.viseo_custom_dashboard"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('viseo_custom_dashboard.object', {
#             'object': obj
#         })
