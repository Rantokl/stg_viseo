# -*- coding: utf-8 -*-
# from odoo import http


# class ViseoImportTva(http.Controller):
#     @http.route('/viseo_import__tva/viseo_import__tva/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/viseo_import__tva/viseo_import__tva/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('viseo_import__tva.listing', {
#             'root': '/viseo_import__tva/viseo_import__tva',
#             'objects': http.request.env['viseo_import__tva.viseo_import__tva'].search([]),
#         })

#     @http.route('/viseo_import__tva/viseo_import__tva/objects/<model("viseo_import__tva.viseo_import__tva"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('viseo_import__tva.object', {
#             'object': obj
#         })
