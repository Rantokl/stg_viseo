from odoo import models, fields,api, exceptions


class PartnerInformationDocument(models.Model):
    _inherit = 'res.partner'

    cin_document_partner = fields.Binary(string='Document CIN', attachment=True)
    cin_document_partner_filename = fields.Char(string='Nom du document CIN')

    cif_document_partner = fields.Binary(string='Document CIF', attachment=True)
    cif_document_partner_filename = fields.Char(string='Nom du document CIF')

    nif_document_partner = fields.Binary(string='Document NIF', attachment=True)
    nif_document_partner_filename = fields.Char(string='Nom du document NIF')

    rcs_document_partner = fields.Binary(string='Document RCS', attachment=True)
    rcs_document_partner_filename = fields.Char(string='Nom du document RCS')

    stat_document_partner = fields.Binary(string='Document STAT', attachment=True)
    stat_document_partner_filename = fields.Char(string='Nom du document STAT')

# ======================================= RULE TO CREATE CONTACT (SIMPLE) ====================================================
    # @api.model
    # def create(self, values):
    #     rule_person = self.env['viseo_partner_info.create_config_model'].search([('selection_company_type', '=', 'person')])
    #     company_rule=self.env['viseo_partner_info.create_config_model'].search([('selection_company_type', '=', 'company')])
    #     if rule_person and company_rule:
    #         if values.get('company_type') == rule_person.selection_company_type :
    #             if rule_person.create_config_cin_partner:
    #                 if not values.get('cin_document_partner'):
    #                     self.cin_file_empty_raise_error()
    #             if rule_person.create_config_cif_partner:
    #                 if not values.get('cif_document_partner'):
    #                     self.cif_file_empty_raise_error()
    #             if rule_person.create_config_nif_partner:
    #                 if not values.get('nif_document_partner'):
    #                     self.nif_file_empty_raise_error()
    #                 if not values.get('rcs_document_partner'):
    #                     self.rcs_file_empty_raise_error()
    #             if rule_person.create_config_stat_partner:
    #                 if not values.get('stat_document_partner'):
    #                     self.stat_file_empty_raise_error()
                    
    #         elif values.get('company_type') == company_rule.selection_company_type :
    #             if company_rule.create_config_cin_partner:
    #                 if not values.get('cin_document_partner'):
    #                     self.cin_file_empty_raise_error()
    #             if company_rule.create_config_cif_partner:
    #                 if not values.get('cif_document_partner'):
    #                     self.cif_file_empty_raise_error()
    #             if company_rule.create_config_nif_partner:
    #                 if not values.get('nif_document_partner'):
    #                     self.nif_file_empty_raise_error()
    #             if company_rule.create_config_rcs_partner:
    #                 if not values.get('rcs_document_partner'):
    #                     self.rcs_file_empty_raise_error()
    #             if company_rule.create_config_stat_partner:
    #                 if not values.get('stat_document_partner'):
    #                     self.stat_file_empty_raise_error()
    #         return super(PartnerInformationDocument, self).create(values)

    #     else:
    #         raise exceptions.UserError("Ajouter les règles lors de la creation des Clients. Dans menu 'configuration'/'configuration creation'")

    # def rule_function_update(self,values,rule_person,company_rule):
    #     if values['company_type'] == rule_person.selection_company_type :
    #         print('*************************PERSONE-MODIF')
    #         if rule_person.create_config_cin_partner:
    #             if 'cin_document_partner' in values:
    #                 if not values['cin_document_partner']:
    #                     self.cin_file_empty_raise_error()
    #         if rule_person.create_config_cif_partner:
    #             if 'cif_document_partner' in values:
    #                 if not values['cif_document_partner'] :
    #                     self.cif_file_empty_raise_error()
    #         if rule_person.create_config_nif_partner:
    #             if 'nif_document_partner' in values:
    #                 if not values['nif_document_partner'] :
    #                     self.nif_file_empty_raise_error()
    #         if rule_person.create_config_rcs_partner:
    #             if 'rcs_document_partner' in values:
    #                 if not values['rcs_document_partner'] :
    #                     self.rcs_file_empty_raise_error()
    #         if rule_person.create_config_stat_partner:
    #             if 'stat_document_partner' in values:
    #                 if not values['stat_document_partner']:
    #                     self.stat_file_empty_raise_error()
                
    #     elif values['company_type'] == company_rule.selection_company_type :
    #         if company_rule.create_config_cin_partner:
    #             if 'cin_document_partner' in values:
    #                 if not values['cin_document_partner']:
    #                     self.cin_file_empty_raise_error()
    #         if company_rule.create_config_cif_partner:
    #             if 'cif_document_partner' in values:
    #                 if not values['cif_document_partner'] :
    #                     self.cif_file_empty_raise_error()
    #         if company_rule.create_config_nif_partner:
    #             if 'nif_document_partner' in values:
    #                 if not values['nif_document_partner'] :
    #                     self.nif_file_empty_raise_error()
    #         if company_rule.create_config_rcs_partner:
    #             if 'rcs_document_partner' in values:
    #                 if not values['rcs_document_partner'] :
    #                     self.rcs_file_empty_raise_error()
    #         if company_rule.create_config_stat_partner :
    #             if 'stat_document_partner' in values:
    #                 if not values['stat_document_partner']:
    #                     self.stat_file_empty_raise_error()

    # @api.model
    # def write(self, values):
    #     rule_person = self.env['viseo_partner_info.create_config_model'].search([('selection_company_type', '=', 'person')])
    #     company_rule=self.env['viseo_partner_info.create_config_model'].search([('selection_company_type', '=', 'company')])
    #     if 'company_type' in values:
    #         if rule_person and company_rule:
    #             self.rule_function_update(values,rule_person,company_rule)
    #         else:
    #             raise exceptions.UserError("Ajouter les règles lors de la creation des Clients. Dans menu 'configuration'/'configuration creation'")
        
    #     elif ('cin_document_partner' in values or 'cif_document_partner' in values or 'nif_document_partner' in values or 'rcs_document_partner' in values or 'stat_document_partner' in values ) :
    #         if self.company_type == rule_person.selection_company_type :
    #             if rule_person.create_config_cin_partner:
    #                 if 'cin_document_partner' in values:
    #                     if not values['cin_document_partner']:
    #                         self.cin_file_empty_raise_error()
    #             if rule_person.create_config_cif_partner:
    #                 if 'cif_document_partner' in values:
    #                     if not values['cif_document_partner']:
    #                         self.cif_file_empty_raise_error()
    #             if rule_person.create_config_nif_partner:
    #                 if 'nif_document_partner' in values:
    #                     if not values['nif_document_partner']:
    #                         self.nif_file_empty_raise_error()
    #             if rule_person.create_config_rcs_partner:
    #                 if 'rcs_document_partner' in values:
    #                     if not values['rcs_document_partner']:
    #                         self.rcs_file_empty_raise_error()
    #             if rule_person.create_config_stat_partner:
    #                 if 'stat_document_partner' in values:
    #                     if not values['stat_document_partner']:
    #                         self.stat_file_empty_raise_error()
                    
    #         elif self.company_type == company_rule.selection_company_type :
    #             if company_rule.create_config_cin_partner:
    #                 if 'cin_document_partner' in values:
    #                     if not values['cin_document_partner']:  
    #                         self.cin_file_empty_raise_error()
    #             if company_rule.create_config_cif_partner:
    #                 if 'cif_document_partner' in values:
    #                     if not values['cif_document_partner']:
    #                         self.cif_file_empty_raise_error()
    #             if company_rule.create_config_nif_partner:
    #                  if 'nif_document_partner' in values:
    #                     if not values['nif_document_partner']:
    #                         self.nif_file_empty_raise_error()
    #             if company_rule.create_config_rcs_partner:
    #                 if 'rcs_document_partner' in values:
    #                     if not values['rcs_document_partner']:
    #                         self.rcs_file_empty_raise_error()
    #             if company_rule.create_config_stat_partner :
    #                 if 'stat_document_partner' in values:
    #                     if not values['stat_document_partner']:
    #                         self.stat_file_empty_raise_error()  
    #     else :
    #         if self.company_type == rule_person.selection_company_type :
    #             if rule_person.create_config_cin_partner:
    #                 if not self.cin_document_partner :
    #                     self.cin_file_empty_raise_error()
    #             if rule_person.create_config_cif_partner:
    #                 if not self.cif_document_partner :
    #                     self.cif_file_empty_raise_error()
    #             if rule_person.create_config_nif_partner:
    #                 if not self.nif_document_partner:
    #                     self.nif_file_empty_raise_error()
    #             if rule_person.create_config_rcs_partner:
    #                 if not self.rcs_document_partner:
    #                     self.rcs_file_empty_raise_error()
    #             if rule_person.create_config_stat_partner:
    #                 if not self.stat_document_partner:
    #                     self.stat_file_empty_raise_error()
                    
    #         elif self.company_type == company_rule.selection_company_type :
    #             if company_rule.create_config_cin_partner:
    #                 if not self.cin_document_partner:
    #                     self.cin_file_empty_raise_error()
    #             if company_rule.create_config_cif_partner:
    #                 if not self.cif_document_partner:
    #                     self.cif_file_empty_raise_error()
    #             if company_rule.create_config_nif_partner:
    #                 if not self.nif_document_partner:
    #                     self.nif_file_empty_raise_error()
    #             if company_rule.create_config_rcs_partner:
    #                 if not self.rcs_document_partner:
    #                     self.rcs_file_empty_raise_error()
    #             if company_rule.create_config_stat_partner :
    #                 if not self.stat_document_partner:
    #                     self.stat_file_empty_raise_error()
                    
    #     return super(PartnerInformationDocument, self).write(values)

    # def cin_file_empty_raise_error(self):
    #    raise exceptions.UserError("Ajouter le Fichier CIN dans l'onglet Document est obligatoire!!")
    
    # def cif_file_empty_raise_error(self):
    #    raise exceptions.UserError("Ajouter le Fichier CIF dans l'onglet Document est obligatoire!!")
    
    # def nif_file_empty_raise_error(self):
    #    raise exceptions.UserError("Ajouter le Fichier NIF dans l'onglet Document est obligatoire!!")
    
    # def rcs_file_empty_raise_error(self):
    #    raise exceptions.UserError("Ajouter le Fichier RCS dans l'onglet Document est obligatoire!!")
    
    # def stat_file_empty_raise_error(self):
    #    raise exceptions.UserError("Ajouter le Fichier STAT dans l'onglet Document est obligatoire!!")
 #=============================================================================================================================   

