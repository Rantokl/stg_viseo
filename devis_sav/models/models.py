# -*- coding: utf-8 -*-
import base64
import datetime
import tempfile
import psycopg2
from odoo import models, fields, api
from odoo.http import request
from odoo.tools import config, human_size, ustr, html_escape
import os
import logging
from . import database

_logger = logging.getLogger(__name__)

class devis_sav(models.Model):
    _name = 'type.devis.sav'
#     _description = 'devis_sav.devis_sav'
    name = fields.Char('Type de devis')
    #resp_id = fields.Many2one('res.users', 'Responsable(s)', required=True)
#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100


class SaleOrderPDFView(models.TransientModel):
    _name = 'sale.order.pdf.view'
    _description = 'Sale Order PDF View'
    _inherit='ir.attachment'
    name = fields.Char('Devis')
    sale_order_id= fields.Many2one('sale.order', 'Devis')
    ir_attach = fields.Many2one('ir.attachment', 'Fichier')
    quotation_pdf = fields.Binary(string='Devis PDF', compute = 'take_pdf',related='ir_attach.datas', default=lambda self : self.ir_attach.datas)
    
    
    datas = fields.Binary(string='File Content', compute='_compute_datas', inverse='_inverse_datas')
    
    #@api.model
    def take_pdf(self):
        pdf = self.env['ir.attachement'].search(['id','=','ir_attach.id'])
        return pdf.datas
   


class devis_pdf_sav(models.Model):
    _inherit= 'sale.order'
    report = fields.Binary('Devis',
                           filters='.pdf', readonly=True)
    name1 = fields.Char('File Name', size=32)
    test=fields.Char("Test")
    
    def generate_and_view_quotation_pdf(self):
        # Utilisez la méthode `print` pour générer le devis au format PDF
        pdf_data = self.with_context(discard_logo_check=True).print_quotation()

        if pdf_data:
            # Créez un enregistrement du modèle personnalisé avec le devis PDF
            pdf_view = self.env['sale.order.pdf.view'].create({'quotation_pdf': pdf_data})

            # Ouvrez la vue personnalisée
            return {
               
                'res_id': pdf_view.id,
                'type':'ir.actions.act_window',
                'res_model':'sale.order.pdf.view',
                'view_mode':'form',
                'res_id':self.id,
                'views':[(False,'form')],
                'target':'new',
                
            }
        else:
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': 'Erreur',
                    'message': 'La génération du PDF du devis a échoué.',
                    'type': 'danger',
                }
            }
    
    # @api.model
    def export_pdf(self):
        file_name = '{}.pdf'.format(self.name)
        tmpdir=tempfile.mkdtemp()
        tmpdir=tmpdir.rstrip('/')
        
        sale_order = self.id

        if sale_order:
            # Générez un fichier PDF à partir de la vue du devis
            report, _ = request.env.ref('sale.action_report_saleorder').sudo().render_qweb_pdf([sale_order])
            #report = self.env['ir.actions.report']._render_qweb_pdf("sale.action_report_saleorder", self.id)
            #report = request.env.ref('sale.report_saleorder', False)
            #pdf_data = report.render_qweb_pdf(sale_order)
            
            # Créez un enregistrement d'attachement avec le PDF
            attachment = self.env['ir.attachment'].create({
                'name': '{}.pdf'.format(self.name),
                'datas': base64.b64encode(report),
                'res_model': 'sale.order',
                'res_id': sale_order,
                'store_fname': '{}.pdf'.format(self.name),
                'type':'binary',
                'mimetype': 'application/x-pdf'
            })
        
            
        # with open("%s/%s" % (tmpdir,file_name), "rb") as file:
        #     out = base64.b64encode(file.read())
        #     self.write({
        #         'report':out,
        #         'name':'{}.pdf'.format(self.name)
        #     })

       # Utilisez la méthode `print` pour générer le devis au format PDF
        #pdf_data = self.with_context(discard_logo_check=True).print_quotation()
        ctx = dict(
            sale_order_id=sale_order,
            quotation_pdf=report,
        )
        print(report)
        self.write({'report':report})
        _report = self.report
        print(_report)
        if report:
            # Créez un enregistrement du modèle personnalisé avec le devis PDF
            #pdf_view = self.env['sale.order'].create({'report': pdf_data})

            # Ouvrez la vue personnalisée
            return {
               
                
                'type':'ir.actions.act_window',
                'res_model':'sale.order.pdf.view',
                'view_mode':'form',
                # 'views':[(False,'form')],
                'target':'new',
                'context':{'default_sale_order_id' : sale_order,
                           'default_ir_attach':attachment.id,
                           'default_name':attachment.name,
                           'default_quotation_pdf':_report},
                
            }
        else:
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': 'Erreur',
                    'message': 'La génération du PDF du devis a échoué.',
                    'type': 'danger',
                }
            }
    
    
class DemandeDevis(models.Model):
    _name = 'sale.order.demand'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Demande de devis'


    customer_id = fields.Many2one('res.partner', string="Client", related="customer_vehicle_id.driver_id")
    customer_vehicle_id = fields.Many2one('fleet.vehicle', 'Vehicules')
    type_devis = fields.Many2one('type.devis.sav', 'Type de devis')
    date_devis = fields.Date("Date du demande")
    devis_id = fields.Integer()
    number_sale = fields.Integer(default=0)

    def check_devis_apk(self):
        curs, connex = database.dbconnex(self)
        curs.execute("""
                        SELECT  id, details, owner_id, type_devis_id, vehicle_id, date_devis 
                        FROM public."viseoApi_devis" where CAST(date_devis as DATE) = CAST(%s AS DATE)
        """,(datetime.date.today(),))
        devis = curs.fetchall()

        for row in devis:

            existing_record = self.env['sale.order.demand'].search([('devis_id', '=', row[0])])
            if existing_record:
                print("pass")
                continue

            records = {
                'devis_id': row[0],
                'customer_id': row[2],
                'type_devis': row[3],
                'customer_vehicle_id': row[4],
                'date_devis': row[5]
            }

            devis = self.env['sale.order.demand'].create(records)
            if devis:
                print('records create succeffully....')
    # def open_sale_order_demand(self):
    #     print('Test .......................')
    #     self.ensure_one()
    #     print('Test .......................')
    #     return {
    #         'type': 'ir.actions.act_window',
    #         'name': 'Demande(s) de devis',
    #         'view_mode': 'tree',
    #         'res_model': 'sale.order.demand',
    #         'domain': [('customer_vehicle_id', '=', self.id)],
    #         'context': {'default_customer_vehicle_id': self.id}
    #     }






class OpenSaleOrderDemand(models.Model):
    _inherit = 'fleet.vehicle'


    def open_sale_order_demand(self):

        self.ensure_one()

        return {
            'type': 'ir.actions.act_window',
            'name': 'Demande(s) de devis',
            'view_mode': 'tree,form',
            'res_model': 'sale.order.demand',
            'domain': [('customer_vehicle_id', '=', self.id)],
            'context': {'default_customer_vehicle_id': self.id}
        }