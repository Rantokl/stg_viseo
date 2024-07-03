# -*- coding: utf-8 -*-
import json

from odoo import models, fields, api
from odoo.exceptions import UserError


class viseo_analytic(models.Model):
    _name = 'viseo_analytic.viseo_analytic'
    #     _description = 'viseo_analytic.viseo_analytic'
    # _inherit = 'account.move'
    name = fields.Char(default='Nouveau')
    start_date = fields.Date('Date de début')
    end_date = fields.Date('Date de fin')
    supplier_id = fields.Many2one('res.partner', 'Fournisseur')
    amount_total = fields.Float('Total')
    percent = fields.Float('Pourcentage')
    departement_id = fields.Many2one('account.department', 'Département')
    report_id = fields.Many2one(
        'ir.actions.report',
        string='Report',
        help='Select the report template for this record.'
    )
    analytic_count = fields.Integer('Analytique', default=0)
    html_content = fields.Html('Contenu html')
    famille = fields.Many2one('analytic.section', string="Famille analytique")
    ecriture = fields.One2many('analytic.move.line', 'analytique_id', string='Ecriture analytique')
    store_analytique = fields.One2many('store.analytique', 'analytique_id')
    department_names = fields.Char(string='Department Names',
                                   default='Department1,Department2,Department3')  # Les noms des départements séparés par des virgules
    department_totals = fields.Integer(string='Total People')  # Total des personnes
    table_data = fields.Text(string='Table Data')
    column_headers = fields.Text('En-têtes des colonnes')
    table_html = fields.Html('Tableau')
    type_repart = fields.Selection(string="Repartir par", selection=[
        ('marque', 'Marque'),
        ('article', 'Article'),
        ('depart', 'Departement'),
        ('sale','Vendeur'),
        ('none', 'Aucun'),
    ], default='none')

    def get_top_salespersons(self, start_date, end_date):
        self.env.cr.execute("""
                   SELECT
                       user_id,
                       SUM(amount_total) as total_sales
                   FROM
                       sale_order
                   WHERE
                       date_order BETWEEN %s AND %s
                       AND state IN ('sale')
                   GROUP BY
                       user_id
                   ORDER BY
                       total_sales DESC
   
               """, (start_date, end_date))

        results = self.env.cr.dictfetchall()
        vals = results[:10]
        # Initialize the total sales variable
        total_sales_sum = 0
        all_salespersons = []
        value_sale = []
        total_sales_sum10 = 0
        all_salespersons10 = []
        value_sale10 = []

        for record in vals:
            user = self.env['res.users'].browse(record['user_id'])
            total_sales_sum10 += record['total_sales']
            all_salespersons10.append(user.name)
            value_sale10.append(record['total_sales'])
        # Format the results and calculate the total sales sum
        for record in results:
            user = self.env['res.users'].browse(record['user_id'])
            total_sales_sum += record['total_sales']
            all_salespersons.append(user.name)
            value_sale.append(record['total_sales'])




        return all_salespersons, total_sales_sum, value_sale,all_salespersons10, total_sales_sum10, value_sale10
        #     {
        #     'top_salespersons': all_salespersons[:10],  # Top 10 salespersons
        #     'total_sales_sum': total_sales_sum,
        #     'all_salespersons': all_salespersons,  # All salespersons
        # }



    def calcul_value_rebrique(self):
        # rubrique = self.env['analytic.section'].search([])

        departements = self.env['account.department'].sudo().search([])
        users = self.env['res.users'].sudo().search([])
        user_dep = []
        tab = []
        for departement in departements:
            user = self.env['res.users'].sudo().search([('account_department_id', '=', departement.id)])
            user = len(user) / len(users)
            user_dep.append(user)
        # ])
        tabData = ['Chiffre affaire', 'COGS', 'Marge brute']
        # Calcul de la somme totale des factures
        rubriques = self.env['analytic.section'].sudo().search([])

        invoices = self.env['analytic.move.line'].sudo().search([
            ('date', '>=', self.start_date),
            ('date', '<=', self.end_date),
            # ('state', '=', 'posted'),  # Inclure uniquement les factures comptabilisées
            ('account_id.code', '=like', '7%')  # Inclure uniquement les factures de vente
        ])
        total_revenue = sum(abs(invoice.amount) for invoice in invoices)

        cogs = self.env['analytic.move.line'].sudo().search([
            ('date', '>=', self.start_date),
            ('date', '<=', self.end_date),
            ('is_cogs', '=', True),
            # ('state', '=', 'posted'),  # Inclure uniquement les factures comptabilisées
            # ('type', '=', 'out_invoice')  # Inclure uniquement les factures de vente
        ])
        total_cogs = sum(cog.amount for cog in cogs)
        val_table = []
        cogs = []
        brute_marge = []
        rubrique = []
        if self.type_repart == 'none':
            departments = self.searchDep('res.company')
            for i in range(len(departments) - 1):
                val_table.append(0)
                cogs.append(0)
                brute_marge.append(0)
            cogs.append(total_cogs)
            val_table.append(total_revenue)

        else:
            if self.type_repart == 'marque':
                departments = self.searchDep('viseo.brand')
                for i in range(len(departments[:11])):
                    val_table.append(0)
                    cogs.append(0)
                    brute_marge.append(0)
                cogs.append(total_cogs)
                val_table.append(total_revenue)
            else:
                if self.type_repart == 'article':
                    departments = self.searchDep('product.template')
                    for i in range(len(departments[:11])):
                        val_table.append(0)
                        cogs.append(0)
                        brute_marge.append(0)
                    cogs.append(total_cogs)
                    val_table.append(total_revenue)
                else:
                    if self.type_repart == 'depart':
                        departments = self.read_depart_group()
                        for i in range(len(departments) - 1):
                            val_table.append(0)
                            cogs.append(0)
                            brute_marge.append(0)
                        cogs.append(total_cogs)
                        val_table.append(total_revenue)
                    else:
                        if self.type_repart == 'sale':
                            departments, total_sales, value_sale,departments10, total_sales10, value_sale10 = self.get_top_salespersons(self.start_date,self.end_date)
                            for i in range(len(departments10)):
                                val_table.append(value_sale10[i])
                                cogs.append(0)
                                brute_marge.append(0)
                            # val_table.append(value_sale)
                            val_table.append(total_sales-total_sales10)
                            cogs.append(total_cogs)
                            val_table.append(total_sales)


        # tab = [[23, 25, 36, 14, 13, 12, 13, 14, ], [23, 25, 36, 14, 13, 12, 13, 14, ],
        #        [23, 25, 36, 14, 13, 12, 13, 14, ]]

        tab.append(val_table)
        tab.append(cogs)
        tab.append(brute_marge)

        for i in rubriques:
            data = i.name

            tabData.append(data)



        resultat = []
        for lettre, chiffres in zip(tabData, tab):
            element_resultat = [lettre] + chiffres
            resultat.append(element_resultat)

        # total_amount = sum(invoice.amount_total for invoice in invoices)
        # for rubrique in rubriques:
        #     invoices = self.env['account.move'].search([
        #         ('partner_id', '=', self.supplier_id.id),
        #         ('invoice_date', '>=', self.start_date),
        #         ('invoice_date', '<=', self.end_date),
        #         ('type', '=', 'in_invoice'),
        #     ])

        return {
            # 'content': tab,
            'famille': resultat
        }

    @api.onchange('table_data')
    def _onchange_table_data(self):
        if self.table_data:
            try:
                table_data = json.loads(self.table_data)
                column_headers = json.loads(self.column_headers)
                return {'value': {'table_data': table_data, 'column_headers': column_headers}}
            except (ValueError, TypeError):
                return {'warning': {
                    'title': "Erreur de données",
                    'message': "Les données de la table sont dans un format incorrect."
                }}
        return {}

    def load_table_data(self):
        try:
            table_data = json.loads(self.table_data)
            column_headers = json.loads(self.column_headers)
        except (ValueError, TypeError):
            table_data = []
            column_headers = []
        return self.env['ir.ui.view'].render_template('viseo_analytic_viseo.custom_html_template', {
            'table_data': table_data,
            'column_headers': column_headers
        })




    def decode_table_data(self):
        return json.loads(self.table_data)

    def decode_column_headers(self):
        return json.loads(self.column_headers)

    # @api.onchange('end_date')
    # def load_table_data(self):
    #     try:
    #         table_data = json.loads(self.table_data)
    #         column_headers = json.loads(self.column_headers)
    #     except (ValueError, TypeError):
    #         table_data = []
    #         column_headers = []
    #     return self.env['ir.ui.view'].render_template('viseo_analytic_viseo.custom_html_template', {
    #         'table_data': table_data,
    #         'column_headers': column_headers
    #     })

    def read_depart_group(self):
        tabData = []
        test = self.env['account.department'].sudo().search([])
        for i in test:
            data = i.name
            tabData.append(data)
        tabData.append('Autres')
        tabData.append('TOTAL')
        # print(tabData)
        return tabData
        # self.env['viseo_analytic.viseo_analytic'].render('viseo_analytic_viseo.analytique_template', docargs)

    def takedata(self):
        print(self.id)
        data = self.env['viseo_analytic.viseo_analytic'].sudo().search([('id', '=', self.id)])
        print('test1', data)
        # return
        return {
            'name2': self.id,
            'name': data.name,
            'value': data.amount_total
        }

    def table_analytic(self):
        print(self.name)
        data = self.env.ref('viseo_analytic_viseo.viseo_analytic_viseo_action_client').read()[0]
        data1 = self.env.ref('viseo_analytic_viseo.viseo_analytic_viseo_action_client').read()
        print(data1)
        return self.env.ref('viseo_analytic_viseo.viseo_analytic_viseo_action_client').read()[0]

    def action_afficher_template(self):
        return {
            'name': 'Affichage du Template',
            'type': 'ir.actions.act_window',
            'res_model': 'viseo.analytique.view',
            'view_mode': 'form',
            'view_id': self.env.ref('viseo_analytic_viseo.view_my_template').id,
            # Remplacez 'my_module.view_my_template' par l'ID de votre vue template
            'target': 'current',
        }

    def openWizard(self):
        self.ensure_one()
        return {

            'type': 'ir.actions.act_window',
            'res_model': 'account.move.line.view',
            'view_mode': 'form',
            'views': [(False, 'form')],
            'target': 'new',

        }

    def searchDep(self, model):
        tabData = []
        test = self.env[model].sudo().search([])
        for i in test:
            data = i.name
            tabData.append(data)
        tabData.append('Autres')
        tabData.append('TOTAL')

        return tabData

    def render_table(self):
        type = self.type_repart
        print(type)
        if self.type_repart == 'none':
            departments = self.searchDep('res.company')
            return {
                'departements': departments
            }
        else:
            if self.type_repart == 'marque':
                departments = self.searchDep('viseo.brand')
                departments = departments[:10]
                departments.append('Autres')
                departments.append('TOTAL')
                return {
                    'departements': departments
                }
            else:
                if self.type_repart == 'article':
                    departments = self.searchDep('product.template')
                    departments = departments[:10]
                    departments.append('Autres')
                    departments.append('TOTAL')
                    return {
                        'departements': departments
                    }
                else:
                    if self.type_repart == 'depart':
                        departments = self.read_depart_group()
                        # print('test', departments)
                        return {
                            'departements': departments
                        }
                    else:
                        if self.type_repart == 'sale':
                            departments, total_sum, value_sale,departments10, total_sales10, value_sale10 = self.get_top_salespersons(self.start_date, self.end_date)
                            # print('test', departments)
                            departments10.append('Autres')
                            departments10.append('TOTAL')
                            return {
                                'departements': departments10
                            }

    @api.model
    def create(self, sequence):
        sequence['name'] = self.env['ir.sequence'].next_by_code('viseo_analytic.viseo_analytic') or '/'

        return super(viseo_analytic, self).create(sequence)

    def action_pivot_view_test(self):
        print('TEst')
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Analytique viseo',
            'view_mode': 'pivot',
            'res_model': 'viseo_analytic.viseo_analytic',
            # 'domain': [('vehicle_id', '=', self.id)],
            # 'context': {'default_driver_company': self.true_driver.id, 'default_driver_other': self.other_driver, 'default_vehicle_id': self.id}
        }

    def read_group_department_ids(self, department, domain, order):
        if self._context.get('restrict_rdv'):
            return department
        all_atelier = department.search(['account_department'], order='name desc')
        print('atelier: ', all_atelier)
        return all_atelier

    @api.onchange('supplier_id')
    def compute_invoice_total(self):
        # Recherche des factures du fournisseur dans la période spécifiée
        invoices = self.env['account.move'].search([
            ('partner_id', '=', self.supplier_id.id),
            ('invoice_date', '>=', self.start_date),
            ('invoice_date', '<=', self.end_date),
            ('type', '=', 'in_invoice'),  # Factures fournisseur
            ('state', '=', 'posted'),  # Factures validées
        ])

        # Calcul de la somme totale des factures
        total_amount = sum(invoice.amount_total for invoice in invoices)

        self.amount_total = total_amount

    @api.onchange('end_date')
    def take_analytique(self):
        ecriture = self.env['analytic.move.line'].search([
            ('date', '>=', self.start_date),
            ('date', '<=', self.end_date),
            ('section_id', '!=', False)
        ])

        results = {}
        for record in ecriture:
            if record.section_id.name in results:
                results[record.section_id.name] += record.amount
            else:
                results[record.section_id.name] = record.amount

        summary_list = [{'rubrique': name, 'total_amount': total_amount} for name, total_amount in results.items()]

        for list in summary_list:
            store = {'name': list['rubrique'],
                     'amount': list['total_amount'],
                     'analytique_id': self.id}

            store_id = self.env['store.analytique'].create(store)

            self.store_analytique = store_id
        self.ecriture = ecriture


