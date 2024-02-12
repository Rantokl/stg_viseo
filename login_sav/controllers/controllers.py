# -*- coding: utf-8 -*-
# from odoo import http


# class LoginSav(http.Controller):
#     @http.route('/login_sav/login_sav/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/login_sav/login_sav/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('login_sav.listing', {
#             'root': '/login_sav/login_sav',
#             'objects': http.request.env['login_sav.login_sav'].search([]),
#         })

#     @http.route('/login_sav/login_sav/objects/<model("login_sav.login_sav"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('login_sav.object', {
#             'object': obj
#         })
