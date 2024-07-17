# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import UserError

class AnalyticSection(models.Model):
    _name = 'analytic.section'
    _description = 'Rubrique analytique'

    name = fields.Char(string="Rubrique", required=True)
    parent_id = fields.Many2one('analytic.section')
    categ_id = fields.Many2one('analytic.section.type', string="Type/catégorie")
    company_id = fields.Many2one('res.company', string="Société", required=True, default=lambda self: self.env.company)
    account_ids = fields.Many2many('account.account', string='Compte comptable',
                                 domain=[('deprecated', '=', False)])


class AnalyticType(models.Model):
    _name = 'analytic.section.type'
    _description = 'Famille analytique'

    name = fields.Char("Nom")



class IfrsMoveLine(models.Model):
    _name = 'analytic.move.line'
    _description = 'Ecritures analytiques'


    @api.model
    def _default_user(self):
        return self.env.context.get('user_id', self.env.user.id)


    date = fields.Date(string='Date')
    name = fields.Char(string="Description")
    section_id = fields.Many2one('analytic.section', string="Rubrique")
    parent_id = fields.Many2one('analytic.move.line', string="Parent")
    product_id = fields.Many2one('product.product', string='Article')
    product_categ_id = fields.Many2one('product.category', string="Catégorie d'article")
    account_department_id = fields.Many2one('account.department', string="Département")
    company_id = fields.Many2one('res.company', string='Société')
    currency_id = fields.Many2one('res.currency', string='Devise')
    account_id = fields.Many2one('account.account', string='Compte comptable', check_company=True,
                                 domain=[('deprecated', '=', False)])
    user_id = fields.Many2one('res.users', string="Utilisateur", default=_default_user)
    quantity = fields.Float(string="Quantité")
    amount = fields.Float(string="Montant")
    amount_residual = fields.Float(string="Montant non splité")
    move_id = fields.Many2one('account.move.line', string="Ecriture d'origine")
    # brand_id = fields.Many2one('viseo.brand', related='product_id.product_tmpl_id.brand_id', string="Marque")
    brand_id = fields.Many2one('viseo.brand', compute='_compute_brand', inverse='_inverse_compute_brand', string="Marque")
    partner_id = fields.Many2one('res.partner', string="Partenaire")
    analytic_line_ids = fields.One2many('analytic.move.line', 'parent_id', string='Ecritures analytic')
    is_changed = fields.Boolean(string="a changer")
    is_from_rules = fields.Boolean(string="est résultant règle")
    percentage = fields.Float(string="Pourcentage")
    method_of_split = fields.Selection(
        string='spliter par ',
        selection=[('fixed', 'Montant fixe'),
                   ('percentage', 'Pourcentage'), ],
        required=True, )
    is_cogs = fields.Boolean(string="Est COGS")

    @api.onchange('percentage')
    def onchange_percent(self):
        try:
            self.amount = self.parent_id.amount * self.percentage / 100
        except:
            self.amount = 0

    @api.model
    def create(self, vals):
        if 'parent_id' in list(vals.keys()):
            parent_id = vals['parent_id']
            parent = self.env['analytic.move.line'].browse([parent_id])
            parent_amount_total = parent.amount
            if abs(parent.amount_residual) < abs(vals['amount']):
                raise UserError("Le montant de sous écriture ne peut pas être supérieur au montant residuel du parent")
            if parent_amount_total < 0:
                parent.amount_residual += abs(vals['amount'])
                vals['amount'] = abs(vals['amount']) * (-1)
            else:
                parent.amount_residual -= abs(vals['amount'])
        # Create amount_residual
        vals['amount_residual'] = vals['amount']
        ifrs = super(IfrsMoveLine, self).create(vals)
        return ifrs

    def write(self, values):
        values_modif = values.copy()
        # Delete One2many child to skip change from it
        if 'analytic_line_ids' in list(values_modif.keys()):
            values_modif.pop('analytic_line_ids')
            if len(values_modif) > 1:
                values['is_changed'] = True
        # Modification signe
        if self.parent_id:
            parent_amount_total = self.parent_id.amount
            if parent_amount_total < 0:
                if values['amount']:
                    values.update({'amount': abs(values['amount']) * (-1)})
        res = super(IfrsMoveLine, self).write(values)
        return res

    def unlink(self):
        if self.parent_id:
            if self.parent_id.amount < 0:
                self.parent_id.amount_residual -= abs(self.amount)
            else:
                self.parent_id.amount_residual += abs(self.amount)
        return super(IfrsMoveLine, self).unlink()

    @api.depends('product_id')
    def _compute_brand(self):
        for line in self:
            if line.product_id:
                line.brand_id = line.product_id.product_tmpl_id.brand_id.id
            else:
                line.brand_id = False
            # 'product_id.product_tmpl_id.brand_id'
    def _inverse_compute_brand(self):
        for line in self:
            if line.brand_id:
                line.brand_id = line.product_id.product_tmpl_id.brand_id.id