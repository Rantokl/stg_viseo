# -*- coding: utf-8 -*-

# from odoo import models, fields, api


# class facturation__izyrent(models.Model):
#     _name = 'facturation__izyrent.facturation__izyrent'
#     _description = 'facturation__izyrent.facturation__izyrent'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100



from datetime import timedelta
from dateutil.relativedelta import relativedelta
from odoo import models, fields, api

class FacturationIzyrent(models.Model):
    _inherit = "viseo.rent"

    invoice_count = fields.Integer(compute="_compute_invoice_count", string='# Factures')
    
    def _compute_invoice_count(self):
        for record in self:
            record.invoice_count = self.env['viseo.rent.deadline'].search_count([('rent_id', '=', record.id), ('invoice_id', '!=', False)])

    def action_view_invoices(self):
        self.ensure_one()
        action = self.env.ref('account.action_move_out_invoice_type').read()[0]
        action['domain'] = [('id', 'in', self.rent_deadline.filtered(lambda r: r.invoice_id).mapped('invoice_id').ids)]
        return action

    date = fields.Date(string='Date du début de facturation')
    date_to = fields.Date(string='Date de fin', compute="remplir_date_de_fin", store=True, readonly=False)
    frequence = fields.Selection([
        ('once', 'Une fois'),
        ('weekly', 'Hebdomadaire'),
        ('monthly', 'Mensuelle'),
        ('quarterly', 'Trimestrielle'),
        ('yearly', 'Annuelle')
    ], string='Fréquence de facturation')

    rent_deadline = fields.One2many('viseo.rent.deadline', 'rent_id', string='Deadline Lines')

    @api.depends('date')
    def remplir_date_de_fin(self):
        for record in self:
            if record.date:
                if record.order_line and record.order_line[0].rental_condition and record.order_line[0].rental_duration:
                    rental_condit = record.order_line[0].rental_condition
                    durat = record.order_line[0].rental_duration
                    if rental_condit == 'day':
                        record.date_to = record.date + relativedelta(days=durat)
                    elif rental_condit == 'month':
                        record.date_to = record.date + relativedelta(months=durat)
                    elif rental_condit == 'week':
                        record.date_to = record.date + relativedelta(weeks=durat)
                    elif rental_condit == 'year':
                        record.date_to = record.date + relativedelta(years=durat)
                else:
                    record.date_to = False
            else:
                record.date_to = False

    def nettoyer_echeances_existantes(self):
        self.rent_deadline.unlink()

    def creer_echeances(self):
        self.nettoyer_echeances_existantes()

        if self.date and self.date_to and self.frequence:
            if self.frequence == 'once':
                self.env['viseo.rent.deadline'].create({
                    'date': self.date_to,  # Utiliser date_to pour une échéance unique
                    'amount': self.amount_untaxed,
                    'rent_id': self.id
                })
            elif self.frequence == 'weekly':
                nb_weeks = (self.date_to - self.date).days // 7
                for i in range(nb_weeks):
                    self.env['viseo.rent.deadline'].create({
                        'date': self.date + timedelta(weeks=i),
                        'amount': self.amount_untaxed / nb_weeks,
                        'rent_id': self.id
                    })
            elif self.frequence == 'monthly':
                start_date = self.date
                while start_date < self.date_to:
                    self.env['viseo.rent.deadline'].create({
                        'date': start_date,
                        'amount': self.amount_untaxed / ((self.date_to - self.date).days // 30),
                        'rent_id': self.id
                    })
                    start_date = start_date + relativedelta(months=1)

            elif self.frequence == 'quarterly':
                start_date = self.date
                while start_date < self.date_to:
                    self.env['viseo.rent.deadline'].create({
                        'date': start_date,
                        'amount': self.amount_untaxed / ((self.date_to - self.date).days // 90),
                        'rent_id': self.id
                    })
                    start_date = start_date + relativedelta(months=3)
            elif self.frequence == 'yearly':
                start_date = self.date
                while start_date < self.date_to:
                    self.env['viseo.rent.deadline'].create({
                        'date': start_date,
                        'amount': self.amount_untaxed / ((self.date_to - self.date).days // 365),
                        'rent_id': self.id
                    })
                    start_date = start_date + relativedelta(years=1)

    @api.onchange('date_to')
    def update_last_deadline_date(self):
        if self.date_to and self.rent_deadline:
            last_deadline = self.rent_deadline[-1]
            last_deadline.date = self.date_to

class FacturationRenting(models.Model):
    _name = "viseo.rent.deadline"

    date = fields.Date(string='Date')
    amount = fields.Float(string='Montant')
    rent_id = fields.Many2one('viseo.rent', string="Rent", required=True, ondelete='cascade')
    invoice_id = fields.Many2one('account.move', string="Facture")

    @api.model
    def schedule_auto_renting(self):
        today = fields.Date.today()
        deadlines = self.search([('date', '=', today)])
        for deadline in deadlines:
            deadline.create_invoice()

    def create_invoice(self):
        invoice_vals = {
            'type': 'out_invoice',
            'invoice_date': self.date,
            'partner_id': self.rent_id.partner_id.id,
            'invoice_line_ids': [(0, 0, {
                'product_id': self.rent_id.order_line[0].product_id.id,
                'price_unit': self.amount,
                'quantity': 1,
                'tax_ids': [(6, 0, self.rent_id.order_line[0].tax_id.ids)],
            })],
        }
        invoice = self.env['account.move'].create(invoice_vals)
        self.invoice_id = invoice.id
        return invoice

    def action_view_invoices(self):
        self.ensure_one()
        action = self.env.ref('account.action_move_out_invoice_type').read()[0]
        action['domain'] = [('id', 'in', self.filtered(lambda r: r.invoice_id).mapped('invoice_id').ids)]
        return action



    def schedule_auto_renting(self):
        today = fields.Date.today()
        deadlines = self.search([('date', '=', today)])
        for deadline in deadlines:
            deadline.create_invoice()
