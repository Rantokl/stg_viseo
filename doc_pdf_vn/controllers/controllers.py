# -*- coding: utf-8 -*-
# from odoo import http


# class DevisPdfVente(http.Controller):
#     @http.route('/devis_pdf_vente/devis_pdf_vente/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/devis_pdf_vente/devis_pdf_vente/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('devis_pdf_vente.listing', {
#             'root': '/devis_pdf_vente/devis_pdf_vente',
#             'objects': http.request.env['devis_pdf_vente.devis_pdf_vente'].search([]),
#         })

#     @http.route('/devis_pdf_vente/devis_pdf_vente/objects/<model("devis_pdf_vente.devis_pdf_vente"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('devis_pdf_vente.object', {
#             'object': obj
#         })
