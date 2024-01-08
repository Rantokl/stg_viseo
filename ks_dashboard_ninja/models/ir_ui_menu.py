# -*- coding: utf-8 -*-

from odoo import models,api

class IrUiMenu(models.Model):

    _inherit= "ir.ui.menu"

    @api.returns('self')
    def _filter_visible_menus(self):
        self.clear_caches()
        menu_to_hide_ids = []
        res = super(IrUiMenu,self)._filter_visible_menus()
        current_user= self.env['res.users'].search([('id','=',self._context.get('uid'))])
        if not current_user.has_group('ks_dashboard_ninja.ks_dashboard_ninja_group_manager'):
            menu_dashboards = self.env['ks_dashboard_ninja.board'].search([]).filtered(lambda l : current_user not in l.ks_dashboard_user_access).mapped('ks_dashboard_menu_name')
            if menu_dashboards:
                query = "select id from ir_ui_menu where name in %(names)s"
                self.env.cr.execute(query, {'names': tuple(menu_dashboards)})
                menu_to_hide_ids = [menu['id'] for menu in self.env.cr.dictfetchall()]
                res = res.filtered(lambda menu:menu.id not in menu_to_hide_ids)
            
        return res