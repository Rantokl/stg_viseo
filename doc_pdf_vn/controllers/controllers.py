# -*- coding: utf-8 -*-
# from odoo import http


# class DevisPdfVente(http.Controller):
#     @http.route('/doc_pdf_vn/doc_pdf_vn/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/doc_pdf_vn/doc_pdf_vn/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('doc_pdf_vn.listing', {
#             'root': '/doc_pdf_vn/doc_pdf_vn',
#             'objects': http.request.env['doc_pdf_vn.doc_pdf_vn'].search([]),
#         })

#     @http.route('/doc_pdf_vn/doc_pdf_vn/objects/<model("doc_pdf_vn.doc_pdf_vn"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('doc_pdf_vn.object', {
#             'object': obj
#         })
