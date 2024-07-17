# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError

class IfrsSection(models.Model):
    _name = 'ifrs.section'
    _description = 'Rubrique IFRS'


    name = fields.Char(string="Rubrique", required=True)
    code = fields.Char(string="Code", required=True)
    parent_id = fields.Many2one('ifrs.section')
    categ_id = fields.Many2one('ifrs.section.type', string="Type/catégorie")
    # department_id = fields.Many2one('account.department', string="Departement")
    company_id = fields.Many2one('res.company', string="Société", required=True, default=lambda self: self.env.company)
    # account_ids = fields.Many2many('account.account', string='Compte comptable')

    def name_get(self):
        result = []
        for ifrs in self:
            name = ifrs.code + ' ' + ifrs.name
            result.append((ifrs.id, name))
        return result

    @api.returns('self', lambda value: value.id)
    def copy(self, default=None):
        default = dict(default or {})
        if default.get('code', False):
            return super(IfrsSection, self).copy(default)
        try:
            default['code'] = (str(int(self.code) + 10) or '').zfill(len(self.code))
            default.setdefault('name', _("%s (copy)") % (self.name or ''))
            while self.env['account.account'].search([('code', '=', default['code']),
                                                      ('company_id', '=', default.get('company_id', False) or self.company_id.id)], limit=1):
                default['code'] = (str(int(default['code']) + 10) or '')
                default['name'] = _("%s (copy)") % (self.name or '')
        except ValueError:
            default['code'] = _("%s (copy)") % (self.code or '')
            default['name'] = self.name
        return super(IfrsSection, self).copy(default)


class IfrsMoveLine(models.Model):
    _name = 'ifrs.section.type'
    _description = 'Catégorie/Type rubrique'

    name = fields.Char("Nom")

class IfrsMoveLine(models.Model):
    _name = 'ifrs.move.line'
    _description = 'Ecritures ifrs'
    _inherit = ['mail.thread', 'mail.activity.mixin']


    @api.model
    def _default_user(self):
        return self.env.context.get('user_id', self.env.user.id)

    date = fields.Date(string='Date', required=True, tracking=True)
    name = fields.Char(string="Libellé", tracking=True)
    section_id = fields.Many2one('ifrs.section', string="Rubrique", required=True, tracking=True)
    parent_id = fields.Many2one('ifrs.move.line', string="ifrs origine")
    product_id = fields.Many2one('product.product', string='Article')
    product_categ_id = fields.Many2one('product.category', string="Catégorie d'article")
    account_department_id = fields.Many2one('account.department', string="Département", tracking=True)
    company_id = fields.Many2one('res.company', string='Société', required=True, default=lambda self: self.env.company)
    currency_id = fields.Many2one('res.currency', string='Devise')
    account_id = fields.Many2one('account.account', string='Compte comptable', check_company=True,
                                 domain=[('deprecated', '=', False)])
    user_id = fields.Many2one('res.users', string="Utilisateur", default=_default_user, tracking=True)
    amount = fields.Float(string="Montant", tracking=True)
    amount_residual = fields.Float(string="Montant non splité", comptute='')
    move_id = fields.Many2one('account.move.line', string="Ecriture d'origine", copy=False)
    brand_id = fields.Many2one('viseo.brand', string="Marque", copy=False)
    partner_id = fields.Many2one('res.partner', string="Partenaire")
    ifrs_line_ids = fields.One2many('ifrs.move.line', 'parent_id', string='Ecritures ifrs')
    is_changed = fields.Boolean(string="Changé")
    is_from_rules = fields.Boolean(string="Est résultant règle")
    is_splited = fields.Boolean(string="Est splité", compute='_compute_split')
    percentage = fields.Float(string="Pourcentage")
    method_of_split = fields.Selection(
        string='spliter par ',
        selection=[('fixed', 'Montant fixe'),
                   ('percentage', 'Pourcentage'), ],
        required=True, )
    is_cogs = fields.Boolean(string="Est COGS")


    @api.onchange('ifrs_line_ids')
    def _compute_split(self):
        if self.ifrs_line_ids:
            child_amount = sum(self.ifrs_line_ids.mapped('amount'))
            if abs(self.amount) > abs(self.amount_residual) and abs(self.amount) > abs(child_amount):
                self.is_splited = True
            else:
                self.is_splited = False

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
            parent = self.env['ifrs.move.line'].browse([parent_id])
            parent_amount_total = parent.amount
            if abs(parent.amount_residual) < abs(vals['amount']):
                raise UserError("Le montant de sous écriture ne peut pas être supérieur au montant residuel du parent")
            if parent_amount_total < 0:
                parent.amount_residual += abs(vals['amount'])
                vals['amount'] = abs(vals['amount']) * (-1)
            else:
                parent.amount_residual -= abs(vals['amount'])
        #Create amount_residual
        vals['amount_residual'] = vals['amount']
        ifrs = super(IfrsMoveLine, self).create(vals)
        return ifrs

    def write(self, values):
        values_modif = values.copy()
        #Delete One2many child to skip change from it
        if 'ifrs_line_ids' in list(values_modif.keys()):
            values_modif.pop('ifrs_line_ids')
            if len(values_modif) > 1:
                values['is_changed'] = True
        #Modification signe
        if self.parent_id:
            parent_amount_total = self.parent_id.amount
            if parent_amount_total < 0:
                if values['amount']:
                    values.update({'amount': abs(values['amount']) * (-1)})
        res = super(IfrsMoveLine, self).write(values)
        return res


    def unlink(self):
        if self.parent_id:
            if self.parent_id.amount < 0 :
                self.parent_id.amount_residual -= abs(self.amount)
            else:
                self.parent_id.amount_residual += abs(self.amount)
        return super(IfrsMoveLine, self).unlink()









