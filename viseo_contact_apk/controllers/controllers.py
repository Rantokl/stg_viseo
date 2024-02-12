# -*- coding: utf-8 -*-
# from odoo import http


# class ViseoContactApk(http.Controller):
#     @http.route('/viseo_contact_apk/viseo_contact_apk/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/viseo_contact_apk/viseo_contact_apk/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('viseo_contact_apk.listing', {
#             'root': '/viseo_contact_apk/viseo_contact_apk',
#             'objects': http.request.env['viseo_contact_apk.viseo_contact_apk'].search([]),
#         })

#     @http.route('/viseo_contact_apk/viseo_contact_apk/objects/<model("viseo_contact_apk.viseo_contact_apk"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('viseo_contact_apk.object', {
#             'object': obj
#         })
