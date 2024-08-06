from odoo import fields, models, api
from odoo.exceptions import UserError
from datetime import datetime,timedelta
class ViseoCrm(models.Model):
    _name = 'viseo.crm'
    _description = 'model pour le module CRM'

    name = fields.Char(required=True)
    vendeur = fields.Many2one(
        'res.users',  # The related model
        string="Vendeur",
        default=lambda self: self.env.user, required=True  # Use self.env.user to get the current user's ID
    )
    begin_date = fields.Date(required=True)
    date_end = fields.Date(required=True)

    state = fields.Selection([
        ('proposition', 'Proposition'),
        ('accounting', 'Comptabilisé'),
        ('done', 'Fini')
    ])
    partner_ids = fields.Many2many('res.users', string="Sous Lead")
    client_line_ids = fields.One2many('crm.client.line','crm_id', string="Client Lines")

    order_line_ids = fields.One2many('crm.order.line','parent_id')

    prosprects_line = fields.One2many('prospect.crm','crm_id')

    crm_lead = fields.Many2one('crm.lead', string="liste des prix")
    currency_id = fields.Many2one('res.currency', string="Devise", required=True)
    company_id = fields.Many2one('res.company', string="Société", default=lambda self: self._default_company(), required=True)
    canal = fields.Selection([('telephone','Appel Téléphonique'),('social_media','Réseaux Sociaux'),('email','Mail'),('other','Autres')], string="Canal", required=True)

    client_sleeping = fields.Integer(string="Clients Dormants", compute='_compute_client_sleeping')
    @api.depends('order_line_ids.product_id')
    def _compute_client_sleeping(self):
        for rec in self:
            date_actuelle = datetime.now()
            date_six_mois_avant = date_actuelle - timedelta(days=180)
            product_ids = rec.order_line_ids.mapped('product_id.id')

            dormant_clients = self.env['res.partner']
            for client in self.env['res.partner'].search([]):
                recent_orders = self.env['sale.order'].search_count([
                    ('partner_id', '=', client.id),
                    ('date_order', '>', date_six_mois_avant),
                    ('state', '=', 'sale'),
                    ('order_line.product_id', 'in', product_ids)
                ])
                if not recent_orders:
                    dormant_clients |= client

            rec.client_sleeping = len(dormant_clients)


    def action_view_client_sleeping(self):
        self.ensure_one()
        date_actuelle = datetime.now()
        date_six_mois_avant = date_actuelle - timedelta(days=180)
        product_ids = self.order_lines_ids.mapped('product_id.id')

        dormant_clients = self.env['res.partner']
        for client in self.env['res.partner'].search([]):
            recent_orders = self.env['sale.order'].search_count([
                ('partner_id', '=', client.id),
                ('date_order', '>', date_six_mois_avant),
                ('state', '=', 'sale'),
                ('order_line.product_id', 'in', product_ids)
            ])
            if not recent_orders:
                dormant_clients |= client

        action = {
            'type': 'ir.actions.act_window',
            'name': 'Clients Dormants',
            'res_model': 'res.partner',
            'view_mode': 'tree,form',
            'target': 'current',
            'domain': [('id', 'in', dormant_clients.ids)],
        }

        return action
    @api.model
    def action_open_social_media_form(self):
        action = self.env.ref('viseo_crm_plus.action_social_media_type').read()[0]
        action['context'] = {
            'default_prospect_line_id': self.id
        }
        return action

    @api.constrains('canal')
    def onchange_canal(self):
        pass
        # print('Tafiditra ato ve')
        # # if self.canal == 'social_media':
        # #     print('$'*50)
        # #     return {
        # #         'type': 'ir.actions.act_window',
        # #         'res_model': 'social.media.model',
        # #         'view_mode': 'form',
        # #         'view_type':'form',
        # #         'view_id': self.env.ref('viseo_crm_plus.view_social_media_type_form').id,
        # #         'context': {
        # #             #'default_crm_id': self.crm_id.id,
        # #            'default_prospect_id': self.id
        # #         },
        # #         'target': 'new',
        # #     }
        #
        #
        # elif self.canal == 'telephone':
        #     return {
        #         'type': 'ir.actions.act_window',
        #         'res_model': 'prospect.telephone.model',
        #         'view_mode': 'form',
        #         'context': {
        #            # 'default_crm_id': self.crm_id.id,
        #             'default_prospect_id': self.id
        #         },
        #         'target': 'new',
        #     }
        # elif self.canal == 'email':
        #     return {
        #         'type': 'ir.actions.act_window',
        #         'res_model': 'prospect.email.model',
        #         'view_mode': 'form',
        #         'context': {
        #             #'default_crm_id': self.crm_id.id,
        #             'default_prospect_id': self.id
        #         },
        #         'target': 'new',
        #     }
        # else:
        #     return {
        #         'type': 'ir.actions.act_window',
        #         'res_model': 'prospect.other.model',
        #         'view_mode': 'form',
        #         'context': {
        #            # 'default_crm_id': self.crm_id.id,
        #             'default_prospect_id': self.id
        #         },
        #         'target': 'new',
        #     }



    @api.model
    def _default_company(self):
        company = self.env['res.company'].search([('name', '=', 'ocean trade')], limit=1)
        return company.id if company else False
    def add_new_lines(self, vals_list):
        vals_list = self.env['prospect.crm']
        """
        Add new lines to the one2many field.
    
        :param vals_list: List of dictionaries containing the values for the new lines.
        """
        for record in self:
            record.write({
                'client_line_ids': [(0, 0, vals) for vals in vals_list]
            })
    def create_customer(self):
        pass

