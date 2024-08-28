from odoo import models, fields

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    attestation_destination = fields.Boolean(string='Attestation de destination')