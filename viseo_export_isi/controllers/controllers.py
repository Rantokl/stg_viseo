# -*- coding: utf-8 -*-
# from odoo import http


# class ViseoExportIsi(http.Controller):
#     @http.route('/viseo_export_isi/viseo_export_isi/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/viseo_export_isi/viseo_export_isi/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('viseo_export_isi.listing', {
#             'root': '/viseo_export_isi/viseo_export_isi',
#             'objects': http.request.env['viseo_export_isi.viseo_export_isi'].search([]),
#         })

#     @http.route('/viseo_export_isi/viseo_export_isi/objects/<model("viseo_export_isi.viseo_export_isi"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('viseo_export_isi.object', {
#             'object': obj
#         })
