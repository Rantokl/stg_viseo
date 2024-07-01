from odoo import fields, models, api

class Move(models.Model):
    _inherit = 'account.move'

    def button_draft(self):
        if bool(self.line_ids):
            move_line_ids = self.line_ids.filtered_domain([('exclude_from_invoice_tab', '!=', True)])
            #get off marked ifrs or analytic
            for line in move_line_ids:
                line.write({'ifrs_generated' : False, 'analytic_generated' : False})
            # Delete all related ifrs and analytic when clicking to draft
            ifrs_ids = self.env['ifrs.move.line'].search([('move_id', 'in', move_line_ids.ids)])
            for ifrs in ifrs_ids:
                ifrs.sudo().unlink()
            analytics_ids = self.env['analytic.move.line'].search([('move_id', 'in', move_line_ids.ids)])
            for anal in analytics_ids:
                anal.sudo().unlink()
        res = super(Move, self).button_draft()
        return res


class Line(models.Model):
    _inherit = 'account.move.line'

    ifrs_generated = fields.Boolean(default=False)
    analytic_generated = fields.Boolean(default=False)
    viseo_analytic_line_ids = fields.One2many('analytic.move.line', 'move_id', string='Ecriture analytique')
    ifrs_line_ids = fields.One2many('ifrs.move.line', 'move_id', string='Ecritures ifrs')

    def generate_ifrs_analytic_line(self):
        # date =
        rules_ifrs = self.env['ifrs.rules'].search([('state', '=', 'in_progress')])
        rules_analytique = self.env['analytic.rules'].search([('state', '=', 'in_progress')])
        exclude_name = ['id','rule_id','create_uid','create_date','write_date', 'write_uid', 'display_name', '__last_update', 'company_id']
        date_today = fields.Date.from_string(fields.Date.context_today(self))
        #For IFRS
        account_move_lines1 = self.env['account.move.line'].search([('date', '>=', date_today), ('write_date', '>=', date_today), ('ifrs_generated', '=', False), ('parent_state', '=', 'posted'), ('exclude_from_invoice_tab', '!=', True)])
        ifrs_line = self.env['ifrs.move.line']
        vals_list1 = []
        for line in account_move_lines1:
            for rule_line in rules_ifrs.origin_ids:
                # Lire nom champ et son valeur
                all_fields = rule_line.read()[0]
                # Exclure les valeurs Faux
                analytic_rule_values = {key: value for key, value in all_fields.items() if
                                        value is not False and key not in exclude_name}
                not_null_analytic = list(analytic_rule_values.keys())
                field_values = line.read(fields=not_null_analytic)[0]
                # Exclure la clé ID de la dictionnaire
                field_move_line = {key: value for key, value in field_values.items() if key != 'id'}
                if field_move_line == analytic_rule_values:
                    for ifrs in rules_ifrs.dest_ids:
                        balance = 0
                        if ifrs.percent > 0:
                            balance = line.balance * ifrs.percent / 100
                        vals = {'date': line.date,
                                'move_id': line.id,
                                'partner_id': line.partner_id.id,
                                'section_id': ifrs.section_id.id,
                                'name': ifrs.name or line.name,
                                'account_department_id': ifrs.account_department_id.id or line.account_department_id.id,
                                'account_id': line.account_id.id,
                                'product_id': ifrs.product_id.id or line.product_id.id,
                                'amount': balance,
                                'company_id': line.company_id.id,
                                'is_from_rules' : True
                                }
                        if vals not in vals_list1:
                            vals_list1.append(vals)

                else:
                    vals = {'date': line.date,
                            'move_id': line.id,
                            'partner_id': line.partner_id.id,
                            'section_id': line.account_id.ifrs_id.id,
                            'name': line.name,
                            'account_department_id': line.account_department_id.id,
                            'account_id': line.account_id.id,
                            'product_id': line.product_id.id,
                            'amount': line.balance,
                            'company_id': line.company_id.id,
                            }
                    if vals not in vals_list1:
                        vals_list1.append(vals)
            line.write({'ifrs_generated': True})
        ifrs_line.create(vals_list1)

        #For analytics
        account_move_lines2 = self.env['account.move.line'].search(
            [('write_date', '>=', date_today), ('analytic_generated', '=', False), ('parent_state', '=', 'posted'),
             ('exclude_from_invoice_tab', '!=', True)])
        analytic_move_line = self.env['analytic.move.line']

        # not_null_analytic = []
        vals_list = []
        for line in account_move_lines2:
            if rules_analytique:
                for rule_line in rules_analytique.origin_ids:
                    #Lire nom champ et son valeur
                    all_fields = rule_line.read()[0]
                    #Exclure les valeurs Faux
                    analytic_rule_values = {key: value for key, value in all_fields.items() if value is not False and key not in exclude_name}
                    not_null_analytic = list(analytic_rule_values.keys())
                    field_values = line.read(fields=not_null_analytic)[0]
                    #Exclure la clé ID de la dictionnaire
                    field_move_line = {key: value for key, value in field_values.items() if key != 'id'}
                    if field_move_line == analytic_rule_values:
                        for analytic_line in rules_analytique.dest_ids:
                            balance = 0
                            if analytic_line.percent > 0:
                                balance = line.balance * analytic_line.percent / 100
                            vals = {'date': line.date,
                                    'move_id': line.id,
                                    'partner_id': line.partner_id.id,
                                    'section_id': analytic_line.section_id.id,
                                    'name': analytic_line.name or line.name,
                                    'account_department_id': analytic_line.account_department_id.id or line.account_department_id.id,
                                    'account_id': line.account_id.id,
                                    'product_id': analytic_line.product_id.id or line.product_id.id,
                                    'amount': balance,
                                    'company_id': line.company_id.id,
                                    'is_from_rules': True
                                    }
                            if vals not in vals_list:
                                vals_list.append(vals)

            else:
                vals = {'date': line.date,
                        'move_id': line.id,
                        'partner_id': line.partner_id.id,
                        'name': line.name,
                        'account_department_id': line.account_department_id.id,
                        'account_id': line.account_id.id,
                        'product_id': line.product_id.id,
                        'amount': line.balance,
                        'company_id': line.company_id.id,
                        }
                if vals not in vals_list:
                    vals_list.append(vals)
            line.write({'analytic_generated': True})
        analytic_move_line.create(vals_list)

    #RECUPeration donnée
    def dispatch_line_ifrs_anaytic(self, account_move_lines):
        for line in account_move_lines:
            line.generate_ifrs_analytic_line_data()
            # vals = { 'date' : line.date,
            #         'move_id' : line.id,
            #         'partner_id' : line.partner_id.id,
            #         'name': line.name,
            #         'account_department_id': line.account_department_id.id,
            #         'account_id': line.account_id.id,
            #         'amount' : line.balance,
            #         'company_id': line.company_id.id,
            # }
            # line.write({'ifrs_generated': True})
            #
            # self.env['ifrs.move.line'].create(vals)

        for line in account_move_lines:
            vals = {'date': line.date,
                    'move_id': line.id,
                    'partner_id': line.partner_id.id,
                    'name': line.name,
                    'account_department_id': line.account_department_id.id,
                    'account_id': line.account_id.id,
                    'product_id': line.product_id.id,
                    'amount': line.balance,
                    'company_id': line.company_id.id,
                    }
            line.write({'analytic_generated': True})

            self.env['analytic.move.line'].create(vals)

    def generate_ifrs_analytic_line_data(self):
        rules_ifrs = self.env['ifrs.rules'].search([('state', '=', 'in_progress')])
        rules_analytique = self.env['analytic.rules'].search([('state', '=', 'in_progress')])
        exclude_name = ['id','rule_id','create_uid','create_date','write_date', 'write_uid', 'display_name', '__last_update', 'company_id']
        date_today = fields.Date.from_string(fields.Date.context_today(self))
        #For IFRS
        # account_move_lines1 = self.env['account.move.line'].search([('write_date', '>=', date_today), ('ifrs_generated', '=', False), ('parent_state', '=', 'posted'), ('exclude_from_invoice_tab', '!=', True)])
        ifrs_line = self.env['ifrs.move.line']
        vals_list1 = []
        for line in self:
            for rule_line in rules_ifrs.origin_ids:
                # Lire nom champ et son valeur
                all_fields = rule_line.read()[0]
                # Exclure les valeurs Faux
                analytic_rule_values = {key: value for key, value in all_fields.items() if
                                        value is not False and key not in exclude_name}
                not_null_analytic = list(analytic_rule_values.keys())
                field_values = line.read(fields=not_null_analytic)[0]
                # Exclure la clé ID de la dictionnaire
                field_move_line = {key: value for key, value in field_values.items() if key != 'id'}
                if field_move_line == analytic_rule_values:
                    for ifrs in rules_ifrs.dest_ids:
                        balance = 0
                        if ifrs.percent > 0:
                            balance = line.balance * ifrs.percent / 100
                        vals = {'date': line.date,
                                'move_id': line.id,
                                'partner_id': line.partner_id.id,
                                'section_id': ifrs.section_id.id,
                                'name': ifrs.name or line.name,
                                'account_department_id': ifrs.account_department_id.id or line.account_department_id.id,
                                'account_id': line.account_id.id,
                                'product_id': ifrs.product_id.id or line.product_id.id,
                                'amount': balance,
                                'company_id': line.company_id.id,
                                'is_from_rules' : True
                                }
                        if vals not in vals_list1:
                            vals_list1.append(vals)

                else:
                    vals = {'date': line.date,
                            'move_id': line.id,
                            'partner_id': line.partner_id.id,
                            'section_id': line.account_id.ifrs_id.id,
                            'name': line.name,
                            'account_department_id': line.account_department_id.id,
                            'account_id': line.account_id.id,
                            'product_id': line.product_id.id,
                            'amount': line.balance,
                            'company_id': line.company_id.id,
                            }
                    if vals not in vals_list1:
                        vals_list1.append(vals)
            line.write({'ifrs_generated': True})
        ifrs_line.create(vals_list1)

        #For analytics
        # account_move_lines2 = self.env['account.move.line'].search(
        #     [('write_date', '>=', date_today), ('analytic_generated', '=', False), ('parent_state', '=', 'posted'),
        #      ('exclude_from_invoice_tab', '!=', True)])
        analytic_move_line = self.env['analytic.move.line']

        # not_null_analytic = []
        vals_list = []
        for line in self:
            if rules_analytique:
                for rule_line in rules_analytique.origin_ids:
                    #Lire nom champ et son valeur
                    all_fields = rule_line.read()[0]
                    #Exclure les valeurs Faux
                    analytic_rule_values = {key: value for key, value in all_fields.items() if value is not False and key not in exclude_name}
                    not_null_analytic = list(analytic_rule_values.keys())
                    field_values = line.read(fields=not_null_analytic)[0]
                    #Exclure la clé ID de la dictionnaire
                    field_move_line = {key: value for key, value in field_values.items() if key != 'id'}
                    if field_move_line == analytic_rule_values:
                        for analytic_line in rules_analytique.dest_ids:
                            balance = 0
                            if analytic_line.percent > 0:
                                balance = line.balance * analytic_line.percent / 100
                            vals = {'date': line.date,
                                    'move_id': line.id,
                                    'partner_id': line.partner_id.id,
                                    'section_id': analytic_line.section_id.id,
                                    'name': analytic_line.name or line.name,
                                    'account_department_id': analytic_line.account_department_id.id or line.account_department_id.id,
                                    'account_id': line.account_id.id,
                                    'product_id': analytic_line.product_id.id or line.product_id.id,
                                    'amount': balance,
                                    'company_id': line.company_id.id,
                                    'is_from_rules': True
                                    }
                            if vals not in vals_list:
                                vals_list.append(vals)

            else:
                vals = {'date': line.date,
                        'move_id': line.id,
                        'partner_id': line.partner_id.id,
                        'name': line.name,
                        'account_department_id': line.account_department_id.id,
                        'account_id': line.account_id.id,
                        'product_id': line.product_id.id,
                        'amount': line.balance,
                        'company_id': line.company_id.id,
                        }
                if vals not in vals_list:
                    vals_list.append(vals)
            line.write({'analytic_generated': True})
        analytic_move_line.create(vals_list)