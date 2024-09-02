# -*- coding: utf-8 -*-
from datetime import datetime

from odoo import models, fields, api,SUPERUSER_ID
from odoo.exceptions import AccessError, ValidationError

from odoo.exceptions import UserError


def check_user():
    return (SUPERUSER_ID) and True or False

class EquipementBT(models.Model):
    _name = 'equipement.bike.tools'
    _description = 'Equipement interne'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name= fields.Char(required=True)
    model = fields.Many2one('model.equipment', string="Modèle", tracking=True)
    owner_id = fields.Many2one('res.partner', string="Proprietaire", tracking=True)
    date_start = fields.Date('Date mise en service', tracking=True)
    # cost_reported = fields.Float('Coût réportée(s)')
    image = fields.Binary("Image", attachment=True, tracking=True)
    # emplacement= fields.Many2one('viseo.vehicle.location')
    address = fields.Char('Adresse', copy=False, tracking=True)
    serial_number = fields.Char('Numéro de série', copy=False, tracking=True)
    # year_model = fields.Char('Année du modèle')
    # partner_id = fields.Many2one('res.partner', string="Fournisseur")
    # expire_date = fields.Date("Date d'expiration de garantie", compute='_compute_date_waranty' )
    expire_date = fields.Date("Date d'expiration de garantie", tracking=True)
    # meeting_count = fields.Integer()
    # contract_count = fields.Integer(compute='_compute_contrat')
    currency_id = fields.Many2one('res.currency', string="Devise", default=lambda self: self.env.company.currency_id)
    fuel_logs_count = fields.Integer()
    cost_total = fields.Monetary(compute="_compute_invoice")
    maintenance_count = fields.Integer(compute='_compute_maint')
    equipment_type = fields.Selection(string="Tyde d'equipement", selection=[
        ('group','Groupe'),
        ('pont','Pont'),
        ('compressor', 'Compresseur'),
        ('other', 'Autres')
    ])

    #Calcul des couts
    def _compute_invoice(self):
        for s in self:
            invoices = self.env['account.move'].sudo().search(
                [('maintenance_id.tools_id', '=', self.id), ('state', '!=', 'cancel'), ('type', '=', 'out_invoice')])
            s.cost_total = sum([invoice.amount_total for invoice in invoices])

    # def _compute_date_waranty(self):
    #     contract = self.env['equipment.log.contract'].sudo().search([('equipment_id','=',self.id)])
    #     if contract:
    #         self.expire_date = contract.expiration_date
    #     else:
    #         self.expire_date = None


    #Compute total des maintenances
    def _compute_maint(self):

        for s in self:
            # contrat = self.env['equipment.log.contract'].sudo().search([('equipment_id', '=', s.id)])
            maint = self.env['maintenance.bike.tools'].sudo().search([('tools_id', '=', s.id)])
            s.maintenance_count = len(maint)
            # s.contract_count = len(contrat)



    # def _compute_contrat(self):
    #
    #     for s in self:
    #         contrat = self.env['equipment.log.contract'].sudo().search([('equipment_id', '=', s.id)])
    #         # maint = self.env['maintenance.bike.tools'].sudo().search([('tools_id', '=', s.id)])
    #         # s.maintenance_count = len(maint)
    #         s.contract_count = len(contrat)

    #Methode pour ouvrir les factures
    def action_view_cost_logs(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Facture',
            'view_mode': 'tree,form',
            'res_model': 'account.move',
            'domain': [('maintenance_id.tools_id', '=', self.id)],

        }


    def return_action_to_open(self):
        """ This opens the xml view specified in xml_id for the current equipement """
        self.ensure_one()
        xml_id = self.env.context.get('xml_id')
        if xml_id:
            res = self.env['ir.actions.act_window'].for_xml_id('fleet', xml_id)
            res.update(
                context=dict(self.env.context, default_equipement_id=self.id, default_customer_id=self.owner_id.id, group_by=False),
                domain=[('equipement_id', '=', self.id)],
                view_mode='tree,form',
                views=[(False, 'tree'), (False, 'form')],
            )
            return res
        return False


    # def return_action_to_open_contrat(self):
    #
    #     self.ensure_one()
    #     return {
    #         'type': 'ir.actions.act_window',
    #         'name': 'Contrat',
    #         'view_mode': 'tree,form',
    #         'res_model': 'equipment.log.contract',
    #         'domain':[('equipment_id','=',self.id),('contract_owner','=',self.owner_id.id)],
    #         'context': {'default_equipment_id': self.id,
    #                     'default_contract_owner': self.owner_id.id,
    #
    #                     },
    #     }

    #Vue maintenance
    def return_action_to_open_maintenance(self):

        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Maintenance',
            'view_mode': 'tree,form',
            'res_model': 'maintenance.bike.tools',
            'domain':[('tools_id','=',self.id),('customer_id','=',self.owner_id.id)],
            'context': {'default_tools_id': self.id,
                        'default_customer_id': self.owner_id.id,

                        },
        }


