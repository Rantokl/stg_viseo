# -*- coding: utf-8 -*-
# from odoo import http


# class ViseoPartnerInfo(http.Controller):
#     @http.route('/viseo_partner_info/viseo_partner_info/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/viseo_partner_info/viseo_partner_info/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('viseo_partner_info.listing', {
#             'root': '/viseo_partner_info/viseo_partner_info',
#             'objects': http.request.env['viseo_partner_info.viseo_partner_info'].search([]),
#         })

#     @http.route('/viseo_partner_info/viseo_partner_info/objects/<model("viseo_partner_info.viseo_partner_info"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('viseo_partner_info.object', {
#             'object': obj
#         })
