# -*- coding: utf-8 -*-

from odoo import models, fields, api, exceptions


class WizardCreditApplication(models.TransientModel):
    _name = 'add_doc_partner.wizard'

    partner_id = fields.Many2one('res.partner')
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
    

    nif_document_partner = fields.Binary(string='Document NIF', attachment=True)
    nif_document_partner_filename = fields.Char(string='Nom du document NIF')

    rcs_document_partner = fields.Binary(string='Document RCS', attachment=True)
    rcs_document_partner_filename = fields.Char(string='Nom du document RCS')
    rcs_expiration_date = fields.Date(string="RCS Expire le")
    rcs_declaration_date = fields.Date(string="RCS Du")

    stat_document_partner = fields.Binary(string='Document STAT', attachment=True)
    stat_document_partner_filename = fields.Char(string='Nom du document STAT')

    # cin_document_partner_represent = fields.Binary(string='CIN Représentant ', attachment=True)
    # cin_document_partner_represent = fields.Many2many('ir.attachment', string='CIN Représentant')
    # cin_document_partner_filename_represent = fields.Char(string='Nom du document CIN Représentant')
    document_partner_represent = fields.One2many(
        comodel_name='viseo_document_partner.partner_document', 
        inverse_name='partner_id', 
        string='Document du représentant'
    )
    company_type= fields.Selection([('person','Particulier'),('company','Société')], store=True)

    def button_add_doc_partner_from_wizard(self):

        # ===========================MISE A JOUR DES CHAMPS DANS L'ONGLET DOCUMENT ==============================
        self.partner_id.sudo().update({
            "cif_document_partner":self.cif_document_partner,
            "rcs_document_partner":self.rcs_document_partner,
            "rib_document_partner":self.rib_document_partner,
            "nif_document_partner":self.nif_document_partner,
            "stat_document_partner":self.stat_document_partner,
            "cin_document_partner":self.cin_document_partner,
            "cif_expiration_date":self.cif_expiration_date,
            "rcs_expiration_date":self.rcs_expiration_date,
            "cif_declaration_date":self.cif_declaration_date,
            "rcs_declaration_date":self.rcs_declaration_date,
            'document_partner_represent': [(5 ,0 ,0 )] +[(0, 0, {
                'cin_represent': doc.cin_represent,
                'cr_represent': doc.cr_represent,   
            }) for doc in self.document_partner_represent]
        })
        # ================================================================================================================
class viseo_add_document_partner(models.Model):
    _inherit = 'res.partner'

    def add_doc_partner_from_wizard(self):
        
        document_partner_represent_data = []
        for document in self.document_partner_represent:
            document_partner_represent_data.append((0, 0, {
                'cin_represent': document.cin_represent,
                'cr_represent': document.cr_represent,              
                }))
        # =============================================== WIZARD ========================================================
        # print('='*50)
        # print(self.env.ref('viseo_add_document_partner.viseo_add_document_partner_action_wizard_add_doc_wizard_form'))
        # return{
        #     'type': 'ir.actions.act_window',
        #     'res_model': 'res.partner',
        #     'res_id':self.id,
        #     'view_mode': 'form',
        #     # 'view_id': self.env.ref('viseo_add_document_partner.viseo_add_document_partner_action_wizard_add_doc_wizard_form').id,
        #     'views': [(self.env.ref('viseo_add_document_partner.viseo_add_document_partner_action_wizard_add_doc_wizard_form').id, 'form')],
        #     'target': 'new',
        #     'name': f'Ajout Document de {self.name}'
        #     }
       # =======================================================================================================================================
    #    action = self.env.ref('viseo_add_document_partner.new_partner_action_').read()[0]

        # =======================================================================================================================================
        # action = self.env.ref('viseo_add_document_partner.new_partner_action_').read()[0]
        # action["res_id"] = self.id
        # return action
        # =======================================================================================================================================
        return{
            'type': 'ir.actions.act_window',
            'res_model': 'add_doc_partner.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_partner_id': self.id,
                'default_rcs_document_partner': self.rcs_document_partner,
                'default_company_type': self.company_type,
                'default_rcs_declaration_date': self.rcs_declaration_date,
                'default_rcs_expiration_date': self.rcs_expiration_date,
                'default_cif_document_partner': self.cif_document_partner,
                'default_cif_declaration_date': self.cif_declaration_date,
                'default_cif_expiration_date': self.cif_expiration_date,
                'default_cin_document_partner': self.cin_document_partner,
                'default_rib_document_partner': self.rib_document_partner,
                'default_cr_document_partner': self.cr_document_partner,
                'default_nif_document_partner': self.nif_document_partner,
                'default_stat_document_partner': self.stat_document_partner,
                'default_document_partner_represent': document_partner_represent_data
            },
            'name': f'Ajout Document de {self.name}'
        }