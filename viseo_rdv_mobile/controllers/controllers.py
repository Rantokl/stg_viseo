# -*- coding: utf-8 -*-
# from odoo import http


# class ViseoRdvMobile(http.Controller):
#     @http.route('/viseo_rdv_mobile/viseo_rdv_mobile/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/viseo_rdv_mobile/viseo_rdv_mobile/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('viseo_rdv_mobile.listing', {
#             'root': '/viseo_rdv_mobile/viseo_rdv_mobile',
#             'objects': http.request.env['viseo_rdv_mobile.viseo_rdv_mobile'].search([]),
#         })

#     @http.route('/viseo_rdv_mobile/viseo_rdv_mobile/objects/<model("viseo_rdv_mobile.viseo_rdv_mobile"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('viseo_rdv_mobile.object', {
#             'object': obj
#         })
