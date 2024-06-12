from odoo import models, fields, api,exceptions
import xlsxwriter
import base64, tempfile
from io import BytesIO
import numpy as np
from datetime import datetime, time
import pytz
import pandas as pd
from datetime import timedelta
from dateutil.relativedelta import relativedelta

class ViseoRepairKpi(models.Model):
    _inherit = 'fleet.vehicle.log.services'

    ok_nok=fields.Selection([('ok','OK'),('nok','NOK')])

    def action_operations_done(self):
        if self.date_forecast <= datetime.now():
            if self.date_forecast > self.time_user_operation_ok:
                self.ok_nok='ok'
            else :
                self.ok_nok='nok'
        else:
            self.ok_nok= None    
                

class WizardReportViseoSav(models.TransientModel):
    _name = 'report_kpi_sav.wizard'

    du = fields.Date(string='Début du RMA :')
    au = fields.Date(string="Jusqu'à :")
    report = fields.Binary('Rapport kpi SAV',filters='.xlsx', readonly=True)
    name = fields.Char(string="File name", size=64)

    def get_data(self):
        # Construction du domaine pour la recherche
        if self.du <= self.au:
            domain = [('create_date', '>=', self.du), ('create_date', '<=', self.au)]

            # Récupération des champs nécessaires dans'sale.order'
            rma_request = self.env['fleet.vehicle.log.services'].search(domain).read(['name2', 'create_date', 'create_uid','date_forecast','time_user_operation_ok','ok_nok'])
            
            # Initialisation de la liste pour stocker les données
            rma_requests_data = []

            # Boucle sur les enregistrements lus
            for request in rma_request:
                # Créer un dictionnaire pour stocker les données de chaque commande
                rma_request_data = {}

                # Vérifier et ajouter chaque champ au dictionnaire
                if request['name2']:
                    rma_request_data['ref_rma'] = request['name2']
                else:
                    rma_request_data['ref_rma'] = None

                if request['create_date']:
                    rma_request_data['date'] = request['create_date']
                else:
                    rma_request_data['date'] = None

                if request['create_uid']:
                    create_uid_record = self.env['res.users'].browse(request['create_uid'][0])
                    if create_uid_record:
                        rma_request_data['responsable'] = create_uid_record.name
                else:
                    rma_request_data['responsable'] = None

                if request['date_forecast']:
                    rma_request_data['date_previsionelle'] = request['date_forecast']
                else:
                    rma_request_data['date_previsionelle'] = None

                if request['time_user_operation_ok']:
                    rma_request_data['date_cloture'] = request['time_user_operation_ok']
                else:
                    rma_request_data['date_cloture'] = None

                if request['ok_nok']:
                    rma_request_data['ok_nok'] = request['ok_nok']
                else:
                    rma_request_data['ok_nok'] = None


                # Ajouter le dictionnaire de données à la liste des commandes
                rma_requests_data.append(rma_request_data)
            df = pd.DataFrame(rma_requests_data)
            # Conversion du dictionnaire en DataFrame
            if not df.empty :
                return df
            else:
                raise exceptions.UserError(f"Il n'y a pas de données entre {self.du} et {self.au}")
        else :
            raise exceptions.UserError("La date de début doit être antérieure à la date de fin!")

 #------------------------ Ajouter 3 heures à la date de demande-------------------------
    def add_3_hours(self, date):
        date += timedelta(hours=3)
        return date

    def get_report_kpi_sav_xlsx(self):

        df = self.get_data()
        file_name = 'Rapport kpi SAV.xlsx'
        tmpdir = tempfile.mkdtemp()
        tmpdir = tmpdir.rstrip('/')
        workbook = xlsxwriter.Workbook("%s/%s" % (tmpdir, file_name))
        sheet = workbook.add_worksheet()
        sheet.set_default_row(15)

        date_format = workbook.add_format({'num_format': 'dd/mm/yyyy hh:mm:ss',
                                   'align': 'center',
                                   'valign': 'vcenter'})

        header_format = workbook.add_format({
                    'border': 1,  # Ajouter une bordure
                    'bold': True,  # Mettre en gras
                    'align': 'center',  # Centrer le texte
                    'valign': 'vcenter' , # Centrer le texte verticalement
                    'bg_color':'#0000fe',
                    'color':'#ffec06'
                })
        
        header_resume_format= workbook.add_format({
                    'border': 1,  # Ajouter une bordure
                    # 'bold': True,  # Mettre en gras
                    'align': 'center',  # Centrer le texte
                    'valign': 'vcenter' , # Centrer le texte verticalement
                    'bg_color': '#219ebc',
                    'color':'#e9c46a'
                })

        body_format= workbook.add_format({
                    'align': 'center',  # Centrer le texte
                    'valign': 'vcenter', # Centrer le texte verticalement
                })
        porcent_format = workbook.add_format({
                    #'color': '#ffffff',
                    'border': 1,  # Ajouter une bordure
                    'bold': True,  # Mettre en gras
                    'align': 'center',  # Centrer le texte
                    'valign': 'vcenter',  # Centrer le texte verticalement
                    'bg_color': '#f3d8c7'
                    
                })

        # Ajuster la largeur des colonnes
        column_widths = [20, 20, 50, 25, 20, 12] 
        for col, width in enumerate(column_widths):
            sheet.set_column(col, col, width) 
        sheet.set_row(0, 40)  

        # En-têtes
        headers = ['REF RMA','DATE', 'RESPONSABLE', 'DATE PREVISIONNELLE', 'DATE DE CLOTURE','ok / Nok']
        for col, header in enumerate(headers):
            sheet.write(0, col, header,header_format)

        row = 1

        count_ok=0
        count_nok=0
        count_ok_per_month=0
        count_nok_per_month=0
        resume_month=[]
        resume_taux_ok_per_month=[]

        df['nom_mois'] = df['date'].dt.strftime('%B')
        month_filter=df['nom_mois'].unique()
        df['ok_nok'] = df['ok_nok'].replace({False: None})

        for month in month_filter:
            count_ok_per_month=0
            count_nok_per_month=0
            for index, date in enumerate(df['date']):
                if month==df['nom_mois'].iloc[index]:
                    if pd.notnull(df['date_previsionelle'].iloc[index]) or pd.notnull(df['date_cloture'].iloc[index]):
                        sheet.write(row, 0, df['ref_rma'].iloc[index])
                        if pd.notnull(df['date'].iloc[index]):
                            date=self.add_3_hours(df['date'].iloc[index])
                            sheet.write(row, 1, date, date_format)
                        sheet.write(row, 2, df['responsable'].iloc[index])
                        if pd.notnull(df['date_previsionelle'].iloc[index]):
                            date_prev=self.add_3_hours(df['date_previsionelle'].iloc[index])
                            sheet.write(row, 3, date_prev, date_format)
                        if pd.notnull(df['date_cloture'].iloc[index]):
                            date_clot=self.add_3_hours(df['date_cloture'].iloc[index])
                            sheet.write(row, 4, date_clot, date_format)

                    #================================= OK NOK DANS LA BASE=========================================
                        # sheet.write(row, 5, df['ok_nok'].iloc[index], body_format)
                        # if df['ok_nok'].iloc[index]=='ok':
                        #     count_ok+=1
                    #=================================OK NOK DANS L'EXCEL=========================================
                        if pd.notnull(df['date_previsionelle'].iloc[index]) and pd.notnull(df['date_cloture'].iloc[index]):
                            if df['date_previsionelle'].iloc[index] >= df['date_cloture'].iloc[index]:
                                sheet.write(row, 5, 'ok', body_format)
                                count_ok+=1
                                count_ok_per_month+=1
                            else :
                                sheet.write(row, 5, 'nok', body_format)
                                count_nok+=1
                                count_nok_per_month+=1
                        
                        elif pd.notnull(df['date_previsionelle'].iloc[index]) and pd.isnull(df['date_cloture'].iloc[index]):
                            if datetime.now() <= df['date_previsionelle'].iloc[index]:   
                                sheet.write(row, 5, '', body_format)
                            else :
                                sheet.write(row, 5, 'nok', body_format)
                                count_nok+=1
                                count_nok_per_month+=1

                        elif pd.isnull(df['date_previsionelle'].iloc[index]) and pd.notnull(df['date_cloture'].iloc[index]):
                            sheet.write(row, 5, 'nok', body_format)
                            count_nok+=1
                            count_nok_per_month+=1
                        # else :
                        #     sheet.write(row, 5, 'nok', body_format)
                        #     count_nok+=1
                        row += 1

            if count_nok_per_month!=0:
                pourcentage_ok=(count_ok_per_month / count_nok_per_month) * 100
                resume_taux_ok_per_month.append("{:.2f}%".format(pourcentage_ok))
                resume_month.append(month)
            elif count_ok_per_month!=0 and count_nok_per_month==0:
                resume_taux_ok_per_month.append("{:.2f}%".format(100))

        #  # ==========================================ENTETE DE RESUME================================================================================================= 
        # headers_resume=[]
        # for month in resume_month:
        #     headers_resume.append(month)
        # for col, headers_resume in enumerate(headers_resume):
        #     sheet.write(row+2, col+2, headers_resume,header_resume_format)
        # sheet.set_row(row+2, 30)  # Hauteur de la première ligne à 10 (en pixels)
        #  # ==========================================================================================================================================================
        # col_resume=2
        # sheet.write(row+3, 1,'Pourcentage "ok"',header_resume_format)
        # for index in range(0,len(resume_taux_ok_per_month)):
        #     sheet.write(row+3, col_resume,resume_taux_ok_per_month[index] ,workbook.add_format({'align': 'center', 'valign': 'vcenter','border': 1}))
        #     # sheet.write(row_resume, 2,resume_count_ok_dep[index] )
        #     # sheet.write(row_resume, 3,resume_len_dep[index] )
        #     col_resume+=1
        # ==========================================ENTETE DE RESUME================================================================================================= 
        sheet.set_row(row+2, 30)  # Hauteur de la première ligne à 10 (en pixels)
         # ==========================================================================================================================================================
        row_resume=row+3
        sheet.write(row+2, 2,'Pourcentage "ok"',header_resume_format)
        sheet.write(row+2, 1,'Mois',header_resume_format)
        for index in range(0,len(resume_taux_ok_per_month)):
            sheet.set_row(row_resume, 30)
            sheet.write(row_resume, 1,resume_month[index] ,workbook.add_format({'align': 'center', 'valign': 'vcenter','border': 1}))
            sheet.write(row_resume, 2,resume_taux_ok_per_month[index] ,workbook.add_format({'align': 'center', 'valign': 'vcenter','border': 1}))
            # sheet.write(row_resume, 2,resume_count_ok_dep[index] )
            # sheet.write(row_resume, 3,resume_len_dep[index] )
            row_resume+=1

        # sheet.set_row(row+2, 40)
        # if count_ok and count_nok:
        #     print(f'ok {count_ok} , nok {count_nok}')
        #     total_pourcentage_ok = (count_ok / count_nok) * 100
        #     sheet.write(row+2, 2, "Total Pourcentage Ok:",header_resume_format)
        #     sheet.write(row+2, 3, "{:.2f}%".format(total_pourcentage_ok),porcent_format)
        # else:
        #     sheet.write(row+2, 2, "Total Pourcentage Ok:",header_resume_format)
        #     sheet.write(row+2, 3, "0.00%",porcent_format)
        
        # row_resume=row+3
        # for index in range(0,len(resume_dep)):
        #     sheet.write(row_resume, 2,resume_dep[index],workbook.add_format({'border': 1} ))
        #     sheet.write(row_resume, 3,resume_porcentage_dep[index] ,workbook.add_format({'align': 'center', 'valign': 'vcenter','border': 1}))
        #     # sheet.write(row_resume, 2,resume_count_ok_dep[index] )
        #     # sheet.write(row_resume, 3,resume_len_dep[index] )
        #     row_resume+=1

        # if count_ok:
        #     total_pourcentage_ok = (count_ok / (row-1)) * 100
        #     sheet.write(row_resume+2, 2, "Total Pourcentage Ok:")
        #     sheet.write(row_resume+2, 3, "{:.2f}%".format(total_pourcentage_ok))
        # else:
        #     sheet.write(row_resume+2, 2, "Total Pourcentage Ok:")
        #     sheet.write(row_resume+2, 3, "0.00%")
        # #     sheet.write(row+2, 3, f"Nombre Ok total")
        # #     sheet.write(row+2, 4, count_ok)
        # #     sheet.write(row+3, 3, f"Nombre total vente")
        # #     sheet.write(row+3, 4, (row-1))
        
        # if delais:
        #     moyenne = np.mean(delais)
        #     # Convertir la moyenne en jours, heures, minutes et secondes
        #     moyenne_jours, moyenne_heures = divmod(moyenne // 3600, 24)
        #     moyenne_minutes, moyenne_secondes = divmod(moyenne % 3600, 60)
        #     # Formatage de la moyenne en "jj:hh:mm:ss"
        #     moyenne_format = "{:02}:{:02}:{:02}:{:02}".format(int(moyenne_jours), int(moyenne_heures), int(moyenne_minutes), int(moyenne_secondes))

        #     # Ajouter la moyenne à la feuille de calcul
        #     sheet.write(row_resume+3, 2, "Moyenne des délais:")
        #     sheet.write(row_resume+3, 3, moyenne_format) 


        workbook.close()

        # ================================================WRITE EXCEL========================================================================================
        with open("%s/%s" % (tmpdir, file_name), "rb") as file:
            out = base64.b64encode(file.read())
            self.write({'report': out, 'name': f'Rapport kpi SAV du {self.du} au {self.au}.xlsx'})

        # ================================================WIZARD RETURN=====================================================================================
        return{
            'type': 'ir.actions.act_window',
            'res_model': 'report_kpi_sav.wizard',
            'view_mode': 'form',
            'res_id': self.id,
            'views': [(False, 'form')],
            'target': 'new',
            'name': 'Rapport KPI SAV'
        }