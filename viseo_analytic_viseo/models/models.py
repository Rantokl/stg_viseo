# -*- coding: utf-8 -*-

from odoo import models, fields, api


class viseo_analytic(models.Model):
    _name = 'viseo_analytic.viseo_analytic'
#     _description = 'viseo_analytic.viseo_analytic'
    #_inherit = 'account.move'
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
    famille = fields.Many2one('famille.analytique', string="Famille analytique")


    def read_depart_group(self):
        tabData = []
        test = self.env['account.department'].sudo().search([])
        for i in test:
            data = i.name
            tabData.append(data)
        # print(tabData)
        return tabData
        #self.env['viseo_analytic.viseo_analytic'].render('viseo_analytic_viseo.analytique_template', docargs)


    def takedata(self):
        print(self.id)
        data = self.env['viseo_analytic.viseo_analytic'].sudo().search([('id','=',self.id)])
        print('test1',data)
        # return
        return {
            'name2':self.id,
            'name':data.name,
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
            'views':[(False,'form')],
            'target': 'new',
            # 'context': {'default_sale_order_id': sale_order,
            #             'default_ir_attach': attachment.id,
            #             'default_name': attachment.name,
            #             'default_quotation_pdf': _report
            #             },

        }

    def render_table(self):
        departments = self.read_depart_group()
        # print('test', departments)
        return {
            'departements': departments
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
             #'domain': [('vehicle_id', '=', self.id)],
             #'context': {'default_driver_company': self.true_driver.id, 'default_driver_other': self.other_driver, 'default_vehicle_id': self.id}
         }
        
    def read_group_department_ids(self, department, domain, order):
        if self._context.get('restrict_rdv'):
            return department
        all_atelier = department.search(['account_department'], order='name desc')
        print('atelier: ',all_atelier)
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

        
        self.amount_total= total_amount




class viewAnalytique(models.Model):
    _name = 'viseo.analytique.view'
    name = fields.Char(default='Nouveau')
    html_content = fields.Html('Contenu html')



class AccountMoveLineView(models.TransientModel):
    _name = 'account.move.line.view'

    name= fields.Char('Nouveau')
    ecriture = fields.Many2one('account.move.line', "Écriture comptable")

class AnalytiqueFamille(models.Model):
    _name = 'famille.analytique'
    
    
    name = fields.Char('Famille')

    def calcul_value_rebrique(self):
        # invoices = self.env['account.move'].search([
        #     ('partner_id', '=', self.supplier_id.id),
        #     ('invoice_date', '>=', self.start_date),
        #     ('invoice_date', '<=', self.end_date),
        #     ('type', '=', 'in_invoice'),
        # ])
        tabData = []
        # Calcul de la somme totale des factures
        rubriques = self.env['famille.analytique'].sudo().search([])
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
    
    
    famille = fields.Many2one('famille.analytique')
        
   
    
    
    
    
    
    

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

    
        
