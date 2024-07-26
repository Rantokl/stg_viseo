
from odoo import models, fields, api


class viseo_document_partner(models.Model):
    _name = 'viseo_document_partner.partner_document'

    partner_id = fields.Many2one('res.partner')
    cr_represent = fields.Binary(string='Résidence représentant', attachment=True)
    cin_represent = fields.Binary(string='CIN représentant', attachment=True)

