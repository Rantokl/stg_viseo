# -*- coding: utf-8 -*-
# from odoo import http


# class ViseoContactgeo(http.Controller):
#     @http.route('/viseo_contactgeo/viseo_contactgeo/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/viseo_contactgeo/viseo_contactgeo/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('viseo_contactgeo.listing', {
#             'root': '/viseo_contactgeo/viseo_contactgeo',
#             'objects': http.request.env['viseo_contactgeo.viseo_contactgeo'].search([]),
#         })

#     @http.route('/viseo_contactgeo/viseo_contactgeo/objects/<model("viseo_contactgeo.viseo_contactgeo"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('viseo_contactgeo.object', {
#             'object': obj
#         })
