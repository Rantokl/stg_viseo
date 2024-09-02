from odoo import models, fields, api

class RepairRules(models.Model):
    _name = "maintenance.repair.rules"
    _description = "Règle sur Bike &amp Tools"
    _inherit = ['portal.mixin', 'mail.thread', 'mail.activity.mixin', 'utm.mixin']

    name = fields.Char("Nom du règle")
    visual_control = fields.Many2many('res.users', 'maint_visual_control_user_rel', 'maint_rule_id', 'maint_user_id',string="Contrôle visuel")
    operation = fields.Many2many('res.users', 'maint_operation_user_rel', 'maint_rule_id', 'maint_user_id', string="Diagnostic")
    automotive = fields.Many2many('res.users', 'maint_automotive_user_rel', 'maint_rule_id', 'maint_user_id', string="Validateur pièces")
    bt_chief = fields.Many2many('res.users', 'chief_bike_rel', 'maint_rule_id', 'maint_user_id', string="Responsables Bike &amp Tools")