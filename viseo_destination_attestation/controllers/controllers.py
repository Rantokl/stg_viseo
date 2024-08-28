# -*- coding: utf-8 -*-
# from odoo import http


# class ViseoDestinationAttestation(http.Controller):
#     @http.route('/viseo_destination_attestation/viseo_destination_attestation/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/viseo_destination_attestation/viseo_destination_attestation/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('viseo_destination_attestation.listing', {
#             'root': '/viseo_destination_attestation/viseo_destination_attestation',
#             'objects': http.request.env['viseo_destination_attestation.viseo_destination_attestation'].search([]),
#         })

#     @http.route('/viseo_destination_attestation/viseo_destination_attestation/objects/<model("viseo_destination_attestation.viseo_destination_attestation"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('viseo_destination_attestation.object', {
#             'object': obj
#         })
