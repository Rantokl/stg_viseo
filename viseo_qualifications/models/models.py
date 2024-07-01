from odoo import models, fields, api


class viseo_qualifications(models.Model):
    _inherit = 'hr.employee.qualification'


    name = fields.Many2one('qual.type',string='Qualification', help='Explication sur le nom des compétences')
    request_level = fields.Char(string='Niveau réquis', help="Niveau réquis pour les compétences")
    specialitee = fields.Char(string='Spécialité')
    type = fields.Selection([('technique', 'Technique'),('general', 'Générale')],default='general', string='Type')
    note = fields.Text(string='Note')
    # name_sequence=fields.Char(string='Order Sequence',readonly='True',index=True, default="Nouveau")
    skills_code = fields.Char(string='Code compétence', required='True')
    eval_employee = fields.Char(string='Evaluation', help="Expliication sur le champs evaluation de l'employee")

    # =======================================Pour les séquences======================================================================
    # @api.model
    # def create(self, vals):
    #     vals['name_sequence'] = self.env['ir.sequence'].next_by_code('hr.employee.qualification.sequence') or '/'
    #     vals['name_sequence'] = f"{vals['name_sequence']}"
    #     result= super(viseo_qualifications, self).create(vals)
    #     return result
    # ===============================================================================================================================