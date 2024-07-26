# -*- coding: utf-8 -*-
# from odoo import http


# class ViseoDevisConfirm(http.Controller):
#     @http.route('/viseo_devis_confirm/viseo_devis_confirm/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/viseo_devis_confirm/viseo_devis_confirm/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('viseo_devis_confirm.listing', {
#             'root': '/viseo_devis_confirm/viseo_devis_confirm',
#             'objects': http.request.env['viseo_devis_confirm.viseo_devis_confirm'].search([]),
#         })

#     @http.route('/viseo_devis_confirm/viseo_devis_confirm/objects/<model("viseo_devis_confirm.viseo_devis_confirm"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('viseo_devis_confirm.object', {
#             'object': obj
#         })
