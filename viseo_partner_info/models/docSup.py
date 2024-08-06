from odoo import models, fields, api


class viseo_document_cin_represent(models.Model):
    _name = 'cin.represent'

    partner_id = fields.Many2one('res.partner')
    cin_represent = fields.Binary(string='CIN représentant', attachment=True)

class viseo_document_rib_represent(models.Model):
    _name = 'rib.represent'

    partner_id = fields.Many2one('res.partner')
    rib_represent = fields.Binary(string='RIB représentant', attachment=True)

class viseo_document_cr_represent(models.Model):
    _name = 'cr.represent'

    partner_id = fields.Many2one('res.partner')
    cr_represent = fields.Binary(string='Résidence représentant', attachment=True)