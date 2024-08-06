from odoo import models, fields,api, exceptions
from odoo.exceptions import UserError
from PIL import Image
import base64
import io

class PartnerInformationDocument(models.Model):
    _inherit = 'res.partner'

    cin_document_partner = fields.Binary(string='Document CIN', attachment=True)
    cin_document_partner_filename = fields.Char(string='Nom du document CIN')

    rib_document_partner = fields.Binary(string='Document RIB', attachment=True)
    rib_document_partner_filename = fields.Char(string='Nom du document RIB')

    cr_document_partner = fields.Binary(string='Certificat de Résidence', attachment=True)
    cr_document_partner_filename = fields.Char(string='Nom du document CR')

    cif_document_partner = fields.Binary(string='Document CIF', attachment=True)
    cif_document_partner_filename = fields.Char(string='Nom du document CIF')
    cif_expiration_date = fields.Date(string="CIF Expire le")
    cif_declaration_date = fields.Date(string="CIF Du")
    required_cif=fields.Boolean(default=False, compute='compute_required_cif')

    nif_document_partner = fields.Binary(string='Document NIF', attachment=True)
    nif_document_partner_filename = fields.Char(string='Nom du document NIF')

    rcs_document_partner = fields.Binary(string='Document RCS', attachment=True)
    rcs_document_partner_filename = fields.Char(string='Nom du document RCS')
    rcs_expiration_date = fields.Date(string="RCS Expire le")
    rcs_declaration_date = fields.Date(string="RCS Du")
    required_rcs=fields.Boolean(default=False, compute='compute_required_rcs')

    stat_document_partner = fields.Binary(string='Document STAT', attachment=True)
    stat_document_partner_filename = fields.Char(string='Nom du document STAT')

    # cin_document_partner_represent = fields.Binary(string='CIN Représentant ', attachment=True)
    # cin_document_partner_represent = fields.Many2many('ir.attachment', string='CIN Représentant')
    # cin_document_partner_filename_represent = fields.Char(string='Nom du document CIN Représentant')
    cin_represent = fields.One2many(
        comodel_name='cin.represent', 
        inverse_name='partner_id', 
        string='CIN du représentant'
    )
    cr_represent = fields.One2many(
        comodel_name='cr.represent', 
        inverse_name='partner_id', 
        string='CR du représentant'
    )
    rib_represent = fields.One2many(
        comodel_name='rib.represent', 
        inverse_name='partner_id', 
        string='RIB du représentant'
    )
    cr_document_partner_filename_represent = fields.Char(string='Nom du document RIB Représentant')

    @api.depends('rcs_document_partner')
    def compute_required_rcs(self):
        if self.rcs_document_partner:
            if not self.rcs_expiration_date:
                self.required_rcs=True
            else :
                self.required_rcs =False
        else :
            self.required_rcs =False
    
    @api.depends('cif_document_partner')
    def compute_required_cif(self):
        if self.cif_document_partner:
            if not self.cif_expiration_date:
                self.required_cif =True
                
            else :
                self.required_cif =False
        else :
            self.required_cif =False
            
    # def abcd(self):
    #     field_name = 'x_new_field'
    #     self.env['ir.model.fields'].create({
    #         'name': field_name,
    #         'model': 'model.name',
    #         'model_id': self.env['ir.model']._get_id('model.name'),
    #         'field_description': 'New Field',
    #         'ttype': 'char',
    #     })
    #     return {
    #         'type': 'ir.actions.client',
    #         'tag': 'reload',
    #     }
    
    @api.model
    def create(self, values):
        if values.get('rcs_document_partner'):
            if not values.get('rcs_expiration_date'):
                raise exceptions.UserError(f"Ajouter la date d'éxpiration de RCS")
        if values.get('cif_document_partner'):
            if not values.get('cif_expiration_date'):
                raise exceptions.UserError(f"Ajouter la date d'éxpiration de CIF")
        return super(PartnerInformationDocument, self).create(values)
    
    def write(self, values):
        if 'rcs_document_partner' in values:
            if values['rcs_document_partner']:
                if 'rcs_expiration_date' in values:
                    if not values['rcs_expiration_date']:
                        raise exceptions.UserError(f"Ajouter la date d'expiration de RCS")
                elif not self.rcs_expiration_date :
                    raise exceptions.UserError(f"Ajouter la date d'expiration de RCS")
        elif self.rcs_document_partner:
            if 'rcs_expiration_date' in values:
                if not values['rcs_expiration_date'] :
                    raise exceptions.UserError(f"Ajouter la date d'expiration de RCS")
        elif not self.rcs_expiration_date:
            if 'rcs_document_partner' in values:
                if values['rcs_expiration_date'] :
                    raise exceptions.UserError(f"Ajouter la date d'expiration de RCS")
        elif 'rcs_expiration_date' in values:
            if not values['rcs_expiration_date'] :
                if self.rcs_document_partner:
                    raise exceptions.UserError(f"Ajouter la date d'expiration de RCS")

        if 'cif_document_partner' in values:
            if values['cif_document_partner']:
                if 'cif_expiration_date' in values:
                    if not values['cif_expiration_date']:
                        raise exceptions.UserError(f"Ajouter la date d'expiration de CIF")
                elif not self.cif_expiration_date :
                    raise exceptions.UserError(f"Ajouter la date d'expiration de CIF")
        elif self.cif_document_partner:
            if 'cif_expiration_date' in values:
                if not values['cif_expiration_date'] :
                    raise exceptions.UserError(f"Ajouter la date d'expiration de CIF")
        elif not self.cif_expiration_date:
            if 'cif_document_partner' in values:
                if values['cif_expiration_date'] :
                    raise exceptions.UserError(f"Ajouter la date d'expiration de CIF")
        elif not self.cif_expiration_date:
            if self.cif_document_partner:
                raise exceptions.UserError(f"Ajouter la date d'expiration de CIF")
        elif 'cif_expiration_date' in values:
            if not values['cif_expiration_date'] :
                if self.cif_document_partner:
                    raise exceptions.UserError(f"Ajouter la date d'expiration de CIF")
        # print("==============================================================="*2)
        return super(PartnerInformationDocument, self).write(values)