class CrmClientLine(models.Model):
    _name = 'crm.client.line'

    partner_ids = fields.Many2one('res.partner', string="Partenaire")
    country_id = fields.Many2one('res.country', string="Pays", related="partner_ids.country_id", store=True)
    phone = fields.Char(string="Téléphone", related="partner_ids.phone", store=True)
    email = fields.Char(string="Email", related="partner_ids.email", store=True)
    mobile = fields.Char(string="Mobile", related="partner_ids.mobile", store=True)
    company_type = fields.Selection([('person','Particulier'),('company','Société')], related="partner_ids.company_type", store=True)
    crm_id = fields.Many2one('viseo.crm')
    pricelist_generated = fields.Boolean(string="Pricelist Generated", default=False)

    def generate_pricelist(self):
        for rec in self:
            crm = rec.crm_id
            orders = crm.order_line_ids

            item_ids = []
            for line in orders:
                if line:
                    vals = {'product_tmpl_id': line.product_id.product_tmpl_id.id,
                            'product_id': line.product_id.id,
                            'applied_on': '1_product',
                            'min_quantity': line.qty_min,
                            'date_start': crm.begin_date or False,
                            'date_end': crm.date_end or False,
                            'compute_price': 'percentage',
                            'percent_price': line.discount}
                    item_ids.append((0, 0, vals))
                raise UserError("Aucun article dans le champs articles!")

            # Recherche de la liste de prix existante
            crm_lead = self.env['product.pricelist'].search([
                ('name', '=', crm.name),
                ('company_id', '=', crm.company_id.id),
                ('currency_id', '=', crm.currency_id.id)

                #('item_ids[1].pricelist_id.date_start', '=', crm.begin_date),
                #('date_end', '=', crm.date_end)
            ], limit=1)

            if not crm_lead:
                # Création de la nouvelle liste de prix
                price_list = self.env['product.pricelist'].create({
                    'name': crm.name,
                    'company_id': crm.company_id.id,
                    'discount_policy': 'without_discount',
                    'currency_id': crm.currency_id.id,
                    'discount_policy':'with_discount',
                    'item_ids': item_ids,
                    #'date_start': crm.begin_date,
                    #'date_end': crm.date_end
                })
            else:
                price_list = crm_lead

            # Création de la commande de vente
            devis = self.env['sale.order'].create({
                'partner_id': rec.partner_ids.id,
                'validity_date': crm.date_end,
                'pricelist_id': price_list.id,
                'order_line': [(0,0, {
                    'product_id': line.product_id.id,
                    #'discount': price_list.item_ids.percent_price or False,
                }) for line in orders]
                #'order_line':[
            })
            rec.pricelist_generated = True

            if (crm.order_line_ids.product_qty < crm.order_line_ids.qty_min) or (crm.order_line_ids.product_qty > crm.order_line_ids.qty_max) :

                return {
                    'type': 'ir.actions.act_window',
                    'name': 'Devis',
                    'view_mode': 'form',
                    'res_model': 'sale.order',
                    'res_id': devis.id,
                    'target': 'current',
                }
            else:
                raise  UserError(f"La demande  dépasse la quantité disponible")
