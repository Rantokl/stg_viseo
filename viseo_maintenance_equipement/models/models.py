# -*- coding: utf-8 -*-
from datetime import datetime

from odoo import models, fields, api,SUPERUSER_ID
from odoo.exceptions import AccessError, ValidationError

from odoo.exceptions import UserError


# class viseo_maintenance_equipement(models.Model):
#     _name = 'viseo.maintenance.equipement'
#     _description = 'Maintenance des equipements internes'
#
#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
def check_user():
    return (SUPERUSER_ID) and True or False

class EquipementBT(models.Model):
    _name = 'equipement.bike.tools'
    _description = 'Equipement interne'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name= fields.Char()
    model = fields.Many2one('model.equipment', string="Modèle")
    owner_id = fields.Many2one('res.partner', string="Proprietaire")
    date_start = fields.Date('Date mise en service')
    cost_reported = fields.Float('Coût réportée(s)')
    emplacement= fields.Many2one('viseo.vehicle.location')
    address = fields.Char('Adresse')
    serial_number = fields.Char('Numéro de série')
    year_model = fields.Char('Année du modèle')
    partner_id = fields.Many2one('res.partner', string="Fournisseur")
    expire_date = fields.Date("Date d'expiration de garantie" )
    meeting_count = fields.Integer()
    contract_count = fields.Integer()
    fuel_logs_count= fields.Integer()
    cost_total = fields.Integer()
    maintenance_count = fields.Integer(compute='_compute_maint')
    equipment_type = fields.Selection(string="Tyde d'equipement", selection=[
        ('group','Groupe'),
        ('pont','Pont'),
        ('tools', 'Accessoires')
    ])

    def _compute_maint(self):
        for s in self:
            maint = self.env['maintenance.bike.tools'].sudo().search([('tools_id', '=', s.id)])
            s.maintenance_count = len(maint)

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

    name = fields.Char()


