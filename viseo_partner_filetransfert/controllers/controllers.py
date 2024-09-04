# -*- coding: utf-8 -*-
# from odoo import http


# class ViseoPartnerFiletransfert(http.Controller):
#     @http.route('/viseo_partner_filetransfert/viseo_partner_filetransfert/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/viseo_partner_filetransfert/viseo_partner_filetransfert/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('viseo_partner_filetransfert.listing', {
#             'root': '/viseo_partner_filetransfert/viseo_partner_filetransfert',
#             'objects': http.request.env['viseo_partner_filetransfert.viseo_partner_filetransfert'].search([]),
#         })

#     @http.route('/viseo_partner_filetransfert/viseo_partner_filetransfert/objects/<model("viseo_partner_filetransfert.viseo_partner_filetransfert"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('viseo_partner_filetransfert.object', {
#             'object': obj
#         })
