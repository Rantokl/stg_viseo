# -*- coding: utf-8 -*-
# from odoo import http


# class ViseoMaintenanceEquipement(http.Controller):
#     @http.route('/viseo_maintenance_equipement/viseo_maintenance_equipement/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/viseo_maintenance_equipement/viseo_maintenance_equipement/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('viseo_maintenance_equipement.listing', {
#             'root': '/viseo_maintenance_equipement/viseo_maintenance_equipement',
#             'objects': http.request.env['viseo_maintenance_equipement.viseo_maintenance_equipement'].search([]),
#         })

#     @http.route('/viseo_maintenance_equipement/viseo_maintenance_equipement/objects/<model("viseo_maintenance_equipement.viseo_maintenance_equipement"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('viseo_maintenance_equipement.object', {
#             'object': obj
#         })
