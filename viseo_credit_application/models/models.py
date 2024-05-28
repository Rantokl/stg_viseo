
from odoo import models, fields, api, exceptions
from odoo.exceptions import ValidationError

from odoo import models, fields, api

class WizardCreditApplication(models.TransientModel):
    _name = 'credit_application.wizard'

    partner_id = fields.Many2one('res.partner')
    plafond_credit_wizard = fields.Float(string='Plafond de crédit', required=True)
    blocage_type_wizard = fields.Selection([
        ('none', 'Aucun'),
        ('blocked', 'Bloque'),
        ('amount_limited', 'Montant'),
        ('date', u'Echéance'),
        ('all', 'Tous')],
        string='Type de blocage', required=True, copy=False, default='none', track_visibility=True
    )
    payment_condition_wizard = fields.Many2one('account.payment.term', string='condition de payement')
    company_wizard = fields.Many2one('res.company', string='Société')
    def send_application_credit_from_wizard(self):
        self.ensure_one()
        self.requester_wizard = self.env.user.id

        # ===========================MISE A JOUR DES CHAMPS DANS L'ONGLET DEMANDE DE CREDIT===============================
        self.partner_id.sudo().update({
            'plafond_credit': self.plafond_credit_wizard,
            'blocage_type': self.blocage_type_wizard,
            'payment_condition': self.payment_condition_wizard.id,
            'company':self.company_wizard.id
        })
        # ================================================================================================================
        self.partner_id.request_credit_application()
        
