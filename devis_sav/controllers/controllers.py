# -*- coding: utf-8 -*-
# from odoo import http


# class DevisSav(http.Controller):
#     @http.route('/devis_sav/devis_sav/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/devis_sav/devis_sav/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('devis_sav.listing', {
#             'root': '/devis_sav/devis_sav',
#             'objects': http.request.env['devis_sav.devis_sav'].search([]),
#         })

#     @http.route('/devis_sav/devis_sav/objects/<model("devis_sav.devis_sav"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('devis_sav.object', {
#             'object': obj
#         })
