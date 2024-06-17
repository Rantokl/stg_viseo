from odoo import models

class ReportVehicleComparison(models.AbstractModel):
    _name = 'report.parc_auto.report_vehicle_comparison'
    _description = 'Vehicle Comparison Report'

    def get_report_values(self, docids, data=None):
        docs = self.env['fleet.vehicle.model'].browse(docids)
        return {
            'doc_ids': docids,
            'doc_model': 'fleet.vehicle.model',
            'docs': docs,
            'data': data,
        }