class SaleOrderline(models.Model):
    _name = 'crm.order.line'

    parent_id = fields.Many2one('viseo.crm')
    product_id = fields.Many2one('product.product', required=True)
    product_qty = fields.Float("Qté(s) Disponible(s)",related="product_id.qty_available_not_res",  store=True)
    qty_min = fields.Float("Qté min", default=1.0)
    qty_max = fields.Float("Qté max")
    description = fields.Char("Description", related="product_id.name", store=True)
    price_ht = fields.Float("Prix public", related='product_id.list_price', store=True)
    qty_dispo = fields.Float("Qté dispo", compute='get_qty_dispo')
    # price_apply_ht = fields.Float("Prix remisé HT", compute='compute_price_ht')
    # price_apply_tva = fields.Float("Prix appliqué TVA")
    product_uom_id = fields.Many2one('uom.uom', related='product_id.uom_id', string="Unité(s)", track_visibility='onchange')
    # brand_id = fields.Many2one('viseo.brand', related='product_id.product_tmpl_id.brand_id', string="Marque",)
    discount = fields.Float()
    price = fields.Float("Prix spécial")



    @api.depends('product_id')
    def get_qty_dispo(self):
        for line in self:
            quants = self.env['stock.quant'].search(
                [('product_id', '=', line.product_id.id),
                 ('location_id.usage', 'in', ['internal'])])
            qty_dispo = sum(quants.mapped('quantity'))
            qty_reserved = sum(quants.mapped('reserved_quantity'))
            line.qty_dispo = qty_dispo - qty_reserved
                # move.mrp_dispo = qty_dispo

    @api.onchange('discount')
    def onchange_discount(self):
        if self.discount > 0:
            self.price = self.price_ht - (self.price_ht * (self.discount/100))

    @api.depends('price_ht')
    def compute_price_ht(self):
        for line in self:
            line.price_apply_ht = line.price_ht
    @api.depends('price')
    def onchange_price(self):
        if self.price > 0:
            self.discount = (self.price_ht - self_price)*(100/self.price_ht)

''' @api.onchange('partner_ids')
    def _default_country_id(self):
        # Get the default country based on the partner if available
        actual_partner = self.partner_ids.id
        partner = self.env['res.partner'].browse(actual_partner)
        return partner.country_id.id if partner else None'''




class ClientLine(models.Model):
    _inherit = 'res.partner'

    crm_id = fields.Many2one('viseo.crm')
    customers_ids = fields.Many2one('res.partner')

