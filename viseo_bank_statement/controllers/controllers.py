# -*- coding: utf-8 -*-
# from odoo import http


# class ViseoBankStatement(http.Controller):
#     @http.route('/viseo_bank_statement/viseo_bank_statement/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/viseo_bank_statement/viseo_bank_statement/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('viseo_bank_statement.listing', {
#             'root': '/viseo_bank_statement/viseo_bank_statement',
#             'objects': http.request.env['viseo_bank_statement.viseo_bank_statement'].search([]),
#         })

#     @http.route('/viseo_bank_statement/viseo_bank_statement/objects/<model("viseo_bank_statement.viseo_bank_statement"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('viseo_bank_statement.object', {
#             'object': obj
#         })
