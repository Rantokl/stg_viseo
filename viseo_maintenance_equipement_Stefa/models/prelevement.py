# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime
from odoo.exceptions import UserError

class PrelevementPiecesTools(models.Model):
    _name = 'prelevement.pieces.bike'
    _inherit = ['mail.thread']
    _description = 'Prelevement pieces'
    _order = "create_date desc"

    name = fields.Char(readonly=True)
    company_id = fields.Many2one('res.company', default=lambda self: self.env.company.id, required=True, readonly=True,
                                 string='Société')
    date = fields.Date(string='Date prélèvement', default=datetime.today(), required=True)
    forcast_return_date = fields.Date(string='Date fin opération', help="Date à laquelle on prevoit de remettre la voiture de prélèvement en état d'être livrable", copy=False)
    demandeur = fields.Many2one(
        string=u'Demandeur',
        comodel_name='res.users', default=lambda self: self.env.user.id,
        required=True, readonly=True, copy=False)
    tools_source = fields.Many2one('equipement.bike.tools', track_visibility="onchange", copy=False, string="Voiture à prélever pièces")
    tools_src = fields.Many2one(
        comodel_name='product.product',
        string='Voiture à prélèver pièces', track_visibility='onchange', copy=False, store="True")
    sn_src = fields.Char( string='Numéro de serie', track_visibility='onchange', copy=False, store="True")

    # @api.depends('tools_source')
    # def _compute_info_src(self):
    #     serial = self.vehicle_source.lot_id
    #     if serial:
    #         self.vehicle_src = serial.product_id
    #         self.vin_src = serial
    #     else:
    #         self.vehicle_src = False
    #         self.vin_src = False

    tools_dest = fields.Many2one(
        comodel_name='equipement.bike.tools',
        string='Voiture de destination pièces', required=True, track_visibility='onchange')
    sn_dest = fields.Char(string='Numéro de serie destination')
    po_link = fields.Many2one(comodel_name='purchase.order', string='PO lié(s)', copy=False, track_visibility='onchange')
    is_taken_from_livrable = fields.Boolean(string='A enlever du livrable')
    state = fields.Selection(
        selection=[('task', 'Demande'),
                   ('request', 'Demande de validation'),
                   ('confirmed', 'Confirmé par chef SAV'),
                   ('vin', 'Choix VIN'),
                   ('validate', 'A Valider'),
                   ('withdraw', 'Ordre de prelevement'),
                   ('done', 'Prélevé'),
                   ('cancel', 'Annulé')
                   ],
        required=False, string="Etat prélèvement", default='task', tracking=3)

    state_return = fields.Selection(
        selection=[('automotive_validate', 'Retour pièces automotive'),
                   ('sav_validate', 'Retour SAV'),
                   ('vn_validate', 'Retour VN'),
                   ('returned', 'Pièce(s) retourné(s)'),
                   ],
        required=False, string="Etat retour pièce(s)", copy=False)

    piece_ids = fields.Many2many('tools.pieces', required=True, copy=False)
    reference_ids = fields.One2many('tools.pieces.reference', 'prelevement_id', copy=False)

    prelevement_id = fields.Many2one(comodel_name='product.product', store=True)
    # prelevement_id = fields.Many2one(comodel_name='product.template', store=True)
    repair_id = fields.Many2one(comodel_name='maintenance.bike.tools', copy=False, string="Maintenance")


    def check_date(self):
        if self.forcast_return_date:
            if self.date >= self.forcast_return_date:
                raise UserError("La date de retour {} ne peut pas être inférieure ou égale à la date du prélèvement {}".format(self.forcast_return_date, self.date))
        else:
            pass

    @api.onchange('forcast_return_date')
    def _onchange_return_date(self):
        self.check_date()

    @api.onchange('po_link')
    def _onchange_po(self):
        if self.po_link and self.repair_id:
            po_lines = self.po_link.order_line
            products_repair = self.repair_id.fleet_servicesline_ids.filtered(lambda l: l.qty_prel > 0)
            ref = self.env['tools.pieces.reference']
            self.write({'reference_ids' : [(5, 0, 0)]})
            for repair_line in products_repair:
                for line in po_lines:
                    if line.product_id.type == 'product':
                        vals = {'prelevement_id': self.id,
                                'purchase_line_id': line.id,
                                'product_id': line.product_id.id,
                                'qty_cmd': line.product_qty,
                                }
                        if repair_line.product_id.id == line.product_id.id:
                            vals['qty_affected']: repair_line.qty_prel
                        ref.create(vals)


    def action_cancel(self):
        self.end_of_withdrawn()
        self.write({'state': 'cancel', 'is_taken_from_livrable': False})

    def action_state_task(self):
        self.write({'state': 'task'})


    #Création ajustement de l'inventaire sur l'emplacement SAV
    def create_adjustement(self):
        reference_ids = self.reference_ids.filtered(lambda x:x.qty_affected > 0)
        if reference_ids and self.repair_id:
            if self.repair_id.workshop_type_id.name == 'VO':
                location_dest_id = self.env['stock.location'].search(
                    [('name', 'in', ['Atelier vo OT', 'Atelier vo CA']), ('company_id', '=', self.company_id.id)])
            else:
                location_dest_id = self.env['stock.location'].search(
                    [('name', 'in', ['SAVOT', 'SAVCA']), ('company_id', '=', self.company_id.id)])
            product_ids = reference_ids.mapped('product_id')
            vals_inventory = {
                'name': ('{} : {}'.format()),
                'product_ids': [(6,0,product_ids.ids)],
                'company_id': self.company_id.id,
                'location_ids': [(6,0,location_dest_id.ids)],
                'state': 'draft',
                'prefill_counted_quantity': 'counted'
            }
            inventaire = self.env['stock.inventory'].sudo().create(vals_inventory)
            inventaire.sudo().action_start()
            inventaire.sudo().action_open_inventory_lines()
            # Suppréssion des lignes d'inventaire par défaut
            inventaire.sudo().write({'line_ids': [(5, 0, {})]})

            # Création ligne d'inventaire dans ajustement de stock
            for line in self.reference_ids:
                theoric_qty = self.env['stock.quant'].search([('location_id', '=', location_dest_id.id), ('product_id', '=', line.product_id.id)])
                qty_onhand = sum(theoric_qty.mapped('quantity'))
                new_real_qty = qty_onhand + line.qty_affected
                new_inventory_line = {
                    'product_id': line.product_id.id,
                    'inventory_id': inventaire.id,
                    'product_qty': new_real_qty,
                    'location_id': location_dest_id.id
                }
                inventaire.update({'line_ids': [(0, 0, new_inventory_line)]})
            inventaire.action_validate()

    def action_done(self):
        self.create_adjustement()
        self.write({'state': 'done'})

    def transfert_prelevement_to_product(self):
        if self.vehicle_src and self.is_taken_from_livrable:
            # Récupér le product.product correspond à la voiture à prélèver pièces
            product = self.env['product.product'].search([('id', '=', self.vehicle_src.id)])
            quant = self.env['stock.quant'].search([('product_id', '=', self.vehicle_src.id), ('lot_id', '=', self.vin_src.id)])
            # Marqué comme prélévé
            product.write({'is_withdrawn': True})
            quant.sudo().write({'is_withdrawn': True})
            # Afficher dans liste prélève sur product.template
            p_template = product.product_tmpl_id
            p_template.write({'prelevement_ids': [(4, self.id)]})

    # Appeler cette méthode après remise en etat de vente de la voiture
    def end_of_withdrawn(self):
        if self.vehicle_src and self.is_taken_from_livrable:
            # Récupér le product.product correspond à la voiture à prélèver pièces
            product = self.env['product.product'].search([('id', '=', self.vehicle_src.id)])
            quant = self.env['stock.quant'].search([('product_id', '=', self.vehicle_src.id)])
            # Marqué comme n'est plus prélévé
            product.write({'is_withdrawn': False})
            quant.sudo().write({'is_withdrawn': False})
            # enlever dans la liste prélève sur product.template
            # p_template = product.product_tmpl_id
            # p_template.write({'prelevement_ids': [(3, self.id)]})

    def action_return_pieces(self):
        self.write({'state_return': 'automotive_validate', 'forcast_return_date': datetime.today()})


    @api.model
    def create(self, vals):
        vals['name'] = self.env['ir.sequence'].next_by_code('prelevement.pieces.bike') or '/'
        return super(PrelevementPiecesTools, self).create(vals)

    def _get_has_mygroup(self):
        if self.env.user.has_group('viseo_prelevement_pieces.group_fleet_vehicle_pieces_po'):
            self.has_mygroup = True
        else:
            self.has_mygroup = False

    has_mygroup = fields.Boolean(compute='_get_has_mygroup')

