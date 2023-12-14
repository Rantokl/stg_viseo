# -*- coding: utf-8 -*-
import base64
import datetime
import tempfile
import paramiko
import requests
import psycopg2
from odoo import models, fields, api
from odoo.http import request
from odoo.tools import config, human_size, ustr, html_escape
import os
import logging
from . import database

_logger = logging.getLogger(__name__)

def send_notif(title, message,type_notif , customer_id):
	# Remplacez cette URL par l'URL de votre API
	#print(message[0])
	api_url = "http://10.68.132.2:8090/api/v1/send_notification/"

	# Remplacez ces données par le corps de votre requête
	payload = {
		"titre": title,
		"message": message,
		"type_notification_id": type_notif,
		"user_id": customer_id
	}

	# Remplacez ces en-têtes par les en-têtes requis par votre API
	headers = {
		"Content-Type": "application/json",

	}

	try:
		# Effectuer la requête POST
		response = requests.post(api_url, json=payload, headers=headers)

		# Vérifier si la requête a réussi (code 2xx)
		if response.status_code // 100 == 2:
			print("Requête POST réussie!")
		else:
			print(f"Échec de la requête POST. Code d'erreur: {response.status_code}")
			print("Réponse du serveur:", response.text)

	except Exception as e:
		print(f"Une erreur s'est produite: {e}")

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
    # _inherit='ir.attachment'
    name = fields.Char('Devis')
    sale_order_id= fields.Many2one('sale.order', 'Devis')
    ir_attach = fields.Many2one('ir.attachment', 'Fichier')
    quotation_pdf = fields.Binary(string='Devis PDF',filters='.pdf' , compute = 'take_pdf',related='ir_attach.datas', default=lambda self : self.ir_attach.datas)
    
    
    datas = fields.Binary(string='File Content', compute='_compute_datas', inverse='_inverse_datas')
    
    #@api.model
    def take_pdf(self):
        pdf = self.env['ir.attachment'].search(['id','=','ir_attach.id'])
        return pdf.datas

    def test_info(self):
        sale_order_id = self.sale_order_id
        date_devis = self.sale_order_id.demand_devis.date_devis
        pdf_name = sale_order_id.name
        demand_id = sale_order_id.demand_devis.devis_id
        total = sale_order_id.amount_total

        print(date_devis, pdf_name, demand_id, total)

    def save_pdf_to_server(self):
        # Récupérer le fichier PDF depuis le champ binaire
        report = self.quotation_pdf
        pdf_name = self.name
        if report:
            # Décodez le fichier PDF
            #decoded_pdf = report.decode('base64')
            decoded_pdf = base64.b64decode(report)
            #pdf_name = pdf_name+".pdf"
            # Enregistrez le fichier sur le serveur
            #file_name = "nouveau_fichier.pdf"
            tmpdir = tempfile.mkdtemp()
            tmpdir = tmpdir.rstrip('/')
            file_path = tmpdir + '/' + pdf_name
            with open(file_path, 'wb') as file:
                file.write(decoded_pdf)

            # Ajoutez votre logique supplémentaire ici, par exemple, enregistrez le chemin du fichier dans votre modèle
                # Transférer le fichier via SCP
            ssh_host = '10.68.132.2'
            ssh_port = 22
            ssh_user = 'odoodb'
            ssh_password = 'O@00v1$E0'
            ssh_directory = '/data/docker/viseo/static/upload/devis/'  # Le répertoire sur le serveur distant

            transport = paramiko.Transport((ssh_host, ssh_port))
            transport.connect(username=ssh_user, password=ssh_password)

            sftp = paramiko.SFTPClient.from_transport(transport)
            sftp.put(file_path, os.path.join(ssh_directory, pdf_name))

                # Fermez la connexion
            sftp.close()
            transport.close()
            os.remove(file_path)

            sale_order_id = self.sale_order_id
            date_devis = self.sale_order_id.demand_devis.date_devis
            sale_number = sale_order_id.name
            demand_id = sale_order_id.demand_devis.devis_id
            total = sale_order_id.amount_total
            curs, connex = database.dbconnex(self)
            curs.execute("""
                            UPDATE public."viseoApi_devis"
	                        SET numero_devis= %s, prix= %s, pdf= %s, uploaded_at= %s
	                        WHERE id = %s;
            """,(sale_number, total, pdf_name, datetime.datetime.now(),demand_id))
            connex.commit()
            curs.close()
            connex.close()
            sale_order_id.message_post(
                body="Devis envoyé à l'application"
            )
            #date_devis = self.sale_order_id.demand_devis.date_devis
            message = '''Votre devis du {} est prêt'''.format(date_devis)
            send_notif("Devis", message, 2, sale_order_id.partner_id.id)
            print("pdf create successfully!!!!")
            return {'success': True, 'message': 'Fichier PDF enregistré avec succès.'}
        else:
            return {'success': False, 'message': 'Le fichier PDF est vide.'}
   


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
                # 'res_id':self.id,
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
                           'default_quotation_pdf':_report
                           },
                
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

    name = fields.Char(string=f"DD", default="Nouveau")
    customer_id = fields.Many2one('res.partner', string="Client", related="customer_vehicle_id.driver_id")
    customer_vehicle_id = fields.Many2one('fleet.vehicle', 'Vehicules')
    type_devis = fields.Many2one('type.devis.sav', 'Type de devis')
    date_devis = fields.Date("Date du demande")
    devis_id = fields.Integer()
    note = fields.Html(string="Note")
    number_sale = fields.Integer(default=0)

    @api.model
    def create(self, sequence):
        sequence['name'] = self.env['ir.sequence'].next_by_code('sale.order.demand') or '/'
        # place_pont = f"Place: {sequence.get('place_id')}" if sequence['place_id'] else f"Pont: {sequence.get('pont_id')}"
        sequence['name'] = f"{sequence['name']}"
        return super(DemandeDevis, self).create(sequence)

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
            to_suscribe = self.env['res.groups'].search([('name','=','Réception devis')])

            devis = self.env['sale.order.demand'].create(records)
            print(devis.customer_id.name, devis.date_devis)
            ask = devis.message_post(body='''Demande de devis de Mr(s) {} du {}'''.format(devis.customer_id.name, devis.date_devis),
                              subject='Demande de devis de Mr(s) {}'.format(devis.customer_id.name),
                              partner_ids=to_suscribe.users.partner_id.ids)
            devis.message_subscribe(partner_ids=to_suscribe.users.partner_id.ids)
            rdv2 = self.env['mail.mail'].sudo().search([('mail_message_id', '=', ask.id)])
            mail = rdv2.send()
            if devis and mail:
                print('records create succeffully....')



    def devis_apk(self):
        self.ensure_one()
        demand = self.id
        sale_id = self.env['sale.order'].sudo().search([('demand_devis.id','=', demand)])
        if sale_id:
            return {
                     'type': 'ir.actions.act_window',
                     'name': 'Devis',
                     'view_mode': 'form',
                     'res_model': 'sale.order',
                     'res_id': sale_id.id,
                     'context': {'default_partner_id': self.customer_id,
                                 'default_vehicle_ids' : self.customer_vehicle_id},
                     'target': 'current'
                 }
        else:
            return {
                'type': 'ir.actions.act_window',
                'name': 'Devis',
                'view_mode': 'form',
                'res_model': 'sale.order',

                'context': {'default_partner_id': self.customer_id.id,
                            'default_vehicle_ids': self.customer_vehicle_id.ids,
                            'default_demand_devis': self.id},
                'target': 'current'
            }
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

class DevisAPK(models.Model):
    _inherit = 'sale.order'

    demand_devis = fields.Many2one('sale.order.demand', 'Ref demande de devis')






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