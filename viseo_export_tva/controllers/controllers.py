# -*- coding: utf-8 -*-
# from odoo import http


# class ViseoExportTva(http.Controller):
#     @http.route('/viseo_export_tva/viseo_export_tva/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/viseo_export_tva/viseo_export_tva/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('viseo_export_tva.listing', {
#             'root': '/viseo_export_tva/viseo_export_tva',
#             'objects': http.request.env['viseo_export_tva.viseo_export_tva'].search([]),
#         })

#     @http.route('/viseo_export_tva/viseo_export_tva/objects/<model("viseo_export_tva.viseo_export_tva"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('viseo_export_tva.object', {
#             'object': obj
#         })
