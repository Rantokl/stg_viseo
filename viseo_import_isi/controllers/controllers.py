# -*- coding: utf-8 -*-
# from odoo import http


# class ViseoImportIsi(http.Controller):
#     @http.route('/viseo_import_isi/viseo_import_isi/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/viseo_import_isi/viseo_import_isi/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('viseo_import_isi.listing', {
#             'root': '/viseo_import_isi/viseo_import_isi',
#             'objects': http.request.env['viseo_import_isi.viseo_import_isi'].search([]),
#         })

#     @http.route('/viseo_import_isi/viseo_import_isi/objects/<model("viseo_import_isi.viseo_import_isi"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('viseo_import_isi.object', {
#             'object': obj
#         })