class Pieces(models.Model):
    _name = 'tools.pieces'
    _description = 'Pieces Equipements'
    _order = 'name desc'

    name = fields.Char(string='Pièces')
    # prelevement_id = fields.Many2one('prelevement.pieces')

class PiecesList(models.Model):
    _name = 'tools.pieces.reference'
    _description = "Référence des articles prélévés"


    product_id = fields.Many2one('product.product', 'Article', required=1)
    prelevement_id = fields.Many2one('prelevement.pieces.bike')
    purchase_line_id = fields.Many2one('purchase.order.line')
    qty_cmd = fields.Float(string="Qté PO")
    qty_affected = fields.Float(string="Qté prélevée")

    @api.constrains('qty_affected')
    def _check_qty_affected(self):
        for piece in self:
            total_qty_affected = sum(piece.filtered(lambda p: p.purchase_line_id == piece.purchase_line_id and
                                                          p.product_id == piece.product_id).mapped('qty_affected'))
            if piece.qty_affected > piece.qty_cmd or total_qty_affected > piece.qty_cmd:
                raise UserError("La quantité affectée ne doit pas dépasser la quantité commandée sur la PO")


class RuleRule(models.Model):
    _inherit = 'rule.rule'

    prelevement_validation_ids = fields.One2many(
        string=u'Niveau de validation prélèvement pièces',
        comodel_name='prelevement.validation.bike',
        inverse_name='rule_id',
    )


