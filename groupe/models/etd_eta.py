from odoo import models, fields, api

class ImportFollow(models.Model):
    _inherit = 'import.followup.line'

    etd_field = fields.Date(string='ETD', readonly=True, compute='_compute_etd_field')
    eta_field = fields.Date(string='ETA', readonly=True, compute='_compute_eta_field')
    #changement du champ 'Numero conteneur' en 'TC'
    #numero_conteneur = fields.Char(string='TC')

    @api.depends('etd')
    def _compute_etd_field(self):
        for record in self:
            record.etd_field = record.etd

    @api.depends('eta')
    def _compute_eta_field(self):
        for record in self:
            record.eta_field = record.eta

    
