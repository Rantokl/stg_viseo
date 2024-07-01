# -*- coding: utf-8 -*-
# from odoo import http


# class ViseoQualifications(http.Controller):
#     @http.route('/viseo_qualifications/viseo_qualifications/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/viseo_qualifications/viseo_qualifications/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('viseo_qualifications.listing', {
#             'root': '/viseo_qualifications/viseo_qualifications',
#             'objects': http.request.env['viseo_qualifications.viseo_qualifications'].search([]),
#         })

#     @http.route('/viseo_qualifications/viseo_qualifications/objects/<model("viseo_qualifications.viseo_qualifications"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('viseo_qualifications.object', {
#             'object': obj
#         })