# PRELEVEMENT VALIDATION
class PrelevementToolsValidation(models.Model):
    _name = "prelevement.validation.bike"
    _order = "sequence"

    sequence = fields.Integer()
    rule_id = fields.Many2one(
        string=u'Nom',
        comodel_name='rule.rule',
    )
    name = fields.Many2one(
        string=u'Nom',
        comodel_name='res.users',
        required=True,
    )

    is_sav_chief = fields.Boolean(string="Chef SAV")
    is_automotive = fields.Boolean(string="Automotive")
    is_vn = fields.Boolean(string="VN")
    is_direction = fields.Boolean(string="Direction")


class PrelevementPiecesToolsMaintenance(models.Model):
    _inherit = 'prelevement.pieces.bike'

    is_sav_chief = fields.Boolean(default=False, compute='_compute_button_validation_visibility')
    is_automotive = fields.Boolean(default=False, compute='_compute_button_validation_visibility')
    is_vn = fields.Boolean(default=False, compute='_compute_button_validation_visibility')
    is_direction = fields.Boolean(default=False, compute='_compute_button_validation_visibility')
    is_first_confirm = fields.Boolean(default=False, compute='_compute_button_validation_visibility')

    sav_validator = fields.Many2one(
        string=u'SAV validateur',
        comodel_name='res.users',
        copy=False,
    )

    automotive_validator = fields.Many2one(
        string=u'Automotive validateur',
        comodel_name='res.users',
        copy=False,
    )

    vn_validator = fields.Many2one(
        string=u'vn validateur',
        comodel_name='res.users',
        copy=False,
    )

    direction_validator = fields.Many2one(
        string=u'Direction validateur',
        comodel_name='res.users',
        copy=False,
    )

    def set_user_false(self):
        self.is_sav_chief = False
        self.is_automotive = False
        self.is_vn = False
        self.is_direction = False

    @api.depends('demandeur')
    def _compute_button_validation_visibility(self):
        # DEMANDEUR
        if self.env.user in self.demandeur:
            self.is_first_confirm = True
        else:
            self.is_first_confirm = False
        try:
            validators = self._get_validators()
            current_validator = validators.filtered(lambda r: r.name == self.env.user)

            if not current_validator:
                self.set_user_false()
            else:
                # SAV CHIEF
                sav_validator = validators.filtered(lambda r: r.is_sav_chief == True)
                sav_users = sav_validator.mapped(lambda c: c.name)
                if self.env.user in sav_users:
                    self.is_sav_chief = True
                else:
                    self.is_sav_chief = False

                # AUTOMOTIVE
                automotive_validator = validators.filtered(lambda r: r.is_automotive == True)
                automotive_users = automotive_validator.mapped(lambda c: c.name)
                if self.env.user in automotive_users:
                    self.is_automotive = True
                else:
                    self.is_automotive = False

                # VN
                vn_validator = validators.filtered(lambda r: r.is_vn == True)
                vn_users = vn_validator.mapped(lambda c: c.name)
                if self.env.user in vn_users:
                    self.is_vn = True
                else:
                    self.is_vn = False

                # DIRECTION
                direction_validator = validators.filtered(lambda r: r.is_direction == True)
                direction_users = direction_validator.mapped(lambda c: c.name)
                if self.env.user in direction_users:
                    self.is_direction = True
                else:
                    self.is_direction = False
        except:
            self.set_user_false()

    prelevement_rule = fields.Many2one(
        'rule.rule',
        string="Règle",
        domain=lambda self: self._rule_domain()
    )

    def _rule_domain(self):
        model_id = self.env['ir.model'].search([('model', '=', 'prelevement.pieces')]).ids
        rule_ids = self.env['rule.rule'].search(
            [('model_id', 'in', model_id), ('company_id', '=', self.env.company.id)]).ids
        domain = [('id', 'in', rule_ids)]
        return domain

    def _get_validators(self):
        list_rule = self.env['rule.rule'].search([('id', '=', self.prelevement_rule.id)]) if self.prelevement_rule else \
        self.env['rule.rule'].search([('model_id', '=', 'prelevement.pieces'), ('company_id', '=', self.company_id.id)])
        rule = []

        if list_rule:
            for lr in list_rule:
                if self.demandeur.id in [user.id for user in lr.user_ids]:
                    rule.append(lr)
        if rule:
            for r in rule:
                if not r.parent_id:
                    validators = r.prelevement_validation_ids
                else:
                    validators = self.env['prelevement.validation']
                    current_rule = r
                    while current_rule:
                        validators += current_rule.prelevement_validation_ids
                        current_rule = current_rule.parent_id
                    # validators = r.prelevement_validation_ids
                    # validators += r.parent_id.prelevement_validation_ids
                    # if r.parent_id.parent_id:
                    #     validators += r.parent_id.parent_id.prelevement_validation_ids
            return validators

    def launch_validation(self, next_validator):
        """
        GET THE NEXT VALIDATOR FOR EACH STATE
        """
        list_validator = self._get_validators()

        if not list_validator:
            raise UserError(
                'Liste de validation invalide, veuillez demander a l\'administrateur de configurer les niveaux de validation de prélèvement.')

        users = self.env['res.users']

        if next_validator == 'sav_chief':
            validators = list_validator.filtered(lambda r: r.is_sav_chief == True)
        elif next_validator == 'automotive':
            validators = list_validator.filtered(lambda r: r.is_automotive == True)
        elif next_validator == 'vn':
            validators = list_validator.filtered(lambda r: r.is_vn == True)
        elif next_validator == 'direction':
            validators = list_validator.filtered(lambda r: r.is_direction == True)

        if not validators:
            raise UserError(
                'Liste de validation invalide, veuillez demander a l\'administrateur de configurer les niveaux de validation de prélèvement.')

        users = validators.mapped(lambda c: c.name)

        for user in users:
            self.message_post(body="Demande de validation", subject="Demande de validation",
                              partner_ids=[user[0].partner_id.id])
            self.message_subscribe(partner_ids=user[0].partner_id.ids)

    def button_request(self):
        self.launch_validation('sav_chief')
        return self.write({'state': 'request'})

    def button_chief_sav(self):
        self.launch_validation('automotive')
        return self.write({'state': 'confirmed', 'sav_validator': self.env.user.id})

    def button_automotive(self):
        self.launch_validation('vn')
        return self.write({'state': 'vin', 'automotive_validator': self.env.user.id})

    def button_dg(self):
        self.launch_validation('vn')
        return self.write({'state': 'vin', 'automotive_validator': self.env.user.id})

    def button_vn(self):
        if not self.vin_src:
            raise UserError('La fiche du véhicule {} doit avoir un numéro de série.'.format(self.vehicle_source.name))
        self.launch_validation('direction')
        self.transfert_prelevement_to_product()
        return self.write({'state': 'validate', 'vn_validator': self.env.user.id})

    def button_confirm(self):
        # POST FOR FOLLOWERS AFTER FINAL VALIDATION
        self.message_post(body="Ordre de prélèvement %s validé par %s" % (self.name, self.env.user.name),
                          subject="Order de prélèvement", partner_ids=self.demandeur.partner_id.ids)
        self.write({'state': 'withdraw', 'direction_validator': self.env.user.id})

    """
    Bouton pour les retours
    """

    def launch_return_validation(self, next_validator):
        """
        GET THE NEXT VALIDATOR FOR EACH STATE
        """
        list_validator = self._get_validators()

        if not list_validator:
            raise UserError(
                'Liste de validation invalide, veuillez demander a l\'administrateur de configurer les niveaux de validation de prélèvement.')

        users = self.env['res.users']

        # if next_validator == 'direction':
        #     validators = list_validator.filtered(lambda r: r.is_direction == True)
        if next_validator == 'automotive':
            validators = list_validator.filtered(lambda r: r.is_automotive == True)
        elif next_validator == 'sav_chief':
            validators = list_validator.filtered(lambda r: r.is_sav_chief == True)
        elif next_validator == 'vn':
            validators = list_validator.filtered(lambda r: r.is_vn == True)

        if not validators:
            raise UserError(
                'Liste de validation invalide, veuillez demander a l\'administrateur de configurer les niveaux de validation de prélèvement.')

        users = validators.mapped(lambda c: c.name)

        for user in users:
            self.message_post(body="Confirmation du retour pièces", subject="Demande de validation",
                              partner_ids=[user[0].partner_id.id])
            self.message_subscribe(partner_ids=user[0].partner_id.ids)

    def button_automotive2(self):
        self.launch_return_validation('sav_chief')
        return self.write({'state_return': 'sav_validate', 'automotive_validator': self.env.user.id})

    def button_chief_sav2(self):
        self.launch_return_validation('vn')
        return self.write({'state_return': 'vn_validate', 'sav_validator': self.env.user.id})

    def button_vn2(self):
        self.end_of_withdrawn()
        self.message_post(
            body="Véhicule remis en état : {} \n vin : {}".format(self.vehicle_src.name, self.vin_src.name),
            subject="Remise en état", partner_ids=self.automotive_validator.partner_id.ids)
        return self.write({'state_return': 'returned', 'vn_validator': self.env.user.id})


