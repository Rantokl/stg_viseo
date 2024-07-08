# -*- coding: utf-8 -*-
# from odoo import http


# class FacturationIzyrent(http.Controller):
#     @http.route('/facturation__izyrent/facturation__izyrent/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/facturation__izyrent/facturation__izyrent/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('facturation__izyrent.listing', {
#             'root': '/facturation__izyrent/facturation__izyrent',
#             'objects': http.request.env['facturation__izyrent.facturation__izyrent'].search([]),
#         })

#     @http.route('/facturation__izyrent/facturation__izyrent/objects/<model("facturation__izyrent.facturation__izyrent"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('facturation__izyrent.object', {
#             'object': obj
#         })
