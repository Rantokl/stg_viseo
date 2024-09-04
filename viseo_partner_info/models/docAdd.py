# -*- coding: utf-8 -*-

from odoo import models, fields, api, exceptions


class WizardCreditApplication(models.TransientModel):
    _name = 'add_doc_partner.wizard'

    partner_id = fields.Many2one('res.partner')
    cin_document_partner = fields.Binary(string='Document CIN', attachment=True)
    cin_document_partner_filename = fields.Char(string='Nom du document CIN')

    # rib_document_partner = fields.Binary(string='Document RIB', attachment=True)
    # rib_document_partner_filename = fields.Char(string='Nom du document RIB')

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

    cin_represent = fields.One2many('cin.wizard', 'wizard_id', string='CIN du représentant')
    cr_represent = fields.One2many('cr.wizard', 'wizard_id', string='CR du représentant')
    rib_represent = fields.One2many('rib.wizard', 'wizard_id', string='RIB du représentant')
    rib_document = fields.One2many('rib.document.wizard','wizard_id',  string='Document RIB')
    company_type = fields.Selection([('person','Particulier'),('company','Société')], related='partner_id.company_type')

    hide_button_delete = fields.Html(string='CSS', sanitize=False, default='<style>.o_clear_file_button {display: none !important;}</style>')


    def add_doc_partner(self):
        cin_represent_data = [(0, 0, {
            'cin_represent': doc.cin_represent,
            'partner_id': self.partner_id.id
        }) for doc in self.cin_represent]

        cr_represent_data = [(0, 0, {
            'cr_represent': doc.cr_represent,
            'partner_id': self.partner_id.id
        }) for doc in self.cr_represent]

        rib_represent_data = [(0, 0, {
            'rib_represent': doc.rib_represent,
            'partner_id': self.partner_id.id
        }) for doc in self.rib_represent]

        rib_document_data = [(0, 0, {
            'rib_document': doc.rib_document,
            'partner_id': self.partner_id.id
        }) for doc in self.rib_document]
        # =========================== MISE A JOUR DES CHAMPS DANS L'ONGLET DOCUMENT ==============================

        self.partner_id.sudo().write({
            "cif_document_partner": self.cif_document_partner,
            "rcs_document_partner": self.rcs_document_partner,
            "nif_document_partner": self.nif_document_partner,
            "stat_document_partner": self.stat_document_partner,
            "cin_document_partner": self.cin_document_partner,
            "cif_expiration_date": self.cif_expiration_date,
            "rcs_expiration_date": self.rcs_expiration_date,
            "cif_declaration_date": self.cif_declaration_date,
            "rcs_declaration_date": self.rcs_declaration_date,
            "cin_represent": [(5, 0, {})] + cin_represent_data,
            "cr_represent":  [(5, 0, {})] + cr_represent_data,
            "rib_represent": [(5, 0, {})] + rib_represent_data,
            "rib_document": [(5, 0, {})] + rib_document_data
        })
        # ================================================================================================================
class viseo_add_document_partner(models.Model):
    _inherit = 'res.partner'

    def add_doc_partner_from_wizard(self):
        
        cin_represent_data = []
        cr_represent_data = []
        rib_represent_data = []
        rib_document_data = []

        for document in self.cin_represent:
            cin_represent_data.append((0, 0, {
                'cin_represent': document.cin_represent,             
                }))
        for document in self.cr_represent:
            cr_represent_data.append((0, 0, {
                'cr_represent': document.cr_represent,             
                }))
        for document in self.rib_represent:
            rib_represent_data.append((0, 0, {
                'rib_represent': document.rib_represent,             
                }))
        for document in self.rib_document:
            rib_document_data.append((0, 0, {
                'rib_document': document.rib_document,
                }))
        # =======================================================================================================================================
        wizard_id = self.env['add_doc_partner.wizard'].create({'partner_id': self.id,
                'rcs_document_partner': self.rcs_document_partner,
                'company_type': self.company_type,
                'rcs_declaration_date': self.rcs_declaration_date,
                'rcs_expiration_date': self.rcs_expiration_date,
                'cif_document_partner': self.cif_document_partner,
                'cif_declaration_date': self.cif_declaration_date,
                'cif_expiration_date': self.cif_expiration_date,
                'cin_document_partner': self.cin_document_partner,
                'cr_document_partner': self.cr_document_partner,
                'nif_document_partner': self.nif_document_partner,
                'stat_document_partner': self.stat_document_partner,
                'cin_represent': cin_represent_data,
                'cr_represent': cr_represent_data,
                'rib_represent': rib_represent_data,
                'rib_document': rib_document_data})
        return{
            'type': 'ir.actions.act_window',
            'res_model': 'add_doc_partner.wizard',
            'res_id' : wizard_id.id,
            'view_mode': 'form',
            'target': 'new',
            'name': f'Ajout Document de {self.name}'
        }