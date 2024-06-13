# -*- coding: utf-8 -*-
# from odoo import http


# class ReportViseoKpiSav(http.Controller):
#     @http.route('/report_viseo_kpi_sav/report_viseo_kpi_sav/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/report_viseo_kpi_sav/report_viseo_kpi_sav/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('report_viseo_kpi_sav.listing', {
#             'root': '/report_viseo_kpi_sav/report_viseo_kpi_sav',
#             'objects': http.request.env['report_viseo_kpi_sav.report_viseo_kpi_sav'].search([]),
#         })

#     @http.route('/report_viseo_kpi_sav/report_viseo_kpi_sav/objects/<model("report_viseo_kpi_sav.report_viseo_kpi_sav"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('report_viseo_kpi_sav.object', {
#             'object': obj
#         })