class StoreAnalytique(models.Model):
    _name = 'store.analytique'

    name = fields.Char('Rubrique(s)')
    amount = fields.Float('Total')
    analytique_id = fields.Many2one('viseo_analytic.viseo_analytic', 'Analytique')


class viewAnalytique(models.Model):
    _name = 'viseo.analytique.view'
    name = fields.Char(default='Nouveau')
    html_content = fields.Html('Contenu html')


class AccountMoveLineView(models.TransientModel):
    _name = 'account.move.line.view'

    name = fields.Char('Nouveau')
    ecriture = fields.Many2one('account.move.line', "Écriture comptable")


class AnalytiqueFamille(models.Model):
    _name = 'analytic.section'

    name = fields.Char('Famille')

    def calcul_value_rebrique(self):
        # rubrique = self.env['analytic.section'].search([])

        departements = self.env['account.department'].sudo().search([])
        users = self.env['res.users'].sudo().search([])
        user_dep = []

        for departement in departements:
            user = self.env['res.users'].sudo().search([('account_department_id', '=', departement.id)])
            user = len(user) / len(users)
            user_dep.append(user)
        # ])
        tabData = []
        # Calcul de la somme totale des factures
        rubriques = self.env['analytic.section'].sudo().search([])

        tab = [[23, 25, 36, 14, 13, 12, 13, 14, ], [23, 25, 36, 14, 13, 12, 13, 14, ],
               [23, 25, 36, 14, 13, 12, 13, 14, ]]
        for i in rubriques:
            data = i.name

            tabData.append(data)

        resultat = []
        for lettre, chiffres in zip(tabData, tab):
            element_resultat = [lettre] + chiffres
            resultat.append(element_resultat)

        # total_amount = sum(invoice.amount_total for invoice in invoices)
        # for rubrique in rubriques:
        #     invoices = self.env['account.move'].search([
        #         ('partner_id', '=', self.supplier_id.id),
        #         ('invoice_date', '>=', self.start_date),
        #         ('invoice_date', '<=', self.end_date),
        #         ('type', '=', 'in_invoice'),
        #     ])

        return {
            # 'content': tab,
            'famille': resultat
        }