class PartnerInformationDocumentCheck(models.Model):
    _name = 'viseo_partner_info.create_config_model'

    selection_company_type = fields.Selection([('person', 'Particulier'), ('company', 'Société')], string='Type de Client', required=True)
    create_config_cin_partner = fields.Boolean(string="CIN", default=False)
    create_config_cif_partner = fields.Boolean(string="CIF", default=False)
    create_config_nif_partner = fields.Boolean(string="NIF", default=False)
    create_config_rcs_partner = fields.Boolean(string="RCS", default=False)
    create_config_stat_partner = fields.Boolean(string="STAT", default=False)

    @api.model
    def create(self, values):
        existing_records = self.search([('selection_company_type', '=', values['selection_company_type'])])
        if existing_records:
            raise exceptions.UserError(f"Une règle avec la même type de Client '{existing_records.selection_company_type}' existe déjà.")
        return super(PartnerInformationDocumentCheck, self).create(values)



# ============================= CREATE PARTNER IN DEVIS ==================================================================

class PartnerCreationInDevis(models.Model):
    _inherit='sale.order'

    def cin_file_empty_raise_error(self):
       raise exceptions.UserError("Pour le client Particulier, Il faut ajouter le CIN dans l'onglet 'Document' dans la fiche partner")
    
    def cif_file_empty_raise_error(self):
       raise exceptions.UserError("Pour le client Société, Il faut ajouter le CIF dans l'onglet 'Document' dans la fiche partner")
    
    def nif_file_empty_raise_error(self):
       raise exceptions.UserError("Pour le client Société, Il faut ajouter le NIF dans l'onglet 'Document' dans la fiche partner")
    
    def rcs_file_empty_raise_error(self):
       raise exceptions.UserError("Pour le client Société, Il faut ajouter le RCS dans l'onglet 'Document' dans la fiche partner")
    
    def stat_file_empty_raise_error(self):
       raise exceptions.UserError("Pour le client Société, Il faut ajouter le STAT dans l'onglet 'Document' dans la fiche partner")

    def action_confirm(self):
        rule_person = self.env['viseo_partner_info.create_config_model'].search([('selection_company_type', '=', 'person')])
        company_rule=self.env['viseo_partner_info.create_config_model'].search([('selection_company_type', '=', 'company')])

        if rule_person and company_rule:
            if self.partner_id.company_type == rule_person.selection_company_type :
                if rule_person.create_config_cin_partner:
                    if not self.partner_id.cin_document_partner:
                        self.cin_file_empty_raise_error()
                if rule_person.create_config_cif_partner:
                    if not self.partner_id.cif_document_partner:
                        self.cif_file_empty_raise_error()
                if rule_person.create_config_nif_partner:
                    if not self.partner_id.nif_document_partner:
                        self.nif_file_empty_raise_error()
                    if not self.partner_id.rcs_document_partner:
                        self.rcs_file_empty_raise_error()
                if rule_person.create_config_stat_partner:
                    if not self.partner_id.stat_document_partner:
                        self.stat_file_empty_raise_error()
                    
            elif self.partner_id.company_type == company_rule.selection_company_type :
                if company_rule.create_config_cin_partner:
                    if not self.partner_id.cin_document_partner:
                        self.cin_file_empty_raise_error()
                if company_rule.create_config_cif_partner:
                    if not self.partner_id.cif_document_partner:
                        self.cif_file_empty_raise_error()
                if company_rule.create_config_nif_partner:
                    if not self.partner_id.nif_document_partner:
                        self.nif_file_empty_raise_error()
                if company_rule.create_config_rcs_partner:
                    if not self.partner_id.rcs_document_partner:
                        self.rcs_file_empty_raise_error()
                if company_rule.create_config_stat_partner:
                    if not self.partner_id.stat_document_partner:
                        self.stat_file_empty_raise_error()
            # return super(PartnerInformationDocument, self).create(values)

        else:
            raise exceptions.UserError("Ajouter les règles lors de la creation des Clients. Dans le module 'Contact', menu 'Configuration'/'configuration creation'")
        return super(PartnerCreationInDevis, self).action_confirm()
