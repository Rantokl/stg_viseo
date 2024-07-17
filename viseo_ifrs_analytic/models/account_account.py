from odoo import fields, models, api


class Account(models.Model):
    _inherit = 'account.account'


    ifrs_id = fields.Many2one('ifrs.section', string='IFRS')
    analytic_id = fields.Many2one('analytic.section', string='Viseo Analytique')