class Analytiquefamille(models.Model):
    _inherit = 'purchase.order'

    famille = fields.Many2one('analytic.section')


class AnalytiqueEcriture(models.Model):
    _inherit = 'analytic.move.line'

    analytique_id = fields.Many2one('viseo_analytic.viseo_analytic', string="analytique_id")



class AddChild(models.TransientModel):
    _name = 'analytic.addchild'


    parents = fields.Char('Parents')
    enfants = fields.Char('Enfants')


    def openWizardChild(self):
        print('OpenWizard_')
        # self.ensure_one()
        return {

            'type': 'ir.actions.act_window',
            'res_model': 'analytic.addchild',
            'view_mode': 'form',
            'view_id':'action_child_wizard',
            'views': [(False, 'form')],
            'target': 'new',

        }


#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
# {
#             'name': 'Somme des factures du fournisseur',
#             'view_type': 'form',
#             'view_mode': 'form',
#             'res_model': 'viseo_analytic.viseo_analytic',
#             'view_id': False,
#             'type': 'ir.actions.act_window',
#             'target': 'new',
#             'context': {'default_start_date': self.start_date,
#                         'default_end_date': self.end_date,
#                         'default_supplier_id': self.supplier_id.id,
#                         'default_total_amount': total_amount,
#                         'amout_total':total_amount
#                         },
#         },
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
