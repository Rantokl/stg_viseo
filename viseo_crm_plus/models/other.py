from odoo import models, fields, api


class othersType(models.TransientModel):
    _name = 'prospect.other.model'
    _description = 'Sélection de Type autres'

    description = fields.Text(string="Petite description")
    prospect_id = fields.Many2one('prospect.crm')
    crm_id = fields.Many2one('viseo.crm')