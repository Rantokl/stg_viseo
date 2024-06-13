from odoo import models, fields,api, exceptions
        # if self.company_type == self.env['res.partner'].sudo().search([('selection_company_type','=','person')]):
        # if create_config_cin_partner:
        #     self.cin_document_partner.required = True
        #     print('#################################TRUE######################################')
        # else :
        #     self.cin_document_partner.required = False
        #     print('#################################FALSE######################################')

        # return super(PartnerInformationDocument, self).create(values)

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

    @api.model
    def create(self, values):
        rule_person = self.env['viseo_partner_info.create_config_model'].search([('selection_company_type', '=', 'person')])
        print('################################CREATION#######################################')
        print(rule_person)
        if rule_person:
            print('################################CREATION#######################################')
            print(rule_person.selection_company_type)
            print(rule_person.create_config_cin_partner)
            print(values.get('company_type'))
        # Rest of your logic using rule_person fields
        else:
        # Handle the case where no rule is found (optional)
            print("No rule found for company type 'person'")

        if rule_person.selection_company_type == 'person':
            if values.get('company_type') == rule_person.selection_company_type :
                if rule_person.create_config_cin_partner:
                    if not self.cin_document_partner:
                        raise exceptions.UserError("Ajouter le Fichier CIN dans l'onglet Document est obligatoire!!")
                if rule_person.create_config_cif_partner:
                    if not self.cif_document_partner:
                        raise exceptions.UserError("Ajouter le Fichier CIF dans l'onglet Document est obligatoire!!")
                if rule_person.create_config_nif_partner:
                    if not self.nif_document_partner:
                        raise exceptions.UserError("Ajouter le Fichier NIF dans l'onglet Document est obligatoire!!")
                if rule_person.create_config_rcs_partner:
                    if not self.rcs_document_partner:
                        raise exceptions.UserError("Ajouter le Fichier RCS dans l'onglet Document, C'est obligatoire!!")
                if rule_person.create_config_stat_partner:
                    if not self.stat_document_partner:
                        raise exceptions.UserError("Ajouter le Fichier STAT dans l'onglet Document est obligatoire!!")
                    
        elif rule_person.selection_company_type == 'company':
            if values.get('company_type') == rule_person.selection_company_type :
                if rule_person.create_config_cin_partner:
                    if not self.cin_document_partner:
                        raise exceptions.UserError("Ajouter le Fichier CIN dans l'onglet Document est obligatoire!!")
                if rule_person.create_config_cif_partner:
                    if not self.cif_document_partner:
                        raise exceptions.UserError("Ajouter le Fichier CIF dans l'onglet Document est obligatoire!!")
                if rule_person.create_config_nif_partner:
                    if not self.nif_document_partner:
                        raise exceptions.UserError("Ajouter le Fichier NIF dans l'onglet Document est obligatoire!!")
                if rule_person.create_config_rcs_partner:
                    if not self.rcs_document_partner:
                        raise exceptions.UserError("Ajouter le Fichier RCS dans l'onglet Document, C'est obligatoire!!")
                if rule_person.create_config_stat_partner:
                    if not self.stat_document_partner:
                        raise exceptions.UserError("Ajouter le Fichier STAT dans l'onglet Document est obligatoire!!")
        return super(PartnerInformationDocument, self).create(values)

    @api.model
    def write(self, values):
        rule_person = self.env['viseo_partner_info.create_config_model'].search([('selection_company_type', '=', 'person')])
        print('################################MODIFICATION#######################################')
        print(rule_person)
        print('values')
        if rule_person:
            print('################################MODIFICATION#######################################')
            print(rule_person.selection_company_type)
            print(rule_person.create_config_cin_partner)
            print(values.get('company_type'))
            return super(PartnerInformationDocument, self).write(values)
        # Rest of your logic using rule_person fields
        else:
        # Handle the case where no rule is found (optional)
            print("No rule found for company type 'person'")


        

class PartnerInformationDocumentCheck(models.Model):
    _name = 'viseo_partner_info.create_config_model'

    selection_company_type = fields.Selection([('person', 'Particulier'), ('company', 'Société')], string='Type de Client', required=True)
    create_config_cin_partner = fields.Boolean(string="CIN partner document", default=False)
    create_config_cif_partner = fields.Boolean(string="CIF partner document", default=False)
    create_config_nif_partner = fields.Boolean(string="NIF partner document", default=False)
    create_config_rcs_partner = fields.Boolean(string="RCS partner document", default=False)
    create_config_stat_partner = fields.Boolean(string="STAT partner document", default=False)

    @api.model
    def create(self, values):
        existing_records = self.search([('selection_company_type', '=', values['selection_company_type'])])
        if existing_records:
            raise exceptions.UserError("Un enregistrement avec le même type de société existe déjà.")
        return super(PartnerInformationDocumentCheck, self).create(values)

    #     record=self.env['viseo_partner_info.create_config_model'].search([('selection_company_type', '=', 'person')])

    #     print('#################################MODIFICATION######################################')
    #     print('selection_company_type',record.selection_company_type)
    #     print('create_config_cin_partner',record.create_config_cin_partner)
    #     print('create_config_cif_partner',record.create_config_cif_partner)
    #     print('create_config_nif_partner',record.create_config_nif_partner)
    #     print('create_config_rcs_partner',record.create_config_rcs_partner)
    #     print('create_config_stat_partner',record.create_config_stat_partner)
    #     print('company_type',self.company_type)
    #     return super(PartnerInformationDocument, self).write(vals)