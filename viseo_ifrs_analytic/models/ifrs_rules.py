from odoo import fields, models, api


class IfrsRules (models.Model):
    _name = 'ifrs.rules'
    _description = 'Régle ifrs'

    name = fields.Char()
    state = fields.Selection(
        string='Etat',
        selection=[('disable', 'Désactivé'),
                   ('in_progress', 'En cours'), ],
        default='disable', )
        
    company_id = fields.Many2one('res.company', string='Société')
    origin_ids = fields.One2many('ifrs.origin.rules', 'rule_id')
    dest_ids = fields.One2many('ifrs.dest.rules', 'rule_id')

    def action_disable(self):
        self.write({'state': 'disable'})

    def action_activate(self):
        self.write({'state': 'in_progress'})

    def cron_dispatch(self):
        pass


class IfrsRulesOrigin(models.Model):
    _name = 'ifrs.origin.rules'
    _description = 'Ligne de règle origine'

    
    rule_id = fields.Many2one('ifrs.rules')
    account_id = fields.Many2one('account.account', string='Compte comptable',
                                 domain=[('deprecated', '=', False)])
    section_id = fields.Many2one('ifrs.section', string="Rubrique")
    product_id = fields.Many2one('product.product', string='Article')
    product_categ_id = fields.Many2one('product.category', string="Catégorie d'article")
    account_department_id = fields.Many2one('account.department', string="Departement")
    brand_id = fields.Many2one('viseo.brand', string="Marque")
    partner_id = fields.Many2one('res.partner', string="Partenaire")
    company_id = fields.Many2one('res.company', string='Société', related='rule_id.company_id')
    # is_active = fields.Boolean("Active")

    @api.onchange('product_id', 'rule_id')
    def _get_domain_for_product(self):
        domain = []
        templates = self.env['product.template'].search([('company_id', '=', self.rule_id.company_id.id)]).ids
        # product_ids = templates.mapped('product_id').ids
        if len(templates) > 0:
            domain += [('product_tmpl_id', 'in', templates)]
        else :
            domain += [('id', 'in', False)]
        return {'domain': {'product_id': domain}}


class IfrsRulesDestination(models.Model):
    _name = 'ifrs.dest.rules'
    _description = 'Ligne de règle destination'


    rule_id = fields.Many2one('ifrs.rules')
    account_id = fields.Many2one('account.account', string='Compte comptable',
                                 domain=[('deprecated', '=', False)])
    section_id = fields.Many2one('ifrs.section', string="Rubrique", required=True)
    name = fields.Char(string="Libellé", required=True)
    product_id = fields.Many2one('product.product', string='Article')
    percent = fields.Float(string="Pourcentage %")
    # method_of_split = fields.Selection(
    #     string='spliter par ',
    #     selection=[('fixed', 'Montant fixe'),
    #                ('percentage', 'Pourcentage'), ],
    #     required=True, )
    # product_categ_id = fields.Many2one('product.category', string="Catégorie d'article")
    account_department_id = fields.Many2one('account.department', string="Departement")
    brand_id = fields.Many2one('viseo.brand', string="Marque")
    partner_id = fields.Many2one('res.partner', string="Partenaire")
    company_id = fields.Many2one('res.company', string='Société', related='rule_id.company_id')
    amount = fields.Float(string="Montant")
    


