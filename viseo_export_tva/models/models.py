
from odoo import models, fields, api, exceptions
import xlsxwriter
import base64
import tempfile
from io import BytesIO
import pandas as pd
from datetime import datetime


class ReportTask(models.Model):
    _inherit = 'account.move.line'

class WizardReportViseoTVA(models.TransientModel):
    _name = 'viseo_export_tva.wizard'

    report = fields.Binary('Rapport viseo TVA', filters='.xlsx', readonly=True)
    name = fields.Char(string="Nom du fichier", size=64)
    du = fields.Date(string='Du :')
    au = fields.Date(string="Jusqu'à :")
    compagnie = fields.Many2one("res.company", string="Société")
     

    def get_data_TVADeductible(self):
        if self.du > self.au:
            raise exceptions.UserError("La date de début ne peut pas être postérieure à la date de fin.")

        domain = [
            ('create_date', '>=', self.du),
            ('create_date', '<=', self.au),
            ('company_id', '=', self.compagnie.id),
            ('is_declared', '=', False),
            ('account_id.code', 'in', ["445610", "445611", "445612", "445613", "445620", "445621", "445622", "445623", "445630"])
            
        ]
        
        report_data = self.env['account.move.line'].sudo().search(domain)


        reports_task = []
        deductible_accounts = {
        "445610": ("300 - TVA déductible sur les biens locaux destinés à la revente", "300 - TVA déductibles / biens locaux destinés à la revente", "B"),
        "445611": ("320 - TVA déductible sur investissements corporels locaux éligibles", "320 - TVA déductibles / investissements corporels locaux éligibles", "I"),
        "445612": ("340 - TVA déductible sur les autres biens locaux", "340 - TVA déductibles / autres biens locaux", "B"),
        "445613": ("350 - TVA déductible sur les services locaux", "350 - TVA déductibles / services locaux", "S"),
        "445620": ("305 - TVA déductible sur les biens importés destinés à la revente", "305 - TVA déductibles / biens importés destinés à la revente", "B"),
        "445621": ("330 - TVA déductible sur investissements corporels importés éligibles", "330 - TVA déductibles / investissements corporels importés éligibles", "I"),
        "445622": ("345 - TVA déductible sur les autres biens importés", "345 - TVA déductibles / autres biens importés", "B"),
        "445623": ("355 - TVA déductible sur les services importés", "355 - TVA déductibles / services importés", "S"),
        "445630": ("355 - TVA déductible sur les services importés", "355 - TVA déductibles / services importés", "S")  
    }
        for line in report_data:
            report_task = {}

            # Obtenez les taxes associées à la ligne de mouvement
            
            if line.account_id.code in deductible_accounts:
        
                report_task['Déductible ou Collectée'] = "D"
            
                report_task['Libellé opération'] = line.name or ''
                report_task['Date facture (jj/mm/aaaa)'] = line.date or ''
                report_task['Référence facture'] = line.move_id.name if line.move_id else ''


                #report_task['Montant TVA'] = abs(line.move_id.amount_by_group[0][1]) if line.move_id and line.move_id.amount_by_group else 0
                report_task['Montant TVA'] = abs(line.debit) or 0

                # Extraire la date de paiement
                payment_date = None
                if line.move_id and line.move_id.payment_ids:
                    payments = line.move_id.payment_ids
                    payment_date = payments[0].payment_date if payments else None
                report_task['Date de paiement (jj/mm/aaaa)'] = payment_date.strftime('%d/%m/%Y') if payment_date else ''

                # Extraire le numéro DAU
                dau = None
                if line.move_id and line.move_id.dau_ids:
                    dau = line.move_id.dau_ids[0].name if line.move_id.dau_ids else None
                report_task['NDAU'] = dau or ''

                # Extraire les codes annexes et les codes déclarations
                code_annexe, code_declaration, nature = deductible_accounts.get(line.account_id.code, ('', '', ''))
                report_task['Code Anex'] = code_annexe
                report_task['Code décl'] = code_declaration
                report_task['Nature'] = nature

                # Extraire les informations du partenaire
                if line.partner_id:
                    partner = line.partner_id
                    country_name = partner.country_id.name.lower() if partner.country_id else ''
                    report_task['Local ou Etranger'] = 'L' if country_name in ['madagascar', 'antananarivo'] else 'E'
                    report_task['Raison sociale'] = partner.name or ''
                    report_task['NIF (10 chiffres avec les 0)'] = partner.nif or ''
                    report_task['Partenaire/Stat'] = partner.stat or ''
                    report_task['Adresse'] = partner.street or ''
                    report_task['Pays du partenaire'] = partner.country_id.name or ''
                else:
                    report_task['Raison sociale'] = ''
                    report_task['NIF (10 chiffres avec les 0)'] = ''
                    report_task['STAT'] = ''
                    report_task['Adresse'] = ''
                    report_task['Local ou Etranger'] = ''

                
                # Calculer le 'Montant HT' en fonction de 'Montant TVA'
                if report_task['Montant TVA']:
                    try:
                        tva_deductible = float(report_task['Montant TVA'])
                        report_task['Montant HT'] = tva_deductible / 0.2
                    except (ValueError, TypeError):
                        report_task['Montant HT'] = 0
                else:
                    report_task['Montant HT'] = 0

                  # En supposant que 'Nature' est un champ supplémentaire, sinon retirez cette ligne
                report_task['Observation'] = ''  # En supposant que 'Observation' est un champ supplémentaire, sinon retirez cette ligne

                # Ajoutez la ligne seulement si le montant TVA est différent de zéro
                if report_task['Montant TVA'] != 0:
                    reports_task.append(report_task)

        df = pd.DataFrame(reports_task)
        if df.empty:
            raise exceptions.UserError(f"Il n'y a pas de données entre {self.du} et {self.au}")

        return df

    #TVA collectée
    def get_data_TVACollectee(self):
        if self.du > self.au:
            raise exceptions.UserError("La date de début ne peut pas être postérieure à la date de fin.")

        domain = [
            ('create_date', '>=', self.du),
            ('create_date', '<=', self.au),
            ('company_id', '=', self.compagnie.id),
            ('is_declared', '=', False),
        ]
        
        report_data = self.env['account.move.line'].sudo().search(domain)

        reports_task = []

        collecte_accounts = {"701200": "B", "702200": "B", "703200": "B", "704200": "S", "706200": "S", "707200": "B", "707102": "",
                            "721100": "B", "722000": "B", "756000": "B", "768000": "",
                            "701100": "B", "707100": "B", "708000": "B", "708800": "B", "709000": "B", "709100": "B", "709700": "B", "709800": "B",
                            "706100": "S", "708100": "S", "708300": "S", "708400": "S", "708500": "S", "709600": "S"}
        
        for line in report_data:
            report_task = {}

            # Vérifier les comptes concernés
            if line.account_id.code in collecte_accounts:
                report_task['Déductible ou Collectée'] = "C"
                report_task['Libellé opération'] = line.name or ''
                report_task['Date facture (jj/mm/aaaa)'] = line.date or ''
                report_task['Référence facture'] = line.move_id.name if line.move_id else ''

                # Initialisation des montants
                report_task['Montant HT'] = 0
                report_task['Montant TVA'] = 0
                report_task['Condition'] = ''  # Nouveau champ pour les conditions

                # Obtenez le mouvement associé
                move = line.move_id
                if move:
                    # Comptes avec montant HT uniquement
                    if line.account_id.code in ["701200", "702200", "703200", "704200", "706200", "707200"]:
                        report_task['Montant HT'] = abs(line.credit)
                        report_task['Montant TVA'] = 0
                        report_task['Condition'] = 'Aucune taxe'
                        report_task['Code Anex'] = '100 - Chiffre d\'affaires taxable relatif aux exportations (taux 0%)'
                        report_task['Code décl'] = '100 - CA taxable relatif aux exportations (0%)'

                    elif line.account_id.code == "707102":
                        report_task['Montant HT'] = abs(line.credit)
                        report_task['Montant TVA'] = 0
                        report_task['Condition'] = 'Aucune taxe'
                        report_task['Code Anex'] = '160 - Chiffre d\'affaires exonéré'
                        report_task['Code décl'] = '155 - CA MP soumis TMP'

                    # Comptes avec montant HT et TVA
                    elif line.account_id.code in ["721100", "722000"]:
                        report_task['Montant HT'] = abs(line.credit)
                        report_task['Montant TVA'] = report_task['Montant HT'] * 0.2
                        report_task['Condition'] = 'TVA standard'
                        report_task['Code Anex'] = '210 - TVA collectée [lignes [(105 + 106 +107 + 108 + 115 + 125 )*20%]'
                        report_task['Code décl'] = '125 - CA / livraison à soi-même'

                    elif line.account_id.code in ["756000"]:
                        report_task['Montant HT'] = abs(line.credit)
                        report_task['Montant TVA'] = report_task['Montant HT'] * 0.2
                        report_task['Condition'] = 'TVA standard'
                        report_task['Code Anex'] = '210 - TVA collectée [lignes [(105 + 106 +107 + 108 + 115 + 125 )*20%]'
                        report_task['Code décl'] = '115 - Produits de cession d\'immobilisations (20%)'
                    
                    elif line.account_id.code in ["768000"]:
                        report_task['Montant HT'] = abs(line.credit)
                        report_task['Montant TVA'] = report_task['Montant HT'] * 0.2
                        report_task['Condition'] = 'TVA standard'
                        report_task['Code Anex'] = '210 - TVA collectée [lignes [(105 + 106 +107 + 108 + 115 + 125 )*20%]'
                        report_task['Code décl'] = '107 - CA taxable / prestations de service'

                    # Comptes avec montant HT provenant du champ amount_untaxed et TVA à partir de taxes associées
                    elif line.account_id.code in ["701100", "707100", "708000", "708800", "709000", "709100", "709700", "709800"]:
                        if move.amount_untaxed:
                            report_task['Montant HT'] = move.amount_untaxed

                        # Calcul du montant TVA à partir des taxes
                        if move.amount_by_group and move.amount_by_group[0][1] != 0:
                            report_task['Montant TVA'] = abs(move.amount_by_group[0][1])
                            report_task['Code Anex'] = '210 - TVA collectée [lignes [(105 + 106 +107 + 108 + 115 + 125 )*20%]'
                            report_task['Code décl'] = '106 - CA taxable / vente de biens'
                            report_task['Condition'] = 'TVA calculée'
                        else:
                            if move.attestation_destination:
                                report_task['Montant TVA'] = 0
                                report_task['Code Anex'] = '160 - Chiffre d\'affaires exonéré'
                                report_task['Code décl'] = '130 - CA objet d\'une attestation de destination (AD)'
                                report_task['Condition'] = 'Attestation de destination'
                            else:
                                report_task['Montant TVA'] = 0
                                report_task['Code Anex'] = '160 - Chiffre d\'affaires exonéré'
                                report_task['Code décl'] = '160 - CA exonéré'
                                report_task['Condition'] = 'Exonéré'

                    elif line.account_id.code in ["706100", "708100", "708300", "708400", "708500", "709600"]:                             
                        if move.amount_untaxed:
                            report_task['Montant HT'] = move.amount_untaxed

                        # Calcul du montant TVA à partir des taxes
                        if move.amount_by_group and move.amount_by_group[0][1] != 0:
                            report_task['Montant TVA'] = abs(move.amount_by_group[0][1])
                            report_task['Code Anex'] = '210 - TVA collectée [lignes [(105 + 106 +107 + 108 + 115 + 125 )*20%]'
                            report_task['Code décl'] = '107 - CA taxable / prestations de service'
                            report_task['Condition'] = 'TVA calculée'
                        else:
                            if move.attestation_destination:
                                report_task['Montant TVA'] = 0
                                report_task['Code Anex'] = '160 - Chiffre d\'affaires exonéré'
                                report_task['Code décl'] = '130 - CA objet d\'une attestation de destination (AD)'
                                report_task['Condition'] = 'Attestation de destination'
                            else:
                                report_task['Montant TVA'] = 0
                                report_task['Code Anex'] = '160 - Chiffre d\'affaires exonéré'
                                report_task['Code décl'] = '160 - CA exonéré'
                                report_task['Condition'] = 'Exonéré'

                # Extraire la date de paiement
                payment_date = None
                if line.move_id and line.move_id.payment_ids:
                    payments = line.move_id.payment_ids
                    payment_date = payments[0].payment_date if payments else None
                report_task['Date de paiement (jj/mm/aaaa)'] = payment_date.strftime('%d/%m/%Y') if payment_date else ''

                # Extraire le numéro DAU
                dau = None
                if line.move_id and line.move_id.dau_ids:
                    dau = line.move_id.dau_ids[0].name if line.move_id.dau_ids else None
                report_task['NDAU'] = dau or ''

                # Extraire les informations du partenaire
                if line.partner_id:
                    partner = line.partner_id
                    country_name = partner.country_id.name.lower() if partner.country_id else ''
                    report_task['Local ou Etranger'] = 'L' if country_name in ['madagascar', 'antananarivo'] else 'E'
                    report_task['Raison sociale'] = partner.name or ''
                    report_task['NIF (10 chiffres avec les 0)'] = partner.nif or ''
                    report_task['Partenaire/Stat'] = partner.stat or ''
                    report_task['Adresse'] = partner.street or ''
                    report_task['Pays du partenaire'] = partner.country_id.name or ''
                else:
                    report_task['Raison sociale'] = ''
                    report_task['NIF (10 chiffres avec les 0)'] = ''
                    report_task['STAT'] = ''
                    report_task['Adresse'] = ''
                    report_task['Local ou Etranger'] = ''

                
                report_task['Nature'] = collecte_accounts.get(line.account_id.code, '')
                report_task['Observation'] = ''
                # Ajoutez la ligne seulement si le montant HT est différent de zéro
                if report_task['Montant HT'] != 0:
                    reports_task.append(report_task)

        df = pd.DataFrame(reports_task)
        if df.empty:
            raise exceptions.UserError(f"Il n'y a pas de données entre {self.du} et {self.au}")

        return df


    def get_report_TVA_xlsx(self):
        # Obtenez les données pour TVA déductible
        df_deductible = self.get_data_TVADeductible()

        # Obtenez les données pour TVA collectée
        df_collectee = self.get_data_TVACollectee()

        # Ajouter une colonne pour identifier le type de TVA
        df_deductible['Déductible ou Collectée'] = 'D'
        df_collectee['Déductible ou Collectée'] = 'C'

        # Combinez les deux DataFrames
        df_combined = pd.concat([df_deductible, df_collectee], ignore_index=True)

        # Créez un fichier Excel temporaire
        file_name = 'TVA.xlsx'
        tmpdir = tempfile.mkdtemp()
        tmpdir = tmpdir.rstrip('/')
        workbook = xlsxwriter.Workbook(f"{tmpdir}/{file_name}", {'nan_inf_to_errors': True})
        sheet = workbook.add_worksheet('TVA')

        # Définissez les formats pour le fichier Excel
        date_format = workbook.add_format({'num_format': 'dd/mm/yyyy', 'align': 'center', 'valign': 'vcenter'})
        header_format = workbook.add_format({'border': 0, 'bold': True, 'align': 'center', 'valign': 'vcenter'})
        body_format = workbook.add_format({'align': 'center', 'valign': 'vcenter'})

        column_widths = [15, 15, 15, 20, 20, 15, 20, 20, 20, 5, 10, 30, 30, 15, 15, 20, 20, 20]
        for col, width in enumerate(column_widths):
            sheet.set_column(col, col, width)
        sheet.set_row(0, 40)

        # Écrire les en-têtes de colonnes
        headers = ['Déductible ou Collectée', 'Local ou Etranger', 'NIF (10 chiffres avec les 0)', 'Raison sociale', 'Partenaire/Stat', 'Adresse', 'Montant HT', 'Montant TVA', 'Référence facture', 'Date facture (jj/mm/aaaa)','Nature', 
                'Libellé opération', 'Date de paiement (jj/mm/aaaa)', 'Mois', 'Année', 'Observation', 'NDAU', 'Code Anex', 'Code décl']

        for col, header in enumerate(headers):
            sheet.write(0, col, header, header_format)

        # Écrire les données
        row = 1
        for index, row_data in df_combined.iterrows():
            date_paiement = row_data.get('Date de paiement (jj/mm/aaaa)')
            if pd.notnull(date_paiement):
                try:
                    date_paiement = pd.to_datetime(date_paiement)
                    if pd.notna(date_paiement):
                        month = date_paiement.month
                        year = date_paiement.year
                        sheet.write(row, 12, date_paiement, date_format)
                        sheet.write(row, 13, month, body_format)
                        sheet.write(row, 14, year, body_format)
                    else:
                        sheet.write(row, 12, '', date_format)
                        sheet.write(row, 13, '', body_format)
                        sheet.write(row, 14, '', body_format)
                except ValueError:
                    sheet.write(row, 12, '', date_format)
                    sheet.write(row, 13, '', body_format)
                    sheet.write(row, 14, '', body_format)
            else:
                sheet.write(row, 12, '', date_format)
                sheet.write(row, 13, '', body_format)
                sheet.write(row, 14, '', body_format)

            sheet.write(row, 0, row_data.get('Déductible ou Collectée'), body_format)
            sheet.write(row, 1, row_data.get('Local ou Etranger'), body_format)
            sheet.write(row, 2, row_data.get('NIF (10 chiffres avec les 0)'), body_format)
            sheet.write(row, 3, row_data.get('Raison sociale'), body_format)
            sheet.write(row, 4, row_data.get('Partenaire/Stat'), body_format)
            sheet.write(row, 5, row_data.get('Adresse'), body_format)
            sheet.write(row, 6, row_data.get('Montant HT'), body_format)
            sheet.write(row, 7, row_data.get('Montant TVA'), body_format)
            sheet.write(row, 8, row_data.get('Référence facture'), body_format)
            sheet.write(row, 9, row_data.get('Date facture (jj/mm/aaaa)'), date_format)
            sheet.write(row, 10, row_data.get('Nature'), body_format)
            sheet.write(row, 11, row_data.get('Libellé opération'), body_format)
            sheet.write(row, 15, " ", body_format)
            sheet.write(row, 16, row_data.get('NDAU'), body_format)
            sheet.write(row, 17, row_data.get('Code Anex'), body_format)
            sheet.write(row, 18, row_data.get('Code décl'), body_format)

            row += 1

        workbook.close()

        with open(f"{tmpdir}/{file_name}", "rb") as file:
            out = base64.b64encode(file.read())
            self.write({'report': out, 'name': f'Rapport TVA {self.compagnie.name} du {self.du} au {self.au}.xlsx'})

        return {
            'type': 'ir.actions.act_window',
            'res_model': 'viseo_export_tva.wizard',
            'view_mode': 'form',
            'res_id': self.id,
            'views': [(False, 'form')],
            'target': 'new',
            'name': 'Rapport TVA'
        }