class ModelEquipement(models.Model):
    _name = 'model.equipment'

    name = fields.Char("Modèle", required=True)
    marque = fields.Many2one('viseo.brand', string="Marque")

class Diagnostic(models.Model):
    _name = 'maintenance.diagnostic'

    name = fields.Char()
    maintenance_id = fields.Many2one('maintenance.bike.tools', string="Ref maintenance")

class ServiceWorkType(models.Model):
    _name = 'maintenance.service.work'

    name = fields.Char()

class MaintenanceProductList(models.Model):
    _name = 'maintenance.product.list'
    _description = 'Liste des pièces à fournir'

    name = fields.Char(string="Libre")
    product_id = fields.Many2one('product.product', string='Articles')
    product_qty = fields.Float(string="Qté", default=0)
    product_uom = fields.Many2one('uom.uom', related="product_id.uom_id", string="UdM")
    observation = fields.Char(string="OBS")
    repair_id = fields.Many2one('maintenance.bike.tools')
    display_type = fields.Selection([
        ('line_section', "Section"),
        ('line_note', "Note")], default=False, help="Technical field.")
    operation_done = fields.Char(string="Opérations effectuées")
    time_done = fields.Float(string="Temps passé")
    technician = fields.Many2many('hr.employee', string='Intervenants', copy=False)


class MaintenanceLogServicesLine(models.Model):
    _name = 'maintenance.servicesline'
    _description = 'Line Service'

    name = fields.Char(string="Description")
    product_id = fields.Many2one('product.product', string="Article")
    product_uom_qty = fields.Float(string="Quantité")
    price_unit = fields.Float(string="Prix Unitaire")
    price_subtotal = fields.Float(string="Sous-Total HT")
    to_invoice = fields.Boolean(string="A facturer?")
    tax_id = fields.Many2many('account.tax', string="Taxes")
    invoiced = fields.Selection(string="Etat de facturation",
                                selection=[('not_invoiced', 'Non Facturé'), ('invoiced', 'Facturé')],
                                default='not_invoiced', readonly="True")
    location_id = fields.Many2one('stock.location', string="Emplacement d'origine")
    location_dest_id = fields.Many2one('stock.location', string="Emplacement de Destination")
    id_maintenance = fields.Many2one('maintenance.bike.tools')
    discount = fields.Float('Remise(%)')
    to_purchase = fields.Boolean('A acheter?')
    not_reserved_qty = fields.Float(string="Dispo", related='product_id.qty_available_not_res')
    count_total = fields.Boolean(default=True)
    pieces = fields.Char(string="Pièces")
    brand_id = fields.Many2one('viseo.brand', string="Marque", related='product_id.product_tmpl_id.brand_id')
    display_type = fields.Selection([
        ('line_section', "Section"),
        ('line_note', "Note")], default=False, help="Technical field.")
    rest_qty = fields.Float("Livré")
    available_quantity = fields.Float(string="Dispo", compute='_compute_qty_in_stock')
    qty_prel = fields.Float(string="à prelever")
    company_id = fields.Many2one('res.company', string='Société', compute='_compute_company_id')

    #####################################################################""
    #   Ajout du champ pour l'article dans le devis

    def _compute_company_id(self):
        for line in self:
            line.company_id = line.id_maintenance.company_id

    @api.depends('product_id')
    def _compute_qty_in_stock(self):
        for line in self:
            availables = 0
            domain = [('product_id', '=', line.product_id.id), ('location_id.usage', '=', 'internal'),
                      ('location_id.name', 'not in', ['SAVOT', 'SAVCA'])]
            quants = self.env['stock.quant'].search(domain)
            for quant in quants:
                availables += quant.available_quantity
            line.available_quantity = availables

    state = fields.Selection(string=u'Etat', selection=[('devis', 'devis'), ('none', 'aucun'), ], default='none')
    is_purchase = fields.Boolean()
    sale_id = fields.Many2one('sale.order')

    def check_access_sale(self):
        current_user = self.env.user
        price = self.product_id.lst_price
        if self.price_unit < price:
            if not current_user.has_group('viseo_sales_price_update.can_discounted_price'):
                self.write({'discount': 0})

            if not current_user.has_group('viseo_sale_price.strict_only_admin'):
                raise ValidationError("Impossible de rabaisser le prix du %s (%s)" % (self.product_id.name, price))

        elif self.price_unit > price:
            if not current_user.has_group('viseo_sales_price_update.can_discounted_price'):
                self.write({'discount': 0})

            if current_user.has_group('viseo_sale_price.raise_price_quotation_product'):
                if not self.product_id.autorized_update_price:
                    raise ValidationError(
                        "Vous n'êtes pas autorisé à augmenter le prix du %s (%s)" % (self.product_id.name, price))

            elif not current_user.has_group('viseo_sale_price.raise_price_quotation'):
                raise ValidationError("Impossible d'augmenter le prix du %s (%s)" % (self.product_id.name, price))

    @api.onchange('price_unit')
    def _check_price_unit(self):
        self.check_access_sale()

    @api.onchange('discount')
    def _reconfirm_max_discount(self):
        self.check_access_sale()
        dc = self.env.user.discount_max
        if check_user:
            if self.discount > dc:
                mess_error = ("Votre plafond de remise est de {discount}".format(discount=dc))
                raise AccessError(mess_error)

    @api.onchange('product_id', 'product_uom_qty')
    def onchange_product_id(self):
        partner = self.id_maintenance.customer_id
        self.name = self.product_id.name
        self.price_unit = self.product_id.lst_price
        self.tax_id = self.product_id.taxes_id
        self.product_uom = self.product_id.uom_id.id
        self.price_subtotal = self.product_uom_qty * self.price_unit

    @api.onchange('price_unit')
    def onchange_price_unit(self):
        self.price_subtotal = self.price_unit * self.product_uom_qty

    def MajSo(self):
        if not self.sale_id:
            raise UserError(u"Il n\'y a pas de devise associé à cette ligne")
        else:
            sol = self.env['sale.order.line'].search(
                [('product_id', '=', self.product_id.id), ('order_id', '=', self.sale_id.id)])
            if sol:
                if self.to_invoice:
                    sol.write({'price_unit': self.price_unit})


class MaintenanceWorkType(models.Model):
    _name = 'maintenance.picking.product.line'

    maintenance_id = fields.Many2one('maintenance.bike.tools')
    location_id = fields.Many2one('stock.location', 'Emplacement', required=True, related='picking_magasinier.location_id')
    location_name = fields.Char('Emplacement', related='location_id.name')
    # product_id = fields.Many2one('product.product', 'Article', required=True)
    picking_magasinier = fields.Many2one('stock.picking', 'Livraison vers Atelier', required=True)
    picking_sav = fields.Many2one('stock.picking', 'Reception Atelier')
    # picking_return_sav = fields.Many2one('stock.picking', 'Retour vers Magasin')
    # picking_return_mg = fields.Many2one('stock.picking', 'Reception magasin')
    # product_ref = fields.Char('Ref interne', related="product_id.default_code")
    # product_name = fields.Char('Désignation', related="product_id.name")
    # qty = fields.Float("Qté")
    # rest_qty = fields.Float("Reste à livrer")
    is_transfert_mg_ok = fields.Boolean(default=False)
    is_transfert_sav_ok = fields.Boolean(default=False)
    is_return_sav_ok = fields.Boolean(default=False)
    is_return_mg_ok = fields.Boolean(default=False)

    # rest_qty = fields.Float("Reste à livrer")

    @api.depends('is_transfert_sav_ok')
    def action_test(self):
        for line in self:
            if line.is_transfert_sav_ok:
                line.picking_return_sav = line.picking_sav.id


class MaintenanceExpense(models.Model):
    _inherit='hr.expense'

    maintenance_id = fields.Many2one('maintenance.bike.tools', "Ref maintenance")
    is_maint_valid_by_direction = fields.Boolean("Maintenance validé par la Direction")

class MaintenanceExpensePurchase(models.Model):
    _inherit = 'purchase.order'

    maintenance_id = fields.Many2one('maintenance.bike.tools', "Ref maintenance")
    is_maint_valid_by_direction = fields.Boolean("Maintenance validé par la Direction")

