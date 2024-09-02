# -*- coding: utf-8 -*-

from odoo import fields, models, api
from datetime import datetime
from odoo import models, fields, api,SUPERUSER_ID
from odoo.exceptions import UserError

class MaintenanceBT(models.Model):
    _name = 'maintenance.bike.tools'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description="Maintenance des équipements"

    name = fields.Char(tracking=True)
    customer_id = fields.Many2one('res.partner', string="Client", related='tools_id.owner_id')
    tools_id = fields.Many2one('equipement.bike.tools')

    address = fields.Char('Adresse', related='customer_id.street')
    street2 = fields.Char('Adresse',related='customer_id.street2')
    city = fields.Char('Adresse',related='customer_id.city')
    previous_date = fields.Date('Date prévisionnelle')
    end_date= fields.Date('Date fin')
    invoice_date = fields.Date('Date de  facturation')
    date_livraison = fields.Datetime("Date de livraison", required=False, track_visibility='onchange')

    state = fields.Selection(string="Status", selection=[
        ('draft', 'Réception'),
        ('diag', 'Diagnostique'),
        ('repair','Réparation'),
        ('try','Essaie OK'),
        ('invoice','Facturation'),
        ('done','Terminé'),
        ('cancel', 'Annulé')
    ], default='draft')


    cancel_reason = fields.Text(copy=False, track_visibility=True, string="Motif de l'annulation")
    last_state = fields.Char(string="Etat avant annulation")
    image = fields.Binary(related='tools_id.image', string="Image", readonly=True)

    prelevement = fields.Integer('Prélevement')
    currency_id = fields.Many2one('res.currency', string="Devise", default=lambda self: self.env.company.currency_id)
    ndf = fields.Monetary("Note de frais",compute='_count_sale_order')
    purchase = fields.Monetary("Achats",compute='_count_sale_order')
    sale = fields.Monetary("Devis", compute='_count_sale_order')
    invoice = fields.Monetary("Facture",compute='_count_sale_order')
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

    order_line_ids = fields.Many2many('sale.order', compute="_get_lines_devis")

    #Tools
    soupape = fields.Boolean("Soupape de sécurité")
    freeze_system = fields.Boolean("Système de refroidissement")
    pression = fields.Boolean("Pression et régulation")

    validity_date = fields.Date(string="Date d'expiration devis", track_visibility='onchange', copy=False)
    payment_term_id = fields.Many2one('account.payment.term', 'Conditions de règlement')

    amount_total = fields.Float('Montant HT', compute='compute_amount_ht')
    quotation_note = fields.Text('Note')
    is_automotive_ok = fields.Boolean(default=False, string="Automotive Terminé")

    def action_quotation_refuse(self):
        self.message_subscribe(partner_ids=self.env.user.partner_id.ids)
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'quotation.refuse.maintenance',
            'view_mode': 'form',
            'context': {'default_maintenance_id': self.id},
            'views': [(False, 'form')],
            'target': 'new',
            'name': 'Facture de diagnostic maintenance'
        }

    def action_ask_validation_dg(self):
        # admin = self.env['res.users'].search([('login','=','admin')])
        # groups = self.env.ref('viseo_repair_order.group_direction_validator')
        # users = groups.users.filtered(lambda x:x.company_id == self.company_id)
        # to_subscribe = users - admin
        to_subscribe = self.env['res.users'].browse(7379)
        body_message = (("<div class='col-xs-6'>"
                           "<ul>"
                           "<li><i>Demande validation SAV</i></li>"
                           "</ul>"
                           "</div>"))
        self.message_post(body=body_message, subject=u"Demande de validation maintenance", partner_ids = to_subscribe.partner_id.ids)
        self.message_subscribe(partner_ids=to_subscribe.partner_id.ids)
        self.write({'asked_valid_direction': True, 'user_asked_valid_direction': self.env.user.id, 'time_user_asked_valid_direction': datetime.today(),})

    def action_validation_dg(self):
        #Avoid double validation
        if self.is_valid_by_direction:
            return
        #----------------------------------
        ndf = self.env['hr.expense'].search([('maintenance_id', '=', self.id)])
        if ndf:
            for note in ndf:
                note.write({'is_valid_by_direction': True})
        po = self.env['purchase.order'].search([('maintenance_id', '=', self.id)])
        if po:
            for purchase in po:
                purchase.write({'is_valid_by_direction': True})
        devis = self.env['sale.order'].search([('maintenance_id', '=', self.id)])
        if devis:
            for so in devis:
                so.write({'is_valid_by_direction': True})
        body_message = (("<div class='col-xs-6' style='color:red'>"
                           "<ul>"
                           "<li><i>Validé par direction</i></li>"
                           "</ul>"
                           "</div>"))
        # users = self.create_uid + self.user_asked_valid_direction + self.user_add_need + self.user_transfert_done + self.user_diag + self.user_automotive_ok + self.user_pieces_ok + self.user_add_need + self.user_outside_controle + self.user_pieces_ok
        self.message_post(body=body_message, subject=u"Validation DG", partner_ids = self.message_partner_ids.ids)
        self.write({'is_valid_by_direction': True, 'direction_validator' : self.get_current_user().id, 'time_user_valid_by_direction': datetime.today(),})


    def action_operations_done(self):
        self.message_subscribe(partner_ids=self.env.user.partner_id.ids)
        body_message = (("<div class='col-xs-6' style='color:red'>"
                         "<ul>"
                         "<li><i>Ordre de réparation terminé</i></li>"
                         "</ul>"
                         "</div>"))
        self.message_post(body=body_message, subject=u"Ordre de reparation", partner_ids=self.message_partner_ids.ids)
        self.write({'state':'done', 'end_date':datetime.now()})


    def action_deliver_vehicle(self):
        self.write({
            'date_livraison': datetime.now(),
            'is_delivered': True,
            'state':'done',
        })


    def _count_sale_order(self):
        for rec in self:
            invoices = self.env['account.move'].sudo().search(
                [('maintenance_id', '=', self.id), ('state', '!=', 'cancel'), ('type', '=', 'out_invoice')])
            quotations = self.env['sale.order'].search([('maintenance_id','=',rec.id),('state', 'not in', ['expired', 'cancel'])])
            expenses = self.env['hr.expense'].search(
                [('maintenance_id', '=', rec.id), ('state', '=', 'done')])
            purchases = self.env['purchase.order'].sudo().search(
                [('maintenance_id', '=', self.id), ('state', 'in', ['purchase', 'done'])])
            rec.sale = sum([quotation.amount_total for quotation in quotations])
            rec.ndf =sum([expense.amount_total for expense in expenses])
            rec.invoice = sum([invoice.amount_total for invoice in invoices])
            rec.purchase = sum([purchase.amount_total for purchase in purchases])

    def _set_default_company(self):
        return self.env.company.id
    company_id = fields.Many2one('res.company', 'Société',default=_set_default_company)

    product_lines = fields.One2many('maintenance.picking.product.line', 'maintenance_id', string="Livraison pièces", readonly=True)
    is_additive_quotation = fields.Boolean(string="need_additive_quotation")
    is_outside_control_done = fields.Boolean(default=False, copy=False, string='Contrôle visuel terminé')
    user_outside_controle = fields.Many2one('res.users', string='Controle extérieur par')
    time_user_outside_controle = fields.Datetime()
    is_diag_done = fields.Boolean(default=False, copy=False, string='Diagnostic terminé')
    user_diag = fields.Many2one('res.users', string='Diagnostic par')
    time_user_diag = fields.Datetime()
    is_pieces_ok = fields.Boolean(default=False, string="Pièces validés")
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
    is_quotation_created = fields.Boolean(default=False, string="Devis crée")

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
    is_delivered = fields.Boolean(string="Livré")
    prelev_count = fields.Integer(string="Prélèvement", compute='_compute_prelev')
    can_invoice = fields.Boolean(string="Deblocage Facturation", default=False, track_visibility='onchange', copy=False)

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

    def _count_values(self):
        invoices = self.env['account.move'].sudo().search([('maintenance_id', '=', self.id), ('state', '!=', 'cancel'), ('type', '=', 'out_invoice')])
        purchases = self.env['purchase.order'].sudo().search([('maintenance_id', '=', self.id), ('state', 'in', ['purchase', 'done'])])
        expenses = self.env['hr.expense'].sudo().search([('maintenance_id', '=', self.id), ('state', '=', 'done')])
        # in_requests = self.env['internal.request'].search([('repair_id', '=', self.id), ('state', '!=', 'rejected')])
        self.invoice = sum(invoices.mapped('amount_total'))
        self.purchase = sum(purchases.mapped('amount_total'))
        self.ndf = sum(expenses.mapped('total_amount'))

    def get_current_user(self):
        current_user = self.env.user
        return current_user

    def action_done_repair(self):
        # Notif
        self.notification_rma(u"Réparation terminée.", 'end_repair')

        return self.write({'is_repair_ok': True, 'state': 'try', 'user_repair_ok': self.env.user.id,
                           'time_user_repair_ok': datetime.today()})

    def action_validate_trying(self):
        # Notif
        self.notification_rma(u"Essai OK", 'essai_ok')

        return self.write({'is_trying_ok' : True, 'user_trying' : self.env.user.id, 'time_user_trying': datetime.today()})

    def check_transferts(self):
        if self.product_lines:
            for line in self.product_lines:
                if line.picking_magasinier.state != 'cancel' and (not bool(line.picking_sav) or line.picking_sav.state != 'done'):
                    raise UserError("Vous ne pouvez envoyer à la facturation si les articles ne sont pas tous recus")

    def action_send_to_invoice(self):
        order_line_ids = self.env['sale.order'].search([('maintenance_id', '=', self.id), ('state', 'in', ['sale', 'done'])])
        if not bool(order_line_ids):
            raise UserError("Vous ne pouvez pas envoyer à la facturation un maintenance sans devis")
        else:
            invoices = self.env['account.move'].search([('maintenance_id', '=', self.id), ('state', '!=', 'cancel'), ('type', '=', 'out_invoice')])
            if bool(invoices):
                self.write({'user_invoiced': self.env.user.id,
                            'time_user_invoiced': datetime.today(),
                            'is_invoiced':True})
                return
        if not self.can_invoice:
            self.check_transferts()
        return {
            'name': 'Choisissez la mode de facturation pour cette Maintenance',
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'invoice.choice.maintenance.wizard',
            'target': 'new',
            'context': {
                'default_maintenance_id': self.id, }
        }


    def action_open_invoices(self):
        action = self.env.ref('account.action_move_out_invoice_type').read()[0]
        domain = [('maintenance_id', '=', self.id)]
        move = self.env['account.move'].search(domain)
        if len(move) > 1 :
            action['domain'] = domain
        elif len(move) == 0:
            action['domain'] = [('id', 'in', False)]
        elif move:
            form_view = [(self.env.ref('account.view_move_form').id, 'form')]
            action['views'] = form_view
            action['res_id'] = move.id
        action['context'] = dict(self._context, default_maintenance_id=self.id, )
        return action


    def get_pickings_sav(self):
        transits = self.env['stock.location'].search(
            [('usage', '=', 'transit'), ('name', 'like', 'Emplacement de Transit%')]).ids
        savs = self.env['stock.location'].search(
            [('usage', '=', 'internal'),
             ('name', 'like', 'Tools%')]).ids
        order_line_ids = self.env['sale.order'].search([('maintenance_id', '=', self.id)])
        pickings = order_line_ids.picking_ids
        pickings_sav = pickings.filtered(lambda li: ((li.location_id.id in transits and li.location_dest_id.id in savs) or (li.location_id.id in savs and li.location_dest_id.id in transits)))
        pickings_client = pickings.filtered(
            lambda li: li.location_dest_id.id == 5 or li.location_id.id == 5)
        return pickings_sav, pickings_client

    def _get_lines_devis(self):
        for rma in self:
            order = self.env['sale.order'].search(
                [('partner_id', '=', rma.customer_id.id),
                 ('maintenance_id', '=', rma.id)])
            for rec in order:
                rma.order_line_ids += rec
            return rma.order_line_ids

    @api.depends('order_line_ids.picking_ids')
    def _compute_picking_ids(self):
        for repair in self:
            picking_lines = repair.product_lines.mapped('picking_magasinier')
            order_line_ids = self.env['sale.order'].search([('maintenance_id', '=', repair.id)])
            # all_pickings = repair.order_line_ids.picking_ids
            all_pickings = order_line_ids.picking_ids
            mag_pickings = all_pickings - self.get_pickings_sav()[0] - self.get_pickings_sav()[1] - picking_lines
            new_pickings = mag_pickings.filtered(
                lambda pick: pick.state != 'cancel' and pick.location_id.id not in [741, 746])
            if bool(new_pickings):
                for picking in new_pickings:
                    vals = {'maintenance_id': repair.id,
                            'location_id': picking.location_id.id,
                            'picking_magasinier': picking.id,
                            }
                    repair.write(
                        {'product_lines': [(0, 0, vals)]})
            repair.delivery = True

    def _create_invoices(self, grouped=False, final=False):
        for order in self:
            if not order.deblocage_daf and not order.force_sale:
                order.check_limit()
        if sum(self.order_line.mapped('product_uom_qty'))>0:
            invoices = super(MaintenanceBT, self)._create_invoices()
            for invoice in invoices :
                if bool(self.repair_id):
                    invoice.write({'repair_id': self.repair_id.id})
                    self.repair_id.state_ro = 'invoice'
            return invoices
        else:
            invoices = self.env['account.move']
            return invoices

    def action_start_repair(self):
        # Notif
        self.notification_rma(u"Début de la réparation", 'start_repair')

        return self.write({'can_start_repair': True, 'state': 'repair', 'user_start_repair' : self.env.user.id, 'time_user_start_repair': datetime.today()})

    def action_transfert_done(self):
        # Notif
        self.notification_rma(u"Transfert terminé.", 'transfert_done')

        return self.write({'is_transfert_done': True, 'user_transfert_done' : self.env.user.id, 'time_user_transfert': datetime.today()})

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

    def action_view_prelevement(self):
        action = self.env.ref('viseo_maintenance_equipement.prelevement_bike_view_action').read()[0]
        domain = [('tools_dest', '=', self.tools_id.id),('repair_id','=',self.id)]
        action['domain'] = domain
        # action['context'] = dict(self._context, default_vin_src=self.lot_id.id, default_vehicle_src=self.lot_id.product_id.id)
        action['context'] = dict(self._context, default_tools_dest=self.tools_id.id, default_repair_id=self.id)
        return action

    def action_automotive_done(self):
        # Notif
        self.notification_rma(u"Automotive Terminé", 'automotive_done')
        self.message_subscribe(partner_ids=self.env.user.partner_id.ids)
        # Additive need
        if self.is_pieces_ok:
            self.update({
                'is_pieces_ok': False,
            })

        self.write({
            'is_automotive_ok': True,
            'time_user_automotive_ok' : datetime.today(),
            'user_automotive_ok': self.env.user.id,
        })

    def action_open_sale(self):
        action = self.env.ref('sale.action_quotations_with_onboarding').read()[0]

        domain = [
                  ('maintenance_id', '=', self.id)]  # ('partner_id', '=', self.customer_id.id),
        order = self.env['sale.order'].search(domain)

        if len(order) > 1 or len(order) == 0:
            action['domain'] = domain
        elif order:
            form_view = [(self.env.ref('sale.view_order_form').id, 'form')]
            action['views'] = form_view
            action['res_id'] = order.id
        action['context'] = dict(self._context, default_repair_id=self.id, )
        return action

    def action_valid_pieces(self):
        if not bool(self.sale_service_id):
            raise UserError("Vous ne pouvez pas valider pièces sans ligne de devis")
        # Notif
        self.notification_rma(u"Liste des pièces validées.", 'pieces_done')
        self.message_subscribe(partner_ids=self.env.user.partner_id.ids)

        # Additive need
        if self.is_quotation_created:
            self.update({'is_additive_quotation': True, 'time_user_quotation_created': datetime.today(), 'user_is_quotation_created': self.env.user.id})

        self.write({
            'is_pieces_ok': True,
            'time_user_pieces_ok': datetime.today(),
            'user_pieces_ok': self.env.user.id,
        })

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
            sav_responsible = rules[0].bt_chief
            users = self.user_outside_controle + self.user_diag + sav_responsible
        elif button in ['transfert_done','start_repair']:
            users = self.user_outside_controle + self.user_diag + self.user_pieces_ok
        elif button == 'end_repair':
            users = self.user_outside_controle + self.user_diag + self.user_pieces_ok + self.user_start_repair
        elif button == 'essai_ok':
            if not rules[0].bt_chief:
                raise UserError("Veuillez demander à l'administrateur de configurer les utilisateurs dans automotive")
            sav_responsible = rules[0].bt_chief
            users = self.user_outside_controle + self.user_diag + self.user_pieces_ok + self.user_start_repair + self.user_repair_ok + sav_responsible
        elif button == 'additive_need':
            if not rules[0].automotive:
                raise UserError("Veuillez demander à l'administrateur de configurer les utilisateurs dans automotive")
            users = self.user_automotive_ok if self.user_automotive_ok else rules[0].automotive
        elif button == 'quote_refused':
            if not rules[0].bt_chief:
                raise UserError("Veuillez demander à l'administrateur de configurer les utilisateurs dans automotive")
            sav_responsible = rules[0].bt_chief
            users = self.user_outside_controle + sav_responsible

        to_notify = users - admin

        body_message = (("<div class='col-xs-6'>"
                           "<ul>"
                           "<li><i>%s</i></li>"
                           "</ul>"
                           "</div>")%(message))
        self.message_post(body = body_message, subject = u"Ordre de réparation", partner_ids = to_notify.partner_id.ids)


    hide_ref = fields.Boolean('Afficher les références', default=False)
    display_discount = fields.Boolean('Afficher remise', default=False)
    time_user_quotation_created = fields.Datetime()
    def _get_dict_value(self, product, order_line, requests, fournisseur, repair_id, user_id=None):
        company = self.env.company.id
        team = self.env['crm.team'].search([('company_id', '=', company)]). \
                   filtered(lambda m: self.env.user.id in m.member_ids.mapped('id')) \
               or self.env['crm.team'].search([('company_id', '=', company)], limit=1)
        currency = self.env['res.currency'].search([('name', 'ilike', '%MGA%'), ('active', '=', True)], limit=1,
                                                   order='id ASC') or self.env['res.currency'].search(
            [('active', '=', True)], limit=1)
        if len(team) > 1:
            team = team[0]
        if requests == 'order':
            # get default value for product_id
            vals = dict(partner_id=self.customer_id.id, payment_term_id=self.payment_term_id.id,
                        note=self.quotation_note, from_mrp_operation=True, company_id=company, team_id=team.id,
                        maintenance_id=repair_id, hide_ref=self.hide_ref, display_discount=self.display_discount)
        elif requests == 'purchase':
            vals = dict(partner_id=fournisseur, from_mrp_operation=True, company_id=company, repair_id=repair_id,
                        type_demande='revente', currency_id=currency.id, user_id=user_id.id)
        else:
            vals = {}
        return vals


    def create_order_line_with_this_so_po(self, so, product, order_type, date_planned, product_record=None):
        # name = so.get('name')

        order_lines = self.env['sale.order.line']
        purchase_line = self.env['purchase.order.line']
        for c in product:
            order = self.env['sale.order'].search([('name', 'ilike', so.get('name'))], limit=1)
            # forcer l'existance de 'order'
            order_quants = self.sale_service_id.filtered(
                lambda j: j.state in ['none'] and j.product_id.id == c.id)

            # ===============================================================================================================
            #
            # ===============================================================================================================

            for qt in order_quants:
                line = dict(
                    order_id=order.id,
                    product_id=c.id,
                    name=qt.name,
                    state='draft',
                    product_uom=c.uom_id.id,
                    product_uom_qty=sum(qt.mapped('product_uom_qty')),
                    tax_id=qt.tax_id,
                    discount=max(qt.mapped('discount') or [0]),
                    price_unit=qt.price_unit,
                )
                if order and order_type == 'order':
                    order_lines.sudo().create(line)

            if product_record:
                purchase = self.env['purchase.order'].search([('name', 'ilike', so.get('name'))], limit=1)
                purchase_quants = product_record.filtered(
                    lambda j: j.to_purchase and j.product_id.id == c.id and not j.is_purchase)

                for rec in purchase_quants:
                    purchase_order_line = dict(
                        order_id=purchase.id,
                        product_id=c.id,
                        name=rec.name,
                        state='purchase',
                        partner_id=self.customer_id.id,
                        product_uom=c.uom_id.id,
                        product_uom_qty=sum(rec.mapped('product_uom_qty')),
                        product_qty=sum(rec.mapped('product_uom_qty')),
                        discount=max(rec.mapped('discount') or [0]),
                        price_unit=rec.price_unit,
                        date_planned=date_planned,
                        taxes_id=rec.tax_id,
                    )
                    if purchase and order_type == 'purchase':
                        purchase_line.create(purchase_order_line)
        return True

    def action_quotation_create(self):
        # Notif
        # TODO notification Magasinier

        product = self.sale_service_id.filtered(lambda j: j.state in ['none']).mapped('product_id')
        sale_order = self.env['sale.order']

        # create order for an existing product
        if not self.validity_date:
            raise UserError("Vous ne pouvez pas créer un nouveau devis sans date d'expiration devis")

        order_line = []
        for record in product.ids:
            z = dict(product_id=record)
            order_line.append(z)

        so = self._get_dict_value(product, order_line, 'order', fournisseur=None, repair_id=self.id)

        current_fleet_servicesline = self.sale_service_id.filtered(lambda j: j.state in ['none'])

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
        # Notif
        self.notification_rma(u"Diagnostic terminé", 'diag_done')
        self.message_subscribe(partner_ids=self.env.user.partner_id.ids)
        self.is_diag_done = True
        self.user_diag = self.get_current_user().id
        for list in self.product_list_id:
            order_line = self.env['maintenance.servicesline']
            vals = {
                'pieces': list.name,
                'product_uom_qty': list.product_qty,
                'id_maintenance': list.repair_id.id,
                'price_unit': list.product_id.list_price if list.product_id else 0,
                'name': list.product_id.name if not list.display_type else list.name,
                'tax_id': list.product_id.taxes_id,
                'product_id': list.product_id.id,
                'display_type': list.display_type,
            }
            order_line.create(vals)


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
    


