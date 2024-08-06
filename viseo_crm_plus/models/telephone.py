from odoo import models, fields, api


class telephoneType(models.TransientModel):
    _name = 'prospect.telephone.model'
    _description = 'Sélection de Type telephone'

    telephone_type = fields.Selection([('particulier','particulier'),('enterprise','Professionel')],string="Type de numéro")
    description = fields.Text(string="Petite remarque")
    prospect_id = fields.Many2one('prospect.crm')
    crm_id = fields.Many2one('viseo.crm')
