from odoo import models, fields, api


class SocialMediaType(models.TransientModel):
    _name = 'social.media.model'
    _description = 'Sélection de Type de Réseau Social'

    social_media_type = fields.Selection([
        ('facebook', 'Facebook'),
        ('twitter', 'Twitter'),
        ('instagram', 'Instagram'),
        ('whatsapp','whatsApp')
    ], string="Type de Réseau Social", required=True)
    description = fields.Char(string="Nom du compte")
    prospect_id = fields.Many2one('prospect.crm')
    crm_id = fields.Many2one('viseo.crm')