# ======================================= CONVERTION D'IMAGE EN PDF ====================================================
    # def _convert_to_pdf(self, file_content, filename):
    #     file_extension = filename.split('.')[-1].lower()
    #     if file_extension not in ['jpg', 'jpeg', 'png']:
    #         return file_content, filename

    #     try:
    #         image = Image.open(io.BytesIO(base64.b64decode(file_content)))
    #         image_converted = image.convert("RGB")
    #         output = io.BytesIO()
    #         image_converted.save(output, format="PDF")
    #         pdf_content = base64.b64encode(output.getvalue())
    #         pdf_filename = "{}.pdf".format(filename.rsplit('.', 1)[0])
    #         return pdf_content, pdf_filename
    #     except Exception as e:
    #         raise UserError("Error converting image to PDF: {}".format(str(e)))

    #     return file_content, filename
 #=============================================================================================================================   

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
    create_config_cr_partner = fields.Boolean(string="CR", default=False)
    create_config_rib_partner = fields.Boolean(string="RIB", default=False)
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

# ============================================================ CREATE PARTNER IN DEVIS ==================================================================

class PartnerCreationInDevis(models.Model):
    _inherit='sale.order'

    def cin_file_empty_raise_error(self):
       raise exceptions.UserError("Pour le client Particulier, Il faut ajouter le CIN dans l'onglet 'Document' dans la fiche partner")

    def cr_file_empty_raise_error(self):
       raise exceptions.UserError("Pour le client Particulier, Il faut ajouter la Cértificat de Résidence(CR) dans l'onglet 'Document' dans la fiche partner")

    def rib_file_empty_raise_error(self):
       raise exceptions.UserError("Il faut ajouter le RIB dans l'onglet 'Document' dans la fiche partner")
    
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
                # =========================  CR   ================================
                if rule_person.create_config_cr_partner:
                    if not self.partner_id.cr_document_partner:
                        self.cr_file_empty_raise_error()
                # ============================  RIB  =============================
                if rule_person.create_config_rib_partner:
                    if not self.partner_id.rib_document_partner:
                        self.rib_file_empty_raise_error()
                # ================================================================
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
                # ============================  CR  ====================================
                if company_rule.create_config_cr_partner:
                    if not self.partner_id.cr_document_partner:
                        self.cr_file_empty_raise_error()
                # ============================  RIB  ===================================
                if company_rule.create_config_rib_partner:
                    if not self.partner_id.rib_document_partner:
                        self.rib_file_empty_raise_error()
                # ======================================================================
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
