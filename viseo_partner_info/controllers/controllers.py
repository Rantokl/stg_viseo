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
from odoo import http
from odoo.http import request

class PDFPreviewController(http.Controller):
    @http.route('/web/pdf_preview', type='http', auth='user')
    def pdf_preview(self, id=None, **kwargs):
        record = request.env['res.partner'].browse(int(id))
        pdf_data = record.pdf_file
        return request.make_response(pdf_data, headers=[
            ('Content-Type', 'application/pdf'),
            ('Content-Disposition', 'inline; filename="preview.pdf"')
        ])
