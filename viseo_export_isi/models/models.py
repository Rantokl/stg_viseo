

from odoo import models, fields, api, exceptions
import xlsxwriter
import base64
import tempfile
from io import BytesIO
import pandas as pd

class ReportTaskIsi(models.Model):
    _inherit = 'account.move.line'

class WizardReportViseoISI(models.TransientModel):
    _name = 'viseo_export_isi.wizard'

    report = fields.Binary('Rapport Viseo ISI', filters='.xlsx', readonly=True)
    name = fields.Char(string="Nom du fichier", size=64)
    du = fields.Date(string='Du :')
    au = fields.Date(string="Jusqu'à :")
    compagnie = fields.Many2one("res.company", string="Société")

    def get_data_ISI(self):
        if self.du > self.au:
            raise exceptions.UserError("La date de début ne peut pas être postérieure à la date de fin.")

        domain = [
            ('create_date', '>=', self.du),
            ('create_date', '<=', self.au),
            ('company_id', '=', self.compagnie.id),
            
        ]
        report_data = self.env['account.move.line'].sudo().search(domain)

        reports_task = []
        for line in report_data:
            report_task = {}

            # Obtenez les taxes associées à la ligne de mouvement
            tax_ids = line.tax_ids.filtered(lambda t: t.name == 'Impôt Synthétique Intermittent - ISI')
            if tax_ids:
                report_task['Mombanyfifam-pivarotana(Détail de transaction)'] = line.name or None

                    # Déterminez le montant correspondant à l'ISI
                isicorrespondant = 0
                if line.move_id:
                    move = line.move_id
                    # Accédez à toutes les lignes de facture associées au mouvement
                    for invoice_line in move.invoice_line_ids:
                        # Vérifiez les taxes associées à chaque ligne de facture
                        for tax in invoice_line.tax_ids:
                            if tax.name == 'Impôt Synthétique Intermittent - ISI':
                                # S'il existe un montant pour cette taxe
                                isicorrespondant += tax.amount

                report_task['ISImifanarakaaminy*(ISI correspondant)'] = abs(line.move_id.amount_by_group[0][1]) or None
                print('======================='*8)
                print(line.name)
                print(line.move_id.amount_by_group[0][1])
                # Extraire la date de paiement
                payment_date = None
                if line.move_id and line.move_id.payment_ids:
                    payments = line.move_id.payment_ids
                    payment_date = payments[0].payment_date if payments else None
                report_task['Datin\'nyfifam-pivarotana*(Date de transaction)'] = payment_date or None

                # Obtenez les détails du partenaire
                if line.partner_id:
                    partner = line.partner_id
                    report_task.update({
                        'Anaranasyfanampiny*(Nom et Prénoms)': partner.name or None,
                        'Laharan\'nykarampanomdrom-pirenena*(CIN)': partner.cin or None,
                        'Faritany*(Province)': partner.province or None,
                        'Faritra*(Région)': partner.region or None,
                        'District': partner.district or None,
                        'Kaominina*(Commune)': partner.commune or None,
                        'Fokontany': partner.street or None
                    })
                else:
                    report_task.update({
                        'Anaranasyfanampiny*(Nom et Prénoms)': None,
                        'Laharan\'nykarampanomdrom-pirenena*(CIN)': None,
                        'Faritany*(Province)': None,
                        'Faritra*(Région)': None,
                        'District': None,
                        'Kaominina*(Commune)': None,
                        'Fokontany': None
                    })

                # Calculer le 'Montant de transaction' en fonction de 'ISI correspondant'
                if report_task.get('ISImifanarakaaminy*(ISI correspondant)'):
                    try:
                        isicorrespondant = report_task['ISImifanarakaaminy*(ISI correspondant)']
                        if isinstance(isicorrespondant, tuple):
                            isicorrespondant = isicorrespondant[0] if isicorrespondant else 0
                        isicorrespondant = float(isicorrespondant)
                        report_task['Saran\'nyfifampivarotana*(Montant de transaction)'] = isicorrespondant / 0.05
                    except (ValueError, TypeError):
                        report_task['Saran\'nyfifampivarotana*(Montant de transaction)'] = None
                else:
                    report_task['Saran\'nyfifampivarotana*(Montant de transaction)'] = None

                report_task['Anton\'nyfifampivarotana*(Nature)'] = ''  # En supposant que 'Nature' est un champ supplémentaire, sinon retirez cette ligne
                reports_task.append(report_task)

        df = pd.DataFrame(reports_task)
        if df.empty:
            raise exceptions.UserError(f"Il n'y a pas de données entre {self.du} et {self.au}")

        return df


    def get_report_ISI_xlsx(self):
        df = self.get_data_ISI()
        file_name = 'ISI.xlsx'
        tmpdir = tempfile.mkdtemp()
        tmpfile = f"{tmpdir}/{file_name}"
        
        with xlsxwriter.Workbook(tmpfile, {'nan_inf_to_errors': True}) as workbook:
            sheet = workbook.add_worksheet()
            sheet.set_default_row(15)

            date_format = workbook.add_format({'num_format': 'dd/mm/yyyy', 'align': 'center', 'valign': 'vcenter'})
            header_format = workbook.add_format({
                'border': 1, 'bold': True, 'align': 'center', 'valign': 'vcenter', 'bg_color': '#adb5bd'
            })
            body_format = workbook.add_format({
                'align': 'center', 'valign': 'vcenter'
            })

            column_widths = [20, 20, 20, 30, 20, 20, 20, 20, 30]
            for col, width in enumerate(column_widths):
                sheet.set_column(col, col, width)
            sheet.set_row(0, 40)

            headers = ['Anaranasyfanampiny*(Nom et Prénoms)', 'Laharan\'nykarampanomdrom-pirenena*(CIN)', 'Anton\'nyfifampivarotana*(Nature)', 'Mombanyfifam-pivarotana(Détail de transaction)', 'Datin\'nyfifam-pivarotana*(Date de transaction)',
                       'Saran\'nyfifampivarotana*(Montant de transaction)', 'ISImifanarakaaminy*(ISI correspondant)', 'Faritany*(Province)', 'Faritra*(Région)', 'District', 'Kaominina*(Commune)', 'Fokontany']
            for col, header in enumerate(headers):
                sheet.write(0, col, header, header_format)

            row = 1
            for index, row_data in df.iterrows():
                sheet.write(row, 0, row_data['Anaranasyfanampiny*(Nom et Prénoms)'], body_format)
                sheet.write(row, 1, row_data['Laharan\'nykarampanomdrom-pirenena*(CIN)'], body_format)
                sheet.write(row, 2, row_data['Anton\'nyfifampivarotana*(Nature)'], body_format)
                sheet.write(row, 3, row_data['Mombanyfifam-pivarotana(Détail de transaction)'], body_format)
                sheet.write(row, 4, row_data['Datin\'nyfifam-pivarotana*(Date de transaction)'], date_format)
                sheet.write(row, 5, row_data['Saran\'nyfifampivarotana*(Montant de transaction)'], body_format)
                sheet.write(row, 6, row_data['ISImifanarakaaminy*(ISI correspondant)'], body_format)
                sheet.write(row, 7, row_data['Faritany*(Province)'], body_format)
                sheet.write(row, 8, row_data['Faritra*(Région)'], body_format)
                sheet.write(row, 9, row_data['District'], body_format)
                sheet.write(row, 10, row_data['Kaominina*(Commune)'], body_format)
                sheet.write(row, 11, row_data['Fokontany'], body_format)
                
                row += 1

        with open(tmpfile, "rb") as file:
            out = base64.b64encode(file.read())
            self.write({'report': out, 'name': f'Rapport ISI {self.compagnie.name} du {self.du} au {self.au}.xlsx'})

        return {
            'type': 'ir.actions.act_window',
            'res_model': 'viseo_export_isi.wizard',
            'view_mode': 'form',
            'res_id': self.id,
            'views': [(False, 'form')],
            'target': 'new',
            'name': 'Rapport ISI'
        }