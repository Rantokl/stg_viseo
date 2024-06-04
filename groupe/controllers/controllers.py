# -*- coding: utf-8 -*-
# from odoo import http


# class Groupe(http.Controller):
#     @http.route('/groupe/groupe/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/groupe/groupe/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('groupe.listing', {
#             'root': '/groupe/groupe',
#             'objects': http.request.env['groupe.groupe'].search([]),
#         })

#     @http.route('/groupe/groupe/objects/<model("groupe.groupe"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('groupe.object', {
#             'object': obj
#         })