class MaintenanceSaleOrder(models.Model):
    _inherit = 'sale.order'

    maintenance_id = fields.Many2one('maintenance.bike.tools', "Document d'origine")



    def _action_confirm(self):
        res = super(MaintenanceSaleOrder, self)._action_confirm()
        # Ajouter le rma sur le transfert
        if self.maintenance_id:
            for picking in self.picking_ids:
                if picking.state not in ('done', 'cancel', 'split', 'partially_available'):
                    picking.sudo().write({'maintenance_id': self.maintenance_id.id})
        return res

    def action_confirm(self):

        res = super(MaintenanceSaleOrder, self).action_confirm()

        if self.maintenance_id:
            for picking in self.picking_ids:
                if picking.state not in ('done', 'cancel', 'split', 'partially_available'):
                    picking.sudo().write({'maintenance_id': self.maintenance_id.id})

        # Ajouter le rma sur le transfert

        return res

class AccountMoveInheritMaintenance(models.Model):
    _inherit = 'account.move'

    maintenance_id = fields.Many2one('maintenance.bike.tools')

class StockPickingMaintenance(models.Model):
    _inherit = 'stock.picking'

    maintenance_id = fields.Many2one('maintenance.bike.tools')

    def internal_transfer_viseo(self):
        des_location_mg = self.get_temp_location(self.company_id.id).id
        if self.picking_type_id.code == 'internal' and self.location_id.id != des_location_mg:
            location_id = des_location_mg
            original_destination_id = self.location_dest_id
            self.write({'location_dest_id': location_id})

            for move_line in self.move_line_ids_without_package:
                move_line.write({'location_dest_id': location_id})

            line_moves = []
            # if self.location_dest_id.id != des_location_mg.id:
            if original_destination_id.id != des_location_mg:
                for line in self.move_ids_without_package:
                    line_moves.append([0, False, {
                        'name': line.product_id.name,
                        'product_id': line.product_id.id,
                        'product_uom_qty': line.quantity_done,
                        'product_uom': line.product_uom.id,
                        'date': datetime.today(),
                        'location_id': location_id,
                        'location_dest_id': original_destination_id.id,
                        'company_id': self.company_id.id,
                        'state': 'draft'}])
                # ---------- passer valeur sale_id, et repair_id si elles existent -----------
                vals = {
                    'group_id': self.group_id.id,
                    'repair_id': self.repair_id.id or False,
                    'sale_id' : self.sale_id.id,
                    'partner_id': self.partner_id.id,
                    'picking_type_id': self.picking_type_id.id,
                    'location_id': location_id,
                    'location_dest_id': original_destination_id.id,
                    'move_ids_without_package': line_moves,
                    'origin': self.name,
                    'company_id': self.company_id.id,
                    'create_date': datetime.today(),
                    'write_date': datetime.today(),
                }
                if vals['location_id'] != vals['location_dest_id']:
                    picking = self.create(vals)
                    picking.action_confirm()
                    picking.action_assign()
                    self.write({'bound_picking_id': picking.id, 'location_dest_id': location_id})
                    if self.repair_id:
                        if self.repair_id and not self.backorder_id:
                            transfert_lines = self.repair_id.product_lines
                            for line_t in transfert_lines:
                                if line_t.picking_magasinier.id == self.id:
                                    line_t.picking_sav = picking.id
                                    break

                            move_lines = self.move_ids_without_package
                            fleet_servicelines_ids = self.repair_id.fleet_servicesline_ids

                            for mov in move_lines:
                                for sln in fleet_servicelines_ids:
                                    if mov.product_id.id == sln.product_id.id:
                                        # rest_qty = sln.product_uom_qty - mov.quantity_done
                                        rest_qty = mov.quantity_done
                                        self.repair_id.sudo().write(
                                            {'fleet_servicesline_ids': [(1, sln.id, {'rest_qty': rest_qty})]})

                        ############################################# création reliquat SAV‘#########################
                        else:
                            if self.repair_id and self.backorder_id:
                                if self.location_dest_id.id == des_location_mg:
                                    # picking = self
                                    transfert_lines = self.repair_id.product_lines
                                    dest_sav_location = self.env['stock.location'].search(
                                        [('usage', '=', 'internal'), ('company_id', '=', self.company_id.id),
                                         ('name', 'like', 'SAV%')],
                                        limit=1)
                                    sav_backorder_picking = self.copy()
                                    sav_backorder_picking.write({'location_id': des_location_mg, 'location_dest_id': dest_sav_location.id})
                                    for move in sav_backorder_picking.move_lines:
                                        move.write(
                                            {'location_id': sav_backorder_picking.location_id.id, 'location_dest_id': sav_backorder_picking.location_dest_id.id})
                                    # sav_backorder_picking.action_confirm()
                                    sav_backorder_picking.action_assign()
                                    ###############################################
                                    for line_t in transfert_lines:
                                        if line_t.picking_magasinier.id == self.id:
                                            line_t.picking_sav = sav_backorder_picking.id
                                            break

                                    move_lines = self.move_ids_without_package
                                    fleet_servicelines_ids = self.repair_id.fleet_servicesline_ids

                                    for mov in move_lines:
                                        for sln in fleet_servicelines_ids:
                                            if mov.product_id.id == sln.product_id.id:
                                                # rest_qty = sln.product_uom_qty - (sln.rest_qty + mov.quantity_done)
                                                rest_qty = sln.rest_qty + mov.quantity_done
                                                self.repair_id.sudo().write(
                                                    {'fleet_servicesline_ids': [(1, sln.id, {'rest_qty': rest_qty})]})

                    elif self.maintenance_id:
                        if self.maintenance_id and not self.backorder_id:
                            transfert_lines = self.maintenance_id.product_lines
                            for line_t in transfert_lines:
                                if line_t.picking_magasinier.id == self.id:
                                    line_t.picking_sav = picking.id
                                    break

                            move_lines = self.move_ids_without_package
                            maintenance_servicelines_ids = self.maintenance_id.sale_service_id

                            for mov in move_lines:
                                for sln in maintenance_servicelines_ids:
                                    if mov.product_id.id == sln.product_id.id:
                                        # rest_qty = sln.product_uom_qty - mov.quantity_done
                                        rest_qty = mov.quantity_done
                                        self.maintenance_id.sudo().write(
                                            {'sale_service_id': [(1, sln.id, {'rest_qty': rest_qty})]})

                        ############################################# création reliquat SAV‘#########################
                        else:
                            if self.maintenance_id and self.backorder_id:
                                if self.location_dest_id.id == des_location_mg:
                                    # picking = self
                                    transfert_lines = self.maintenance_id.product_lines
                                    dest_sav_location = self.env['stock.location'].search(
                                        [('usage', '=', 'internal'), ('company_id', '=', self.company_id.id),
                                         ('name', 'like', 'Tools%')],
                                        limit=1)
                                    sav_backorder_picking = self.copy()
                                    sav_backorder_picking.write(
                                        {'location_id': des_location_mg, 'location_dest_id': dest_sav_location.id})
                                    for move in sav_backorder_picking.move_lines:
                                        move.write(
                                            {'location_id': sav_backorder_picking.location_id.id,
                                             'location_dest_id': sav_backorder_picking.location_dest_id.id})
                                    # sav_backorder_picking.action_confirm()
                                    sav_backorder_picking.action_assign()
                                    ###############################################
                                    for line_t in transfert_lines:
                                        if line_t.picking_magasinier.id == self.id:
                                            line_t.picking_sav = sav_backorder_picking.id
                                            break

                                    move_lines = self.move_ids_without_package
                                    fleet_servicelines_ids = self.maintenance_id.sale_service_id

                                    for mov in move_lines:
                                        for sln in fleet_servicelines_ids:
                                            if mov.product_id.id == sln.product_id.id:
                                                # rest_qty = sln.product_uom_qty - (sln.rest_qty + mov.quantity_done)
                                                rest_qty = sln.rest_qty + mov.quantity_done
                                                self.maintenance_id.sudo().write(
                                                    {'sale_service_id': [(1, sln.id, {'rest_qty': rest_qty})]})


