from odoo import fields, models, api


# class HistoricPartner(models.Model):
#     _name = 'historic.name.partner'
#     _description = 'Historique de nom'
#
#     name = fields.Char()
#     viseo_name = fields.Char(string="Nom client Viseo")
#     partner_id = fields.Many2one('res.partner')
#     bank_name = fields.Char(string="Nom banque")
#     bank_id = fields.Many2one('res.bank')
#

class Bank(models.Model):
    _inherit = 'res.bank'

    partner_id = fields.Many2one('res.partner', 'Partenaire lié')


