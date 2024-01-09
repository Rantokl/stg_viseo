# -*- coding: utf-8 -*-
# from odoo import http


# class ViseoRfid(http.Controller):
#     @http.route('/viseo_rfid/viseo_rfid/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/viseo_rfid/viseo_rfid/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('viseo_rfid.listing', {
#             'root': '/viseo_rfid/viseo_rfid',
#             'objects': http.request.env['viseo_rfid.viseo_rfid'].search([]),
#         })

#     @http.route('/viseo_rfid/viseo_rfid/objects/<model("viseo_rfid.viseo_rfid"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('viseo_rfid.object', {
#             'object': obj
#         })
