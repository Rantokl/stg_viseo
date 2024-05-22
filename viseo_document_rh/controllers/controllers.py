# -*- coding: utf-8 -*-
# from odoo import http


# class ViseoDocumentPdfVn(http.Controller):
#     @http.route('/viseo_document_pdf__vn/viseo_document_pdf__vn/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/viseo_document_pdf__vn/viseo_document_pdf__vn/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('viseo_document_pdf__vn.listing', {
#             'root': '/viseo_document_pdf__vn/viseo_document_pdf__vn',
#             'objects': http.request.env['viseo_document_pdf__vn.viseo_document_pdf__vn'].search([]),
#         })

#     @http.route('/viseo_document_pdf__vn/viseo_document_pdf__vn/objects/<model("viseo_document_pdf__vn.viseo_document_pdf__vn"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('viseo_document_pdf__vn.object', {
#             'object': obj
#         })
