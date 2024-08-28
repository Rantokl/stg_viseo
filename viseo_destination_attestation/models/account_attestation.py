from odoo import models, fields

class AccountMove(models.Model):
    _inherit = 'account.move'

    attestation_destination = fields.Boolean(string='Attestation de destination')

    def action_post(self):
        res = super(AccountMove, self).action_post()
        for invoice in self:
            if invoice.invoice_origin:
                sale_order = self.env['sale.order'].search([('name', '=', invoice.invoice_origin)])
                if sale_order:
                    invoice.attestation_destination = sale_order.attestation_destination
        return res