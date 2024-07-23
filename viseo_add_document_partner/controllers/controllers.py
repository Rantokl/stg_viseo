# -*- coding: utf-8 -*-
# from odoo import http


# class ViseoAddDocumentPartner(http.Controller):
#     @http.route('/viseo_add_document_partner/viseo_add_document_partner/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/viseo_add_document_partner/viseo_add_document_partner/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('viseo_add_document_partner.listing', {
#             'root': '/viseo_add_document_partner/viseo_add_document_partner',
#             'objects': http.request.env['viseo_add_document_partner.viseo_add_document_partner'].search([]),
#         })

#     @http.route('/viseo_add_document_partner/viseo_add_document_partner/objects/<model("viseo_add_document_partner.viseo_add_document_partner"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('viseo_add_document_partner.object', {
#             'object': obj
#         })
