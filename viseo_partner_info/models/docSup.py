from odoo import models, fields, api


class viseo_document_cin_represent(models.Model):
    _name = 'cin.represent'

    partner_id = fields.Many2one('res.partner')
    cin_represent = fields.Binary(string='CIN', attachment=True)


class viseo_document_rib_represent(models.Model):
    _name = 'rib.represent'

    partner_id = fields.Many2one('res.partner')
    rib_represent = fields.Binary(string='RIB', attachment=True)

class viseo_document_cr_represent(models.Model):
    _name = 'cr.represent'

    partner_id = fields.Many2one('res.partner')
    cr_represent = fields.Binary(string='Cértificat de résidence', attachment=True)

class RibDoc(models.Model):
    _name = 'rib.document'

    partner_id = fields.Many2one('res.partner')
    rib_document = fields.Binary(string='Document RIB', attachment=True)

class CinWizard(models.TransientModel):
    _name = 'cin.wizard'

    wizard_id = fields.Many2one('add_doc_partner.wizard')
    cin_represent = fields.Binary(string='CIN représentant', attachment=True)

    # @api.model
    # def create(self, vals):
    #     res = super(CinWizard, self).create(vals)
    #     res._process_pending_operations()
    #     return res
    #
    # def write(self, vals):
    #     res = super(CinWizard, self).write(vals)
    #     self._process_pending_operations()
    #     return res
    #
    # def _process_pending_operations(self):
    #     # Force processing of pending operations
    #     self.wizard_id.flush()
    #     self.wizard_id.cin_represent.invalidate_cache()

class RibWizard(models.TransientModel):
    _name = 'rib.wizard'

    wizard_id = fields.Many2one('add_doc_partner.wizard')
    rib_represent = fields.Binary(string='RIB représentant', attachment=True)

class CrWizard(models.TransientModel):
    _name = 'cr.wizard'

    wizard_id = fields.Many2one('add_doc_partner.wizard')
    cr_represent = fields.Binary(string='Résidence représentant', attachment=True)

class RibWizardDoc(models.TransientModel):
    _name = 'rib.document.wizard'

    wizard_id = fields.Many2one('add_doc_partner.wizard')
    rib_document = fields.Binary(string='Document RIB', attachment=True)