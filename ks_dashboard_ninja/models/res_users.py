# -*- coding: utf-8 -*-


from odoo import models,api,fields, _


class User(models.Model):

    _inherit = "res.users"

       
    dashboard_action_domain = fields.Many2many('ir.actions.actions',string='Action Dashboard',compute = "_get_dashboard_domain")

    
    def _get_dashboard_domain(self):
        for rec in self:
            menus = self.env['ks_dashboard_ninja.board'].search([]).filtered(lambda l : rec in l.ks_dashboard_user_access).mapped('ks_dashboard_menu_name')
            action_names = [menu+' Action' for menu in menus]
            rec.dashboard_action_domain  = self.env['ir.actions.actions'].search([('name','in',action_names),('type','=','ir.actions.client')]).ids

