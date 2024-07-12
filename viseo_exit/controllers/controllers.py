# -*- coding: utf-8 -*-
# from odoo import http


# class ViseoExit(http.Controller):
#     @http.route('/viseo_exit/viseo_exit/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/viseo_exit/viseo_exit/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('viseo_exit.listing', {
#             'root': '/viseo_exit/viseo_exit',
#             'objects': http.request.env['viseo_exit.viseo_exit'].search([]),
#         })

#     @http.route('/viseo_exit/viseo_exit/objects/<model("viseo_exit.viseo_exit"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('viseo_exit.object', {
#             'object': obj
#         })
