# -*- coding: utf-8 -*-
# from odoo import http


# class ViseoWhatsapp(http.Controller):
#     @http.route('/viseo_whatsapp/viseo_whatsapp/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/viseo_whatsapp/viseo_whatsapp/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('viseo_whatsapp.listing', {
#             'root': '/viseo_whatsapp/viseo_whatsapp',
#             'objects': http.request.env['viseo_whatsapp.viseo_whatsapp'].search([]),
#         })

#     @http.route('/viseo_whatsapp/viseo_whatsapp/objects/<model("viseo_whatsapp.viseo_whatsapp"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('viseo_whatsapp.object', {
#             'object': obj
#         })