class ProductTemplatePrelevementBike(models.Model):
    _inherit = 'product.template'

    prelevement_ids = fields.One2many('prelevement.pieces', 'prelevement_id', copy=False)
    prelevement_count = fields.Float(compute='_compute_prelevement_count', string='Nbr prélèvement')

    @api.depends('prelevement_ids')
    def _compute_prelevement_count(self):
        for product in self:
            product.prelevement_count = len(product.prelevement_ids)

    def action_open_prelevement(self):
        return self.product_variant_ids.action_open_prelevement()

class ProductTemplatePrelevementTools(models.Model):
    _inherit = 'product.product'

    prelevement_count = fields.Float(related='product_tmpl_id.prelevement_count')
    is_withdrawn = fields.Boolean(string='Est prélèvé', default=False)

    def action_open_prelevement(self):
        action = self.env.ref('viseo_prelevement_pieces.prelevement_view_action').read()[0]
        domain = [('vehicle_src', 'in', self.ids)]
        prel = self.env['prelevement.pieces'].search(domain)
        if len(prel) > 1:
            action['domain'] = domain
        elif len(prel) == 0:
            action['domain'] = [('id', 'in', False)]
        elif prel:
            form_view = [(self.env.ref('viseo_prelevement_pieces.prelevement_pieces_view_form').id, 'form')]
            action['views'] = form_view
            action['res_id'] = prel.id
        action['context'] = dict(self._context, default_vehicle_src=self.id, )
        return action


    #=====================================================================================================================
    # Esorina anaty livrable ny voiture prélévé
    @api.depends("stock_move_ids.product_qty", "stock_move_ids.state")
    def _compute_qty_available_not_reserved(self):
        res = self._compute_product_available_not_res_dict()
        for prod in self:
            qty = res[prod.id]["qty_available_not_res"] - prod.prelevement_count
            prod.qty_available_not_res = qty
        return res
    #=====================================================================================================================


class QuantPrelevementTools(models.Model):
    _inherit = 'stock.quant'

    is_withdrawn = fields.Boolean(string='Est prélèvé', default=False)