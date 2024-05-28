# -*- coding: utf-8 -*-
# from odoo import http


# class ViseoCreditApplication(http.Controller):
#     @http.route('/viseo_credit_application/viseo_credit_application/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/viseo_credit_application/viseo_credit_application/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('viseo_credit_application.listing', {
#             'root': '/viseo_credit_application/viseo_credit_application',
#             'objects': http.request.env['viseo_credit_application.viseo_credit_application'].search([]),
#         })

#     @http.route('/viseo_credit_application/viseo_credit_application/objects/<model("viseo_credit_application.viseo_credit_application"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('viseo_credit_application.object', {
#             'object': obj
#         })