class prospectLine(models.Model):
    _name = 'prospect.crm'

    name = fields.Char(string="nom", required=True)
    adress = fields.Char(string="Adresse")
    company_type = fields.Selection([('person','Particulier'),('company','Société')], required=True)
    country = fields.Many2one('res.country',string="Pays", required=True)
    number = fields.Char(string="Mobile")
    telephone = fields.Char(string="Téléphone")
    email = fields.Char(string="Email")
    is_invisible = fields.Boolean(default=False)

    crm_id = fields.Many2one('viseo.crm')
    canal = fields.Selection([('telephone','Appel Téléphonique'),('social_media','Réseaux Sociaux'),('email','Mail'),('other','Autres')], string="Canal", required=True)
    state = fields.Selection([('open','Ouvert'),('win','Gagné'),('lost','Perdus')], string="Etats")

    def create_devis(self):
        for rec in self:
            crm = rec.crm_id
            orders = crm.order_line_ids

            item_ids = []

            for line in orders:
                if line:
                    vals = {'product_tmpl_id': line.product_id.product_tmpl_id.id,
                            'product_id': line.product_id.id,
                            'applied_on': '1_product',
                            'min_quantity': line.qty_min,
                            'date_start': crm.begin_date or False,
                            'date_end': crm.date_end or False,
                            'compute_price': 'percentage',
                            'percent_price': line.discount}
                    item_ids.append((0, 0, vals))
                raise UserError("Aucun article dans le champs articles!")

            # Recherche de la liste de prix existante
            crm_lead = self.env['product.pricelist'].search([
                ('name', '=', crm.name),
                ('company_id', '=', crm.company_id.id),
                ('currency_id', '=', crm.currency_id.id)

                # ('item_ids[1].pricelist_id.date_start', '=', crm.begin_date),
                # ('date_end', '=', crm.date_end)
            ], limit=1)

            if not crm_lead:
                # Création de la nouvelle liste de prix
                price_list = self.env['product.pricelist'].create({
                    'name': crm.name,
                    'company_id': crm.company_id.id,
                    'discount_policy': 'without_discount',
                    'currency_id': crm.currency_id.id,
                    'discount_policy': 'with_discount',
                    'item_ids': item_ids,
                    # 'date_start': crm.begin_date,
                    # 'date_end': crm.date_end
                })
            else:
                price_list = crm_lead
            partner_id = self.env['res.partner'].search([('name', '=', 'PROPOSITION COMMERCIALE')], limit=1)
            # Création de la commande de vente
            devis = self.env['sale.order'].create({
                'partner_id': partner_id.id,
                'validity_date': crm.date_end,
                'pricelist_id': price_list.id,
                'order_line': [(0, 0, {
                    'product_id': line.product_id.id,
                    # 'discount': price_list.item_ids.percent_price or False,
                }) for line in orders]
                # 'order_line':[
            })
            rec.pricelist_generated = True

            if (crm.order_line_ids.product_qty < crm.order_line_ids.qty_min) or (
                    crm.order_line_ids.product_qty > crm.order_line_ids.qty_max):

                return {
                    'type': 'ir.actions.act_window',
                    'name': 'Devis',
                    'view_mode': 'form',
                    'res_model': 'sale.order',
                    'res_id': devis.id,
                    'target': 'current',
                }
            else:
                raise UserError(f"La demande  dépasse la quantité disponible")
    # @api.onchange('canal')
    # def onchange_canal(self):
    #     if self.canal == 'social_media':
    #         return {
    #             'type': 'ir.actions.act_window',
    #             'res_model': 'social.media.model',
    #             'view_mode': 'form',
    #             'context': {
    #                 'default_crm_id': self.crm_id.id,
    #                 'default_prospect_id': self.id
    #             },
    #             'target': 'new',
    #         }
    #
    #     elif self.canal == 'telephone':
    #         return {
    #             'type': 'ir.actions.act_window',
    #             'res_model': 'prospect.telephone.model',
    #             'view_mode': 'form',
    #             'context': {
    #                 'default_crm_id': self.crm_id.id,
    #                 'default_prospect_id': self.id
    #             },
    #             'target': 'new',
    #         }
    #     elif self.canal == 'email':
    #         return {
    #             'type': 'ir.actions.act_window',
    #             'res_model': 'prospect.email.model',
    #             'view_mode': 'form',
    #             'context': {
    #                 'default_crm_id': self.crm_id.id,
    #                 'default_prospect_id': self.id
    #             },
    #             'target': 'new',
    #         }
    #     else:
    #         return {
    #             'type': 'ir.actions.act_window',
    #             'res_model': 'prospect.other.model',
    #             'view_mode': 'form',
    #             'context': {
    #                 'default_crm_id': self.crm_id.id,
    #                 'default_prospect_id': self.id
    #             },
    #             'target': 'new',
    #         }

    def create_customer(self):
        for rec in self:
            crm = self.env['prospect.crm'].browse(rec.id)  # Assuming 'self' is a crm.lead recordset
            if crm:
                crm.is_invisible = True
                client = self.env['res.partner'].create({
                    'name': crm.name,
                    'company_type': crm.company_type,
                    'country_id': crm.country.id,  # Assuming 'country' is a many2one field
                    'phone': crm.telephone,  # Corrected 'telehone' to 'telephone'
                    'mobile': crm.number,
                    'email': crm.email
                })
                client = self.env['crm.client.line'].search
                return client

    def put_into_client(self):
        self.create_customer()
        for rec in self:

            client = self.env['res.partner'].search([
                ('name', '=', rec.name),
                ('country_id', '=', rec.country.id),
                ('company_type', '=', rec.company_type)
            ], limit=1)

            if client:
                crm = rec.crm_id.id
                client_crm = self.env['viseo.crm'].browse(crm)

                if client_crm:
                    # Ajout d'une nouvelle ligne dans le champ one2many
                    client_crm.write({
                        'client_line_ids': [(0, 0, {
                            'partner_ids': client.id,
                            # Ajoutez ici les autres champs nécessaires
                        })]
                    })
            line = self.env['prospect.crm'].browse(rec.id)
            if line:
                line.unlink()

def create_invoice(self):
        pass