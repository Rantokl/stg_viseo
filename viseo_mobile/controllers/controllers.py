# -*- coding: utf-8 -*-
# from odoo import http


# class ViseoMobile(http.Controller):
#     @http.route('/viseo_mobile/viseo_mobile/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/viseo_mobile/viseo_mobile/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('viseo_mobile.listing', {
#             'root': '/viseo_mobile/viseo_mobile',
#             'objects': http.request.env['viseo_mobile.viseo_mobile'].search([]),
#         })

#     @http.route('/viseo_mobile/viseo_mobile/objects/<model("viseo_mobile.viseo_mobile"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('viseo_mobile.object', {
#             'object': obj
#         })