class StockRuleMaintenance(models.Model):
    _inherit = 'stock.rule'

    def _check_rules_and_get_moves(self, src_location, location_id, origin, product_id, values, company_id, product_qty,
                                   product_uom, name, partner, group_id, date_expected):
        res = super(StockRuleMaintenance, self)._check_rules_and_get_moves(src_location, location_id, origin, product_id, values, company_id, product_qty,
                                   product_uom, name, partner, group_id, date_expected)

        sale_id = self.env['sale.order'].search([('name', '=', origin)])

        if sale_id.maintenance_id:
            destination = self.env['stock.location']
            dest_loc = destination.search(
                [('company_id', '=', company_id.id), ('name', '=like', 'Tools%')])

        rules = self.env['stock.rule'].search([('company_id', '=', company_id.id), ('action', '=', 'pull'),
                                               ('procure_method', '=', 'make_to_stock'),
                                               ('picking_type_id.name', '=', 'Transferts Internes'),
                                               ('sequence', '=', 20)])

        if not rules:
            raise UserError("Aucune règle ne correspond à votre choix d'emplacement, verifier route et/ou emplacement")
        else:
            location = src_location.id
            # if sale_id.from_mrp_operation:
            location_id = dest_loc
            rule_id = rules.id
            picking_type_id = rules.picking_type_id.id

        res.update({
            'location_id': location,
            'location_dest_id': location_id.id,
            'rule_id': rule_id,
            'picking_type_id': picking_type_id,
        })

        return res


class InvoiceChoiceMaintenance(models.TransientModel):
    _name = 'invoice.choice.maintenance.wizard'

    maintenance_id = fields.Many2one('maintenance.bike.tools')
    advance_invoice_method = fields.Selection([
        ('one_invoice', 'Une Seule facture'),
        ('multi_invoice', 'Une facture par devis')
    ], string='Créer facture', default='one_invoice', required=True,
        help="Une seule facture suffit pour une maintenance mais si en cas de besoin vous pouvez choisir une facture par devis")

    def action_validate(self):

        sale_orders = self.env['sale.order'].search([('maintenance_id', '=', self.maintenance_id.id), ('state', 'in', ['sale', 'done']), ('is_quote_expired', '=', False)])
        account_department_id = sale_orders[0].account_department_id
        if self.advance_invoice_method == 'one_invoice':
            invoice = sale_orders._create_invoices(grouped=False, final=True)
            invoice.write({'account_department_id' : account_department_id.id, 'maintenance_id' : self.maintenance_id.id})
            self.maintenance_id.write({'is_invoiced': True,
                                'user_invoiced': self.env.user.id,
                                'time_user_invoiced': datetime.today(),
                                'state': 'invoice'})
        else:
            invoices = self.env['account.move']
            for sale in sale_orders:
                invoices |= sale._create_invoices(grouped=True, final=True)
            self.repair_id.write({'is_invoiced': True,
                                   'user_invoiced': self.env.user.id,
                                  'time_user_invoiced': datetime.today(),
                                  'state_ro': 'invoice'})

            for inv in invoices:
                inv.write({'account_department_id': account_department_id.id, 'maintenance_id' : self.maintenance_id.id})


class QuotationRefuseMaintenance(models.TransientModel):
    _name = 'quotation.refuse.maintenance'


    line_ids = fields.One2many('quotation.refuse.line', 'quotation_refuse_id', string="Ligne à facturer")
    amount_untaxed = fields.Float(string="Montant HT", compute="compute_amount_ht")
    note = fields.Text(string="Observation")

    maintenance_id = fields.Many2one('maintenance.bike.tools', strng="Ref maintenance")

    @api.depends('line_ids')
    def compute_amount_ht(self):
        amount = 0
        for record in self.line_ids:
            amount += record.price_unit
        self.amount_untaxed = amount

    def action_confirm(self):

        if self.maintenance_id:
            self.maintenance_id.update({
                'user_quote_refuse': self.env.user.id,
            })

            invoice_line = []
            for line in self.line_ids:
                invoice_line.append((
                    0, None, {
                        'name': line.description if line.description else line.product_id.name,
                        'product_id': line.product_id.id,
                        'quantity': 1,
                        'price_unit': line.price_unit,
                        'tax_ids': line.tax_ids.ids,
                    }
                ))

            sales = self.env['sale.order'].sudo().search([('maintenance_id','=',self.maintenance_id.id)])

            if invoice_line:
                move = self.env['account.move'].create({
                    'type': 'out_invoice',
                    'partner_id': self.maintenance_id.customer_id.id,
                    'partner_shipping_id': self.maintenance_id.customer_id.id,
                    'invoice_payment_term_id': self.maintenance_id.customer_id.property_payment_term_id.id,
                    'maintenance_id': self.maintenance_id.id,
                    'invoice_origin': self.maintenance_id.name,
                    'narration': self.note,
                    'invoice_line_ids': invoice_line,
                    })

                # Notif
                self.maintenance_id.notification_rma(u'Facture de diagnostic créée.', 'quote_refused')
                self.maintenance_id.update({
                    'state': 'done',
                    'is_invoiced': True,
                    'date_livraison': datetime.now(),
                    'is_delivered': True,
                })

            elif sales:
                self.maintenance_id.update({
                    'state': 'done',
                    'is_invoiced': True,
                    'date_livraison': datetime.now(),
                    'is_delivered': True,
                })

            else:
                self.maintenance_id.update({
                    'state': 'cancel',
                    'last_state': self.maintenance_id.state,
                    'cancel_reason': self.note,
                })