class MaintenanceBT(models.Model):
    _name = 'maintenance.bike.tools'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description="Maintenance des équipements"

    name=fields.Char()
    customer_id = fields.Many2one('res.partner', string="Client", related='tools_id.owner_id')
    tools_id = fields.Many2one('equipement.bike.tools')

    address = fields.Char('Adresse', related='customer_id.street')
    street2 = fields.Char('Adresse',related='customer_id.street2')
    city = fields.Char('Adresse',related='customer_id.city')
    previous_date = fields.Date('Date prévisionnelle')
    end_date= fields.Date('Date fin')
    invoice_date = fields.Date('Date de  facturation')

    state = fields.Selection(string="Status", selection=[
        ('draft', 'Réception'),
        ('diag', 'Diagnostique'),
        ('repared','Réparattion'),
        ('try','Essaie OK'),
        ('invoice','Facturation'),
        ('done','Livraison')
    ], default='draft')

    prelevement = fields.Integer('Prélevement')
    ndf = fields.Integer("Note de frais")
    purchase = fields.Integer("Achats")
    sale = fields.Integer("Devis")
    invoice = fields.Integer("Facture")
    equipment_type = fields.Selection(string="Tyde d'equipement", selection=[
        ('group', 'Groupe'),
        ('pont', 'Pont'),
        ('tools', 'Accessoires')
    ], related='tools_id.equipment_type')


    #check controle visuel
    #groupe electrogene
    oil = fields.Boolean("Niveau d'huile")
    freeze_liquid = fields.Boolean("Niveau de liquide de refroidissement")
    battery = fields.Boolean("Etat de la batterie")
    courroie = fields.Boolean("Etat des courroies")
    air_filter = fields.Boolean("Etat du filtre à air")
    radiator = fields.Boolean("Etat du radiateur")

    visual_comments = fields.Html()
    reception_comments = fields.Html()
    diagnostic = fields.One2many('maintenance.diagnostic', 'maintenance_id', string="Ligne(s) de diagnostique")
    service_work_id = fields.Many2one('maintenance.service.work', string="Type de travaux")
    product_list_id = fields.One2many('maintenance.product.list', 'repair_id', string="Article(s)")
    sale_service_id = fields.One2many('maintenance.servicesline', 'id_maintenance', string="Devis")

    #Controle Pont
    fixation = fields.Boolean(string="Fixation/Serrage chevilles")
    arm = fields.Boolean(string="Bras de levage/ Fin de course")
    roulement = fields.Boolean("Chemin de roulement")
    verin = fields.Boolean("Vérin + Fuite")
    synchronisme = fields.Boolean("Synchronisme et horizontalité")

    poulie = fields.Boolean("Poulie")
    cable = fields.Boolean("Cable")
    alim = fields.Boolean("Alimentation")
    stop_urgency = fields.Boolean("Arrêt d\'urgence")

    validity_date = fields.Date(string="Date d'expiration devis", track_visibility='onchange', copy=False)
    payment_term_id = fields.Many2one('account.payment.term', 'Conditions de règlement')

    amount_total = fields.Float('Montant HT', compute='compute_amount_ht')
    quotation_note = fields.Text('Note')


    product_lines = fields.One2many('maintenance.picking.product.line', 'maintenance', string="Livraison pièces", readonly=True)

    is_outside_control_done = fields.Boolean(default=False, copy=False, string='Contrôle visuel terminé')
    user_outside_controle = fields.Many2one('res.users', string='Controle extérieur par')
    time_user_outside_controle = fields.Datetime()
    is_diag_done = fields.Boolean(default=False, copy=False, string='Diagnostic terminé')
    user_diag = fields.Many2one('res.users', string='Diagnostic par')
    time_user_diag = fields.Datetime()
    is_transfert_done = fields.Boolean(default=False, copy=False, string='Transfert terminé')
    user_transfert_done = fields.Many2one('res.users', string='Transfert terminé par')
    time_user_transfert = fields.Datetime()
    can_start_repair = fields.Boolean(default=False, copy=False, string='Commencer réparation')
    user_start_repair = fields.Many2one('res.users', string='Autorisation de réparation par')
    time_user_start_repair = fields.Datetime()
    user_operation_ok = fields.Many2one('res.users', string='Opération validé par')
    time_user_operation_ok = fields.Datetime()
    is_repair_ok = fields.Boolean(default=False, copy=False, string='Réparation terminé')
    user_repair_ok = fields.Many2one('res.users', string='Réparation terminée par')
    time_user_repair_ok = fields.Datetime()
    is_trying_ok = fields.Boolean(default=False, copy=False, string='Essai ok')
    user_trying = fields.Many2one('res.users', string='Validation essaie par')
    time_user_trying = fields.Datetime()
    is_invoiced = fields.Boolean(default=False, copy=False, string='Ordre de réparation facturé')
    user_invoiced = fields.Many2one('res.users', string='Créateur facture')
    time_user_invoiced = fields.Datetime()
    # is_under_warranty = fields.Boolean(default=False, related='vehicle_id.is_under_warranty', store=True)
    is_valid_by_direction = fields.Boolean(default=False, string="Validation DG")
    time_user_valid_by_direction = fields.Datetime()
    direction_validator = fields.Many2one('res.users', string="DG")
    asked_valid_direction = fields.Boolean(default=False, string="Demande de validation à la direction")
    user_asked_valid_direction = fields.Many2one('res.users', string='Demande à la direction par')
    time_user_asked_valid_direction = fields.Datetime()
    user_automotive_ok = fields.Many2one('res.users', string='Automotive terminé par')
    time_user_automotive_ok = fields.Datetime()
    # user_debloc_automotive = fields.Many2one('res.users', string='Autorisé modification')
    user_pieces_ok = fields.Many2one('res.users', string="Pièces validées par")

    user_add_need = fields.Many2one('res.users', string="Besoin additif par")
    time_user_pieces_ok = fields.Datetime()
    user_quote_refuse = fields.Many2one('res.users', string="Devis refusé par")
    delivery = fields.Boolean(string='Transfert', compute='_compute_picking_ids')
    prelev_count = fields.Integer(string="Prélèvement", compute='_compute_prelev')
    # delivery_count_sav = fields.Integer(string='SAV', compute='_compute_picking_ids')
    # delivery_count_mg = fields.Integer(string='Delivery Orders', compute='_compute_picking_ids')

    #product_lines = fields.One2many('picking.product.line', 'repair_id', string="Livraison pièces", readonly=True)

    # invoice_value = fields.Monetary(string='Facture', compute='_count_values', readonly=True)
    # purchase_values = fields.Monetary(string='Achat', compute='_count_values', readonly=True)
    # expense_values = fields.Monetary(string='Note de frais', compute='_count_values', readonly=True)

    @api.model
    def create(self, sequence):
        sequence['name'] = self.env['ir.sequence'].next_by_code('maintenance.bike.tools') or '/'
        # place_pont = f"Place: {sequence.get('place_id')}" if sequence['place_id'] else f"Pont: {sequence.get('pont_id')}"
        sequence['name'] = f"{sequence['name']}"
        return super(MaintenanceBT, self).create(sequence)

    def get_current_user(self):
        current_user = self.env.user
        return current_user

    def _count_values(self):
        invoices = self.env['account.move'].sudo().search([('repair_id', '=', self.id), ('state', '!=', 'cancel'), ('type', '=', 'out_invoice')])
        purchases = self.env['purchase.order'].search([('repair_id', '=', self.id), ('state', 'in', ['purchase', 'done'])])
        expenses = self.env['hr.expense'].search([('repair_id', '=', self.id), ('state', '=', 'done')])
        # in_requests = self.env['internal.request'].search([('repair_id', '=', self.id), ('state', '!=', 'rejected')])
        self.invoice_value = sum(invoices.mapped('amount_total'))
        self.purchase_values = sum(purchases.mapped('amount_total'))
        self.expense_values = sum(expenses.mapped('total_amount'))

    def action_note_frais(self):
        action = self.env.ref('hr_expense.hr_expense_actions_my_unsubmitted').read()[0]
        domain = [('maintenance_id', '=', self.id)]
        ndf = self.env['hr.expense'].search(domain)

        if len(ndf) > 1 or len(ndf) == 0:
            action['domain'] = domain
        elif ndf:
            form_view = [(self.env.ref('hr_expense.hr_expense_view_form').id, 'form')]
            action['views'] = form_view
            action['res_id'] = ndf.id
        action['context'] = dict(self._context, default_maintenance_id=self.id)

        return action

    def ask_purchase_maintenance(self):
        action = self.env.ref('purchase.purchase_rfq').read()[0]
        domain = [('maintenance_id', '=', self.id)]
        purchase = self.env['purchase.order'].search(domain)

        if len(purchase) > 1 or len(purchase) == 0:
            action['domain'] = domain
        elif purchase:
            form_view = [(self.env.ref('purchase.purchase_order_form').id, 'form')]
            action['views'] = form_view
            action['res_id'] = purchase.id
        action['context'] = dict(self._context, default_maintenance_id=self.id)
        return action

    def action_outside_control_done(self):
        # Notif
        self.notification_rma(u"Contrôle visuel terminé.", 'visual_control')

        return self.write({'is_outside_control_done': True, 'state': 'diag', 'user_outside_controle': self.get_current_user().id, 'time_user_outside_controle': datetime.today()})

    def notification_rma(self, message, button):
        """FUNCTION FOR NOTIFICATION WITH RULES"""
        if self.user_outside_controle:
            user_control = self.user_outside_controle.id
        else:
            user_control = self.env.user.id
        rules = self.env['maintenance.repair.rules'].search([('visual_control','=',user_control)])
        admin = self.env['res.users'].search([('login', '=', 'admin')])
        users = self.env['res.users']
        if not rules:
            raise UserError("Veuillez demander à l'administrateur de vous inscrire dans une règle de Bike & Tools")
        if button == 'visual_control':
            if not rules[0].operation:
                raise UserError("Veuillez demander à l'administrateur de configurer les utilisateurs dans opération")
            users = rules[0].operation
        elif button == 'diag_done':
            if not rules[0].automotive:
                raise UserError("Veuillez demander à l'administrateur de configurer les utilisateurs dans automotive")
            users = rules[0].automotive
        elif button in ['automotive_done','pieces_done']:
            sav_responsible = rules[0].sav_chief
            users = self.user_outside_controle + self.user_diag + sav_responsible
        elif button in ['transfert_done','start_repair']:
            users = self.user_outside_controle + self.user_diag + self.user_pieces_ok
        elif button == 'end_repair':
            users = self.user_outside_controle + self.user_diag + self.user_pieces_ok + self.user_start_repair
        elif button == 'essai_ok':
            if not rules[0].sav_chief:
                raise UserError("Veuillez demander à l'administrateur de configurer les utilisateurs dans automotive")
            sav_responsible = rules[0].sav_chief
            users = self.user_outside_controle + self.user_diag + self.user_pieces_ok + self.user_start_repair + self.user_repair_ok + sav_responsible
        elif button == 'additive_need':
            if not rules[0].automotive:
                raise UserError("Veuillez demander à l'administrateur de configurer les utilisateurs dans automotive")
            users = self.user_automotive_ok if self.user_automotive_ok else rules[0].automotive
        elif button == 'quote_refused':
            if not rules[0].sav_chief:
                raise UserError("Veuillez demander à l'administrateur de configurer les utilisateurs dans automotive")
            sav_responsible = rules[0].sav_chief
            users = self.user_outside_controle + sav_responsible

        to_notify = users - admin

        body_message = (("<div class='col-xs-6'>"
                           "<ul>"
                           "<li><i>%s</i></li>"
                           "</ul>"
                           "</div>")%(message))
        self.message_post(body = body_message, subject = u"Ordre de réparation", partner_ids = to_notify.partner_id.ids)

    is_additive_quotation = fields.Boolean(string="need_additive_quotation")

    def action_quotation_create(self):
        # Notif
        # TODO notification Magasinier

        product = self.fleet_servicesline_ids.filtered(lambda j: j.state in ['none']).mapped('product_id')
        sale_order = self.env['sale.order']

        # create order for an existing product
        if not self.validity_date:
            raise UserError("Vous ne pouvez pas créer un nouveau devis sans date d'expiration devis")

        order_line = []
        for record in product.ids:
            z = dict(product_id=record)
            order_line.append(z)

        so = self._get_dict_value(product, order_line, 'order', fournisseur=None, repair_id=self.id)

        current_fleet_servicesline = self.fleet_servicesline_ids.filtered(lambda j: j.state in ['none'])

        if current_fleet_servicesline:
            order_id = sale_order.sudo().create(so)
            order_id.write({'validity_date' : self.validity_date})
            self.create_order_line_with_this_so_po(so, product, 'order', date_planned=None)
            for f in current_fleet_servicesline:
                f.state = 'devis'
                f.sale_id = order_id.id
        self.message_subscribe(partner_ids=self.env.user.partner_id.ids)
        self.write({'is_quotation_created': True, 'time_user_quotation_created': datetime.today()})

    def action_quotation_create_additive(self):
        self.action_quotation_create()
        self.update({
            'is_additive_quotation': False,
            'asked_valid_direction': False,
            'is_valid_by_direction': False
        })

    def action_diag_done(self):
        if  not self.is_additive_quotation:
            self.notification_rma(u"Diagnostic terminé", 'diag_done')
            self.message_subscribe(partner_ids=self.env.user.partner_id.ids)
            self.is_diag_done = True
            self.user_diag = self.get_current_user().id
            contract = self.env['fleet.vehicle.log.contract'].search(
                [('state', 'in', ['open', 'diesoon']), ('cost_subtype_id.name', '=', 'Contrat Sav'),
                 ('vehicle_id', '=', self.vehicle_id.id)], order='id desc', limit=1)
            type_work = contract.type_work_ids.filtered(
                lambda x: x.servicing_id == self.service_work_id and x.is_reserved == True and x.is_done == False)
            for list in self.product_list_id:
                product_contract = type_work.product_ids.filtered(lambda x:x.product_id == list.product_id)
                order_line = self.env['fleet.servicesline']
                vals = {
                    'pieces': list.name,
                    'product_uom_qty': list.product_qty,
                    'fleet_servicesline_id': list.repair_id.id,
                    'price_unit': product_contract.price_unit,
                    'name': list.product_id.name if not list.display_type else list.name,
                    'tax_id': list.product_id.taxes_id,
                    'product_id': list.product_id.id,
                    'display_type': list.display_type,
                    'is_product_from_contract': True
                }
                order_line.create(vals)
        else:
            return super(MaintenanceBT, self).action_diag_done()

    def get_view_context(self):
        self.ensure_one()
        equipment_type = self.tools_id.equipment_type if self.tools_id else None
        return {
            'equipment_type': equipment_type,
        }


    @api.depends('sale_service_id')
    def compute_amount_ht(self):
        amount = 0
        for record in self.sale_service_id:
            if record.count_total:
                amount += record.product_uom_qty * record.price_unit
        self.amount_total = amount



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

    maintenance = fields.Many2one('maintenance.bike.tools')
    location_id = fields.Many2one('stock.location', 'Emplacement', required=True, related='picking_magasinier.location_id')
    location_name = fields.Char('Emplacement', related='location_id.name')
    # product_id = fields.Many2one('product.product', 'Article', required=True)
    picking_magasinier = fields.Many2one('stock.picking', 'Livraison vers Atelier', required=True)
    picking_sav = fields.Many2one('stock.picking', 'Reception Atelier')
    picking_return_sav = fields.Many2one('stock.picking', 'Retour vers Magasin')
    picking_return_mg = fields.Many2one('stock.picking', 'Reception magasin')
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




