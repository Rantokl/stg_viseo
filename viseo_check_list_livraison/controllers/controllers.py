# -*- coding: utf-8 -*-
# from odoo import http


# class ViseoCheckListLivraison(http.Controller):
#     @http.route('/viseo_check_list_livraison/viseo_check_list_livraison/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/viseo_check_list_livraison/viseo_check_list_livraison/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('viseo_check_list_livraison.listing', {
#             'root': '/viseo_check_list_livraison/viseo_check_list_livraison',
#             'objects': http.request.env['viseo_check_list_livraison.viseo_check_list_livraison'].search([]),
#         })

#     @http.route('/viseo_check_list_livraison/viseo_check_list_livraison/objects/<model("viseo_check_list_livraison.viseo_check_list_livraison"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('viseo_check_list_livraison.object', {
#             'object': obj
#         })