class ViseoCreditApplication(models.Model):
    _inherit = 'res.partner'

    plafond_credit = fields.Float(string='plafond de crédit', required=True)
    blocage_type = fields.Selection([
        ('none', 'Aucun'),
        ('blocked', 'Bloque'),
        ('amount_limited', 'Montant'),
        ('date', u'Echéance'),
        ('all', 'Tous')],
        string='Type de Blocage', required=True, copy=False, default='none', track_visibility=True
    )
    payment_condition = fields.Many2one('account.payment.term', string='durée de payement')
    company= fields.Many2one('res.company', string='Société')
    state_application_credit = fields.Selection([
        ('draft', 'Brouillon'),
        ('request', 'Demande en cours'),
        ('done', 'Validé'),
        ('rejected', 'Refusé')],
        default='draft', string='Etat'
    )
    visibility_button_chief = fields.Boolean(string='Visibilité des boutons des chefs', compute='check_chief')
    visibility_button_commercial = fields.Boolean(string='Visibilité des boutons des commerciaux', default=False)
    requester = fields.Many2one('res.users', string='Demandeur')
    confirm_chief=fields.Boolean(string='Les chefs Confirm??', default=False)

    def check_chief(self):
        if self.confirm_chief == False:    
            if self.state_application_credit =='request':
                user_id = self.env.user.id
                model_id = self.env['ir.model'].search([('model', '=', 'sale.order')]).ids
                rules = self.env['rule.rule'].with_context(active_test=False).search([('model_id', 'in', model_id)])
                rule_of_user=[]
                same_rule_and_user_is_chief= False
                requester_in_rule=False
                for rule in rules:          
                    for x in rule.sale_validation_ids:
                        if self.requester.id == x.name.id:
                            requester_in_rule=True
                            is_chief=self.env['sale.validation'].search([('rule_id','=',x.rule_id.id),('is_to_chief','=',True),('amount_limit','>=',self.plafond_credit)])
                            if is_chief :
                                for chef in is_chief:
                                    if user_id == chef.name.id:
                                        self.visibility_button_chief=True
                                        return True
                                    else:
                                        self.visibility_button_chief=False
                            elif x.rule_id.parent_id.id:
                                is_chief_parent=self.env['sale.validation'].search([('rule_id','=',x.rule_id.parent_id.id),('is_to_chief','=',True),('amount_limit','>=',self.plafond_credit)])
                                if is_chief_parent:
                                    for chef_parent in is_chief_parent:
                                        if user_id == chef_parent.name.id:
                                            self.visibility_button_chief=True
                                            return True
                                        else:
                                            self.visibility_button_chief=False
                                else :
                                    is_mh=self.env['sale.validation'].search([('rule_id','=',x.rule_id.parent_id.id),('is_to_mh','=',True)])
                                    if is_mh:
                                        for mh in is_mh:
                                            if user_id == mh.name.id:
                                                self.visibility_button_chief=True
                                                return True
                                            else:
                                                self.visibility_button_chief=False
                                    else:
                                        self.visibility_button_chief=False
                                
                            elif x.rule_id.parent_id.parent_id.id:
                                is_chief_parent_parent=self.env['sale.validation'].search([('rule_id','=',x.rule_id.parent_id.parent_id.id),('is_to_chief','=',True),('amount_limit','>=',self.plafond_credit)])
                                if is_chief_parent_parent:
                                    for chef_parent_parent in is_chief_parent_parent:
                                        if user_id == chef_parent_parent.name.id:
                                            self.visibility_button_chief=True
                                            return True
                                        else:
                                            self.visibility_button_chief=False
                                else :
                                    is_mh=self.env['sale.validation'].search([('rule_id','=',x.rule_id.parent_id.parent_id.id),('is_to_mh','=',True)])
                                    if is_mh:
                                        for mh in is_mh:
                                            if user_id == mh.name.id:
                                                self.visibility_button_chief=True
                                                return True
                                            else:
                                                self.visibility_button_chief=False
                                    else :
                                        self.visibility_button_chief=False
                            else:
                                is_mh=self.env['sale.validation'].search([('rule_id','=',x.rule_id.id),('is_to_mh','=',True)])
                                if is_mh:
                                    for mh in is_mh:
                                        if user_id == mh.name.id:
                                            self.visibility_button_chief=True
                                            return True
                                        else:
                                            self.visibility_button_chief=False
                                else :
                                    self.visibility_button_chief=False
                        else:
                            self.visibility_button_chief=False
            else:
                self.visibility_button_chief=False
        else:
            self.visibility_button_chief=False

    def commercial_confirm_boutton(self):
        self.message_post(body=f"La Demandé de credit pour {self.name} de montant {self.plafond_credit} est VALIDE par {self.env.user.name} ")
        self.state_application_credit='done'
        self.visibility_button_commercial = False
        self.confirm_chief=True
        self.credit_limit = self.plafond_credit
        self.warning_type = self.blocage_type
        self.property_payment_term_id = self.payment_condition.id

        # Recherche d'enregistrements dans ir.property
        self.env.cr.execute("""SELECT * FROM ir_property WHERE 
                                res_id = %s AND name = 'property_payment_term_id' AND company_id = %s""", 
                                (f'res.partner,{self.id}', self.company.id))

        is_property = self.env.cr.fetchall()
        print('=====================================================================================================================')
        print(is_property)
       
        if is_property:
            self.env.cr.execute(""" UPDATE ir_property SET value_reference = %s WHERE 
                                    res_id = %s AND name = 'property_payment_term_id' AND 
                                    company_id = %s""", 
                                    (f'account.payment.term,{self.property_payment_term_id.id}', f'res.partner,{self.id}', self.company.id))
            print(self.company.id)

            self.env.cr.execute("""SELECT * FROM ir_property WHERE 
                                res_id = %s AND value_reference = %s AND name = 'property_payment_term_id' AND company_id = %s""", 
                                (f'res.partner,{self.id}',f'account.payment.term,{self.property_payment_term_id.id}', self.company.id))

            up = self.env.cr.fetchall()
            print('=====================================================================================================================')
            print(up)
            print('§§§§§§§§§§§§§§§§§§§§§§§§§§§§UPDATED§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§')

        else:

            self.env.cr.execute("""SELECT id FROM ir_model_fields WHERE model = 'res.partner' AND name = 'property_payment_term_id'""")
            payment_term_field_id = self.env.cr.fetchone()

            self.env.cr.execute("""
                INSERT INTO ir_property (res_id, name, company_id, value_reference, fields_id, type)
                VALUES (%s, 'property_payment_term_id', %s, %s, %s,'many2one')
            """, (f'res.partner,{self.id}', self.company.id, f'account.payment.term,{self.property_payment_term_id.id}', payment_term_field_id[0]))
            print(self.company.id)
            print('§§§§§§§§§§§§§§§§§§§§§§§§§§§§CREATED§§§§§§§§§§§')

    def test(self):
        self.credit_limit = self.plafond_credit
        self.warning_type = self.blocage_type
        self.property_payment_term_id = self.payment_condition

        self.env.cr.execute("""SELECT res_id, name, company_id ,id FROM ir_property WHERE 
                                res_id = %s AND name = 'property_payment_term_id' AND company_id = %s""", 
                                (f'res.partner,{self.id}', self.company.id))

        is_property = self.env.cr.fetchall()
        print('=====================================================================================================================')
        print(is_property)

        if is_property:
            # property_id = is_property[0][3]  
            # property_record = self.env['ir.property'].search([('id','=',property_id),('company_id','!=',1)])
            # print(property_record)
            # property_record.sudo().update({
            #     'value_reference': f'account.payment.term,{self.property_payment_term_id.id}'
            # })
            query_update = """
                            UPDATE ir_property
                            SET value_reference = %s
                            WHERE id = (
                                SELECT id 
                                FROM ir_property 
                                WHERE res_id = %s AND name = 'property_payment_term_id' AND company_id = %s
                            )"""
            self.env.cr.execute(query_update, (
                f'account.payment.term,{self.property_payment_term_id.id}', 
                f'res.partner,{self.id}', 
                self.company.id
            ))
            print(self.company.id)

            print('§§§§§§§§§§§§§§§§§§§§§§§§§§§§UPDATED§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§')


        else:
            # print(f'res.partner,{self.id}')
            # print(self.property_payment_term_id.company_id.id)
            # print(f'account.payment.term,{self.property_payment_term_id.id}')
            payment_term_field = self.env['ir.model.fields'].search([('model', '=', 'res.partner'), ('name', '=', 'property_payment_term_id')])
            print(payment_term_field.id)
            print(payment_term_field)
            self.env['ir.property'].sudo().create({
                'res_id': f'res.partner,{self.id}',
                'name': 'property_payment_term_id',
                'company_id': self.company.id,
                'value_reference':f'account.payment.term,{self.property_payment_term_id.id}',
                'fields_id': payment_term_field.id
                })
            print(self.company.id)
            print('§§§§§§§§§§§§§§§§§§§§§§§§§§§§CREATED§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§')

    def commercial_rejected_boutton(self):
        self.message_post(body=f"La Demandé de credit pour {self.name} de montant {self.plafond_credit} est été REFUSEE par {self.env.user.name}")
        self.state_application_credit='rejected'
        self.visibility_button_commercial = False
        self.confirm_chief==True

    def chief_confirm_boutton(self):
        body_message = ("<div class='col-xs-6'>"
                "<ul>"
                "<li><i>Demande de validation de crédit</i></li>"
                "</ul>"
                "</div>")
        self.message_post(body=f"La Demandé de credit pour {self.name} de montant {self.plafond_credit} est accepté par {self.env.user.name} ")
        self.visibility_button_commercial=True
        groups = self.env['res.groups'].search([('name', '=', 'Commercial')])
        if groups:
            self.message_post(body = body_message, subject = u"Demande de validation de credit", partner_ids = groups.users.partner_id.ids)
            self.message_subscribe(partner_ids = groups.users.partner_id.ids)
        self.confirm_chief=True

    def chief_rejected_boutton(self):
        body_message = ("<div class='col-xs-6'>"
                        "<ul>"
                        "<li><i>Demande de validation de crédit</i></li>"
                        "</ul>"
                        "</div>")
        self.message_post(body=f"La Demandé de credit pour {self.name} de montant {self.plafond_credit} est été réfusé par {self.env.user.name} ")
        self.state_application_credit='rejected'

    def notifications_to_chief(self,chief):
        body_message = ("<div class='col-xs-6'>"
                        "<ul>"
                        "<li><i>Demande de validation de crédit</i></li>"
                        "</ul>"
                        "</div>")
        self.message_post(body=body_message, subject="Demande de validation du Demande de crédit", partner_ids=chief.name.partner_id.ids)
        self.message_post(body=f"{self.env.user.name} a Demandé un credit pour {self.name} de montant {self.plafond_credit}")
        self.requester=self.env.user.id

    def notifications_chief(self):
        body_message = ("<div class='col-xs-6'>"
                        "<ul>"
                        "<li><i>Demande de validation de crédit</i></li>"
                        "</ul>"
                        "</div>")
        self.message_post(body=f"{self.env.user.name} a Demandé un credit pour {self.name} de montant {self.plafond_credit}")
        self.requester=self.env.user.id

    def request_credit_application(self):
        user_id = self.env.user.id
        self.state_application_credit='request'
        self.confirm_chief=False
        model_id = self.env['ir.model'].search([('model', '=', 'sale.order')]).ids
        rules = self.env['rule.rule'].with_context(active_test=False).search([('model_id', 'in', model_id)])
        # print('=====================================gbgb============================================')
        # print(rules)
        id_rule_of_user=[]
        id_rule_user_parent=[]
        id_rule_user_parent_of_parent=[]
        for rule in rules:          
            for user in rule.sale_validation_ids:
                if user_id == user.name.id:
                    # print("Règle:", rule.ids)
                    if rule.parent_id:
                        id_rule_user_parent.append(rule.parent_id.ids)
                        if rule.parent_id.parent_id:
                            id_rule_user_parent_of_parent.append(rule.parent_id.parent_id.ids)
            #         print("Règle:", rule.name)
            #         print("Utilisateurs associés:")
            #         print(user.name.name)
            #         print(user.amount_limit)
                    id_rule_of_user.append(rule.ids)
            # print('*************************************************************************') 
        # print(len(id_rule_of_user))
        body_message = ("<div class='col-xs-6'>"
                        "<ul>"
                        "<li><i>Demande de validation de crédit</i></li>"
                        "</ul>"
                        "</div>")
        user_chef=False
        if len(id_rule_of_user) == 1:
            is_chief=self.env['sale.validation'].search([('rule_id','=',id_rule_of_user[0]),('is_to_chief','=',True),('amount_limit','>=',self.plafond_credit)])            
            if is_chief:
                for user_is_chief in is_chief:
                    if user_is_chief.name.id == user_id:
                        user_chef=True
                if not user_chef: # L'utilisateur actuel n'est pas un chef 
                    self.notifications_to_chief(is_chief)
                else:
                    self.notifications_chief()

            elif len(id_rule_user_parent)>0:
                is_chief_parent=self.env['sale.validation'].search([('rule_id','=',id_rule_user_parent[0]),('is_to_chief','=',True),('amount_limit','>=',self.plafond_credit)])
                if is_chief_parent:
                    for user_is_chief in is_chief_parent:
                        if user_is_chief.name.id == user_id:
                            user_chef=True
                    if user_chef:
                        # self.message_post(body=f"{self.env.user.name} a Demandé un credit pour {self.name} de montant {self.plafond_credit}")
                        # self.state_application_credit= 'request'
                        # self.visibility_button_chief=True
                        self.notifications_chief()
                    else : 
                        # self.message_post(body=body_message, subject="Demande de validation du Demande de crédit", partner_ids=is_chief_parent.name.partner_id.ids)
                        # self.message_post(body=f"{self.env.user.name} a Demandé un credit pour {self.name} de montant {self.plafond_credit}")
                        # self.state_application_credit= 'request'
                        self.notifications_to_chief(is_chief_parent)

                elif len(id_rule_user_parent_of_parent)>0:
                        is_chief_parent_of_parent=self.env['sale.validation'].search([('rule_id','=',id_rule_user_parent_of_parent[0]),('is_to_chief','=',True),('amount_limit','>=',self.plafond_credit)])
                        if is_chief_parent_of_parent:
                            for user_is_chief in is_chief_parent_of_parent:
                                if user_is_chief.name.id == user_id:
                                    user_chef=True
                            if user_chef :
                                # self.message_post(body=f"{self.env.user.name} a Demandé un credit pour {self.name} de montant {self.plafond_credit}")
                                # self.state_application_credit= 'request'
                                # self.visibility_button_chief=True
                                self.notifications_chief()
                            else :
                                # self.message_post(body=body_message, subject="Demande de validation du Demande de crédit", partner_ids=is_chief_parent_of_parent.name.partner_id.ids)
                                # self.message_post(body=f"{self.env.user.name} a Demandé un credit pour {self.name} de montant {self.plafond_credit}")
                                # self.state_application_credit= 'request'
                                self.notifications_to_chief(is_chief_parent_of_parent)
                        else :
                            is_mh=self.env['sale.validation'].search([('rule_id','=',id_rule_user_parent_of_parent[0]),('is_to_mh','=',True)])
                            if is_mh :
                                for user_is_mh in is_mh:
                                    if user_is_mh.name.id == user_id:
                                        user_chef=True
                                if user_chef:
                                    self.notifications_chief()
                                else:
                                    self.notifications_to_chief(is_mh)
                            else :
                                raise exceptions.UserError(f"Mh n'est pas dans la règle {id_rule_user_parent_of_parent[0]}")
                else:
                    is_mh=self.env['sale.validation'].search([('rule_id','=',id_rule_user_parent[0]),('is_to_mh','=',True)])
                    if is_mh :
                        for user_is_mh in is_mh:
                            if user_is_mh.name.id == user_id:
                                user_chef=True
                        if user_chef:
                            self.notifications_chief()
                        else :
                            self.notifications_to_chief(is_mh)
                    else :
                        raise exceptions.UserError(f"Mh n'est pas dans la règle {id_rule_user_parent[0]}")

            else :
                is_mh=self.env['sale.validation'].search([('rule_id','=',id_rule_of_user[0]),('is_to_mh','=',True)])
                if is_mh :
                    for user_is_mh in is_mh:
                        if user_is_mh.name.id == user_id:
                            user_chef=True
                    if user_chef:
                        self.notifications_chief()
                    else :
                        self.notifications_to_chief(is_mh)
                else :
                    raise exceptions.UserError(f"Mh n'est pas dans la règle {id_rule_of_user[0]}")
                    
        elif len(id_rule_of_user) > 1 :
            id_many_rule_of_user=[]
            mh_rule=[]
            for many_rule_of_user in id_rule_of_user:
                is_chief=self.env['sale.validation'].search([('rule_id','=',many_rule_of_user),('is_to_chief','=',True),('amount_limit','>=',self.plafond_credit)])    
                is_mh=self.env['sale.validation'].search([('rule_id','=',many_rule_of_user),('is_to_mh','=',True)])
                if is_chief:
                    for user_is_chief in is_chief:
                        if user_is_chief.name.id == user_id:
                            if user_is_chief.amount_limit >= self.plafond_credit : 
                                # print("¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿")
                                # print(user_is_chief.amount_limit , ">=", self.plafond_credit)
                                user_chef=True
                                id_many_rule_of_user.append(many_rule_of_user)
                if is_mh:
                   mh_rule.append(many_rule_of_user) 

            if user_chef:
                self.notifications_chief()
            else :
                if len(mh_rule)>0:
                    is_mh=self.env['sale.validation'].search([('rule_id','=',mh_rule[0]),('is_to_mh','=',True)])
                    if is_mh:
                        for user_is_mh in is_mh:
                            if user_is_mh.name.id == user_id:
                                user_chef=True
                        if user_chef:
                            self.notifications_chief()
                        else :
                            self.notifications_to_chief(is_mh)
                    else :
                        raise exceptions.UserError(f"MH n'est pas dans la règle {mh_rule[0]}")
                else :
                    raise exceptions.UserError(f"MH n'est pas dans les règles ")
        else :
            raise exceptions.UserError("Vous n'avez pas le droit de demander un crédit")           

    def send_application_credit(self):
        if self.state_application_credit !='request':
            user_id = self.env.user.id
            model_id = self.env['ir.model'].search([('model', '=', 'sale.order')]).ids
            rules = self.env['rule.rule'].with_context(active_test=False).search([('model_id', 'in', model_id)])
            print('=====================================gbgb============================================')
            print(rules)
            rule_of_user=[]
            for rule in rules:          
                for user in rule.sale_validation_ids:
                    if user_id == user.name.id:
                        print("Règle:", rule.ids)
                        print("Règle:", rule.name)
                        print("Utilisateurs associés:")
                        print(user.name.name)
                        rule_of_user.append(rule.name)
                print('*************************************************************************')     
            if len(rule_of_user) > 0:
                #------------------------------------------------------------------------------------------------------------------------------------
                return{
                    'type': 'ir.actions.act_window',
                    'res_model': 'credit_application.wizard',
                    'view_mode': 'form',
                    'target': 'new',
                    'context': {'default_partner_id': self.id},
                    'name': f'Demande de crédit pour {self.name}'
                    }
                #------------------------------------------------------------------------------------------------------------------------------------
            else:
                raise exceptions.UserError("Vous n'avez pas le droit de Demander un credit")
        else:
            raise exceptions.UserError("Une demande est déja en cour")