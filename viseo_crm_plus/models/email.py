from odoo import models, fields, api


class emailType(models.TransientModel):
    _name = 'prospect.email.model'
    _description = 'Sélection de Type email'

    email_type = fields.Selection([('particulier','particulier'),('enterprise','Professionel')],string="Type d'adresse email")
    description = fields.Text(string="Petite remarque")
    prospect_id = fields.Many2one('prospect.crm')
    crm_id = fields.Many2one('viseo.crm')
