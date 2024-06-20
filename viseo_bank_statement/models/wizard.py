from odoo import models, fields, api
from selenium.common import TimeoutException
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import tempfile
import os
import pandas as pd
import numpy as np
import re
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from odoo.exceptions import UserError
import datetime
from selenium.webdriver.support.ui import Select
import tabula
import zipfile
import time



class BankStatementWizard(models.TransientModel):
    _name = 'web.scrap.wizard'


    date = fields.Date(string="Date de relevé", default=fields.Date.today())
    bank_id = fields.Many2one('res.bank', string="Banque", required=True)
    account_journal_id = fields.Many2one('account.journal', string="Journal du relevé")
    company_id = fields.Many2one('res.company', string="Société", related='account_journal_id.company_id')

    @api.onchange('bank_id')
    def _get_domain_journal(self):
        domain = []
        if self.bank_id:
            domain = [('bank_id', '=', self.bank_id.id)]
        return {'domain': {'account_journal_id': domain}}


    def check_exist_abs(self, date_bank_statement):
        exist_abs = self.env['account.bank.statement'].search([('date', '=', date_bank_statement),('journal_id', '=', self.account_journal_id.id)])
        return exist_abs

    def create_bank_statement(self, dataweb):
        date_bank_statement = dataweb['date'].min()
        if len(self.check_exist_abs(date_bank_statement)) > 0:
            abs_id = self.check_exist_abs(date_bank_statement)
        else:
            abs = self.env['account.bank.statement']
            name = "{} du {}".format(self.bank_id.name, date_bank_statement)
            balance_start = 0
            last_bnk_stmt = abs.search([('journal_id', '=', self.account_journal_id.id)], limit=1)
            #On create account_bank_statement we have to keep the last balance of previous account_bank_statement of the same journal_id
            if last_bnk_stmt:
                balance_start = last_bnk_stmt.balance_end
            else:
                balance_start = 0
            vals = {
                'name': name,
                'date': date_bank_statement,
                'journal_id': self.account_journal_id.id,
                'balance_start': balance_start
            }
            abs_id = abs.create(vals)

        for index, row in dataweb.iterrows():
            # Create a new bank statement line
            print(row['libelle'], row['date'])
            self.env['account.bank.statement.line'].create({
                'date': row['date'],
                'name': row['libelle'],
                'amount': row['amount'],
                'partner_id': row['partner_id'],
                'payment_id': row['payment_id'],
                'statement_id': abs_id.id,
                'is_from_web': True
            })

        #RETURN TO THE FORM VIEW OF ACCOUNT BANK STATEMENT
        action = self.env.ref('account.action_bank_statement_tree').read()[0]
        form_view = [(self.env.ref('account.view_bank_statement_form').id, 'form')]
        action['views'] = form_view
        action['res_id'] = abs_id.id
        return action



    def get_data_from_web(self):
        if self.bank_id.name.startswith("BNI"):
            dataweb = self.generate_bank_statement_line_BNI()
        elif self.bank_id.name.startswith("BOA"):
            dataweb = self.generate_bank_statement_line_BOA()
        elif self.bank_id.name.startswith("BFV"):
            dataweb = self.generate_bank_statement_line_BFV()
        elif self.bank_id.name.startswith("BMOI"):
            dataweb = self.generate_bank_statement_line_BMOI()
        elif self.bank_id.name.startswith("BGFI"):
            dataweb = self.generate_bank_statement_line_BGFI()
        self.create_bank_statement(dataweb)
        # return {
        #     'effect': {
        #         'fadeout': 'slow',
        #         'message': 'Recupération relevé terminée',
        #         'type': 'rainbow_man',
        #     }
        # }

    def update_dataframe_with_payments(self, df):
        # Clean dataset
        # Rename the 'Date op.' column to 'date'
        df.rename(columns={'Date op.': 'date'}, inplace=True)
        # Combine 'description' and 'reference' into 'libelle'
        df['libelle'] = df['Description'] + ' ' + df['Reference']
        # Create 'amount' column that contains 'debit' if it's not NaN, otherwise 'credit'
        df['amount'] = df.apply(lambda row: row['Débit'] if pd.notna(row['Débit']) else row['Crédit'], axis=1)
        # Reorganize the DataFrame columns
        df['cheque_number'] = df['libelle'].apply(self.extract_cheque_number_if_present)
        # Add column partner_id and payment_id
        df['partner_id'] = 0
        df['payment_id'] = 0
        df = df[['date', 'libelle', 'amount', 'cheque_number', 'partner_id', 'payment_id']]
        # Convert date column to datetime if not already
        date_format = '%d/%m/%y'  # Adjust this format to match your date format
        # Convert date column to datetime with the specified format
        df.loc[:, 'date'] = pd.to_datetime(df['date'], format=date_format, errors='coerce')
        df.loc[:, 'date'] = df['date'].dt.date
        #Keyword for bank expenses
        partner_keywords = ['frais', 'commissions', 'cion ', 'taxe', 'comm', 'achat dev', 'ouv dom ', 'com ope', 'vente devise']
        # Iterate through each row in the DataFrame
        for index, row in df.iterrows():
            cheque_number = row.get('cheque_number')
            amount = row['amount']
            date = row['date']

            #Get date min because date operation in bank may not the same as payment_banking_date
            date_min = date - datetime.timedelta(days=5)
            # Construct the domain dynamically
            if amount > 0:
                domain = [
                    ('amount', '=', abs(amount)),
                    ('date_depot', '>=', date_min),
                    ('date_depot', '<=', date),
                    ('bank_depot_id', '=', self.bank_id.id)
                ]
            else:
                domain = [
                    ('amount', '=', abs(amount)),
                    ('bank_id', '=', self.bank_id.id),
                ]
            #Check cheque_number and to domain search
            if cheque_number:
                normalized_reference = cheque_number.lstrip("0")
                domain.append(('reference', 'ilike', normalized_reference))

            # Search for matching account.payment record
            payment = self.env['account.payment'].search(domain, limit=1)

            if payment:
                # Update DataFrame with payment_id and partner_id
                df.at[index, 'payment_id'] = payment.id
                df.at[index, 'partner_id'] = payment.partner_id.id if payment.partner_id else np.nan
            else:
                if bool(self.bank_id.partner_id):
                    libelle_lower = row['libelle'].lower()
                    if any(keyword in libelle_lower for keyword in partner_keywords) and amount < 0:
                        df.at[index, 'partner_id'] = self.bank_id.partner_id.id
        return df


    def extract_cheque_number_if_present(self, libelle):
        cheque_keywords = ['CHQ', 'CHEQUE']
        libelle_lower = libelle.lower()
        # Check if any of the keywords are present in the libelle
        if any(keyword.lower() in libelle_lower for keyword in cheque_keywords):
            # Look for the first number following the keywords
            pattern = r'(?:' + '|'.join(re.escape(keyword.lower()) for keyword in cheque_keywords) + r')\D*(\d+)'
            match = re.search(pattern, libelle_lower, re.IGNORECASE)
            if match:
                return match.group(1)
        return None

    def clean_data_from_pdf_to_csv(self, df):
        new_names = {
            "Libellé de l'opération": 'Description',
            'Débit (MGA)': 'Débit',
            'Crédit (MGA)': 'Crédit',
            'Date': 'date'
        }
        df.rename(columns=new_names, inplace=True)
        df['Description'] = df['Description'].replace('\r', ' ', regex=True)
        df.insert(loc=df.columns.get_loc('Description') + 1, column='Reference', value='')
        df['date'] = pd.to_datetime(df['date'], format='%d/%m/%Y', errors='coerce')
        df_cleaned = df[pd.notna(df['date'])]
        # Step 1: Replace 'nan' strings with np.nan and clean the formatting
        df_cleaned['Débit'] = df_cleaned['Débit'].str.strip().str.replace(' ', '').str.replace(',', '.').replace('nan',
                                                                                                                 np.nan)
        df_cleaned['Crédit'] = df_cleaned['Crédit'].str.strip().str.replace(' ', '').str.replace(',', '.').replace(
            'nan', np.nan)
        df_cleaned[['Débit', 'Crédit']] = df_cleaned[['Débit', 'Crédit']].apply(pd.to_numeric, errors='coerce')
        # add negation to debit
        df_cleaned['Débit'] = np.where(pd.notna(df_cleaned['Débit']), -df_cleaned['Débit'], df_cleaned['Débit'])

        return df_cleaned

    def generate_bank_statement_line_BOA(self):
        url_authentification = "https://boaweb.of.africa/users/authentication"
        # bouton d'export en format (csv,xls,pdf)

        with tempfile.TemporaryDirectory() as download_dir:
            # Set up Firefox options
            firefox_options = Options()
            firefox_options.set_preference("browser.download.folderList", 2)  # Use custom download path
            firefox_options.set_preference("browser.download.dir", download_dir)
            firefox_options.set_preference("browser.download.useDownloadDir", True)
            firefox_options.set_preference("browser.helperApps.neverAsk.saveToDisk",
                                           "text/csv,application/csv")  # MIME types for CSV
            button_locator = (By.CSS_SELECTOR, "a.btn.btn-default.btn-sm[href*='/reporting/export/formt.csv']")
            try:
                driver = webdriver.Firefox(options=firefox_options)
                driver.maximize_window()
                # driver = webdriver.Firefox()
                driver.get(url_authentification)
                wait = WebDriverWait(driver, 120)  # Create a WebDriverWait object with a 60-second timeout
                #On attend maximum 60 s la présence du bouton avant de pouvoir cliquer sur l'exportation
                button = wait.until(EC.presence_of_element_located(button_locator))
                button.click()

                downloaded_file = None
                for filename in os.listdir(download_dir):
                    if filename.endswith(".csv"):
                        downloaded_file = os.path.join(download_dir, filename)
                        break

                if downloaded_file:
                    # Load the file into a DataFrame
                    df = pd.read_csv(downloaded_file)
                    new_df = self.update_dataframe_with_payments(df)
                    driver.quit()
                    return new_df

            except TimeoutException:
                raise UserError("Le fichier de relevé n'est pas encore prêt")


    def generate_bank_statement_line_BNI(self):
        url_authentification = "https://secure.bni.mg/retail/index.ebk"

        with tempfile.TemporaryDirectory() as download_dir:
            firefox_options = Options()
            firefox_options.set_preference("browser.download.folderList", 2)
            firefox_options.set_preference("browser.download.dir", download_dir)
            firefox_options.set_preference("browser.download.useDownloadDir", True)
            firefox_options.set_preference("browser.helperApps.neverAsk.saveToDisk",
                                           "text/csv,application/csv")
            button_locator = (By.ID, "NWP_telecharger")
            from_date = (By.NAME,"dateDebutPeriode")
            to_date = (By.NAME,"dateFinPeriode")
            try:
                driver = webdriver.Firefox(options=firefox_options)
                driver.get(url_authentification)

                wait = WebDriverWait(driver, 60)
                # Wait until field date are visible
                wait.until(EC.presence_of_element_located(from_date))
                wait.until(EC.presence_of_element_located(to_date))

                # Find input field date
                from_date_input = driver.find_element(By.NAME,"dateDebutPeriode")
                to_date_input = driver.find_element(By.NAME,"dateFinPeriode")

                # Get value input field date
                from_date_value = from_date_input.get_attribute('value')
                to_date_value = to_date_input.get_attribute('value')

                while not from_date_value or not to_date_value:
                    from_date_value = from_date_input.get_attribute('value')
                    to_date_value = to_date_input.get_attribute('value')

                wait = WebDriverWait(driver, 60)
                button = wait.until(EC.presence_of_element_located(button_locator))
                button.click()

                downloaded_file = None
                for filename in os.listdir(download_dir):
                    if filename.endswith(".pdf"):
                        downloaded_file = os.path.join(download_dir, filename)
                        break

                if downloaded_file:
                    downloaded_csv_file = os.path.join(download_dir, 'bni.csv')
                    # convert PDF into CSV
                    tabula.convert_into(downloaded_file, downloaded_csv_file, output_format="csv", pages='all',
                                        lattice=True)
                    df = pd.read_csv(downloaded_csv_file)
                    df.drop(['Valeur', 'Solde (MGA)'], axis=1, inplace=True)
                    df_cleaned = self.clean_data_from_pdf_to_csv(df)
                    new_df = self.update_dataframe_with_payments(df_cleaned)
                    driver.quit()
                    return new_df

            except TimeoutException:
                raise UserError("Le fichier de relevé n'est pas encore prêt")

    def generate_bank_statement_line_BMOI(self):
        url_authentification = "https://ebanking.bmoinet.net/index.ebk"

        with tempfile.TemporaryDirectory() as download_dir:
            firefox_options = Options()
            firefox_options.set_preference("browser.download.folderList", 2)
            firefox_options.set_preference("browser.download.dir", download_dir)
            firefox_options.set_preference("browser.download.useDownloadDir", True)
            firefox_options.set_preference("browser.helperApps.neverAsk.saveToDisk",
                                           "text/csv,application/csv")
            button_locator = (By.ID, "NWP_telecharger")
            from_date = (By.NAME, "dateDebutPeriode")
            to_date = (By.NAME, "dateFinPeriode")
            try:
                driver = webdriver.Firefox(options=firefox_options)
                driver.maximize_window()
                driver.get(url_authentification)

                wait = WebDriverWait(driver, 60)
                # Wait until field date are visible
                wait.until(EC.presence_of_element_located(from_date))
                wait.until(EC.presence_of_element_located(to_date))

                # Find input field date
                from_date_input = driver.find_element(By.NAME, "dateDebutPeriode")
                to_date_input = driver.find_element(By.NAME, "dateFinPeriode")

                # Get value input field date
                from_date_value = from_date_input.get_attribute('value')
                to_date_value = to_date_input.get_attribute('value')

                while not from_date_value or not to_date_value:
                    from_date_value = from_date_input.get_attribute('value')
                    to_date_value = to_date_input.get_attribute('value')

                wait = WebDriverWait(driver, 60)
                button = wait.until(EC.presence_of_element_located(button_locator))
                button.click()

                downloaded_file = None
                for filename in os.listdir(download_dir):
                    if filename.endswith(".pdf"):
                        downloaded_file = os.path.join(download_dir, filename)
                        break

                if downloaded_file:
                    downloaded_csv_file = os.path.join(download_dir, 'bmoi.csv')
                    # convert PDF into CSV
                    tabula.convert_into(downloaded_file, downloaded_csv_file, output_format="csv", pages='all', lattice=True)
                    df = pd.read_csv(downloaded_csv_file)
                    df.drop(['Valeur','Solde (MGA)'], axis=1, inplace=True)
                    df_cleaned = self.clean_data_from_pdf_to_csv(df)
                    new_df = self.update_dataframe_with_payments(df_cleaned)
                    driver.quit()
                    return new_df

            except TimeoutException:
                raise UserError("Le fichier de relevé n'est pas encore prêt")

    def generate_bank_statement_line_BFV(self):
        url_authentification = "https://www.sogecashnet.societegenerale.mg"

        with tempfile.TemporaryDirectory() as download_dir:
            firefox_options = Options()
            firefox_options.set_preference("browser.download.folderList", 2)
            firefox_options.set_preference("browser.download.dir", download_dir)
            firefox_options.set_preference("browser.download.useDownloadDir", True)
            firefox_options.set_preference("browser.helperApps.neverAsk.saveToDisk",
                                           "text/csv,application/csv")
            send_button = (By.CSS_SELECTOR, 'button.btn.btn-primary[type="button"][function="_submit"][form="DownloadList"]')
            check_button = (By.NAME, 'Select.Check')
            download_link = (By.XPATH, "//a[contains(., 'Télécharger des éléments sélectionnés comme archive ZIP')]")
            from_date = (By.NAME, "Select.StartDate")
            to_date = (By.NAME, "Select.EndDate")
            try:
                driver = webdriver.Firefox(options=firefox_options)
                driver.get(url_authentification)

                # Wait for the specific option element to be present
                wait = WebDriverWait(driver, 60)
                selected_option = wait.until(
                    EC.presence_of_element_located((By.XPATH, "//option[@selected and @value='STA001']"))
                )

                wait = WebDriverWait(driver, 60)
                # Wait until field date are visible
                wait.until(EC.presence_of_element_located(from_date))
                wait.until(EC.presence_of_element_located(to_date))

                # Find input field date
                from_date_input = driver.find_element(By.NAME, "Select.StartDate")
                to_date_input = driver.find_element(By.NAME, "Select.EndDate")

                # Get value input field date
                from_date_value = from_date_input.get_attribute('value')
                to_date_value = to_date_input.get_attribute('value')

                while not from_date_value or not to_date_value:
                    from_date_value = from_date_input.get_attribute('value')
                    to_date_value = to_date_input.get_attribute('value')

                wait = WebDriverWait(driver, 60)
                button = wait.until(EC.presence_of_element_located(send_button))
                button.click()

                wait = WebDriverWait(driver, 60)
                button = wait.until(EC.presence_of_element_located(check_button))
                button.click()

                wait = WebDriverWait(driver, 60)
                button = wait.until(EC.presence_of_element_located(download_link))
                button.click()

                time.sleep(10)

                downloaded_file = None
                for filename in os.listdir(download_dir):
                    if filename.endswith(".zip"):
                        downloaded_file = os.path.join(download_dir, filename)
                        break

                if downloaded_file:
                    with zipfile.ZipFile(downloaded_file, "r") as zip_file:
                        # Récupérer la liste des fichiers dans le ZIP
                        file_names = [file_name for file_name in zip_file.namelist() if file_name.endswith('.CSV')]

                        # Créer une liste vide pour stocker les DataFrames
                        dfs = []

                        # Parcourir chaque fichier dans le ZIP
                        for file_name in file_names:
                            # Lire le contenu du fichier dans le ZIP
                            with zip_file.open(file_name) as file:
                                # Supposons que le fichier soit au format CSV
                                df = pd.read_csv(file)
                                dfs.append(df)

                    # # Concaténer tous les DataFrames dans un seul DataFrame
                    combined_df = pd.concat(dfs, ignore_index=True)

            except TimeoutException:
                raise UserError("Le fichier de relevé n'est pas encore prêt")

    def generate_bank_statement_line_BGFI(self):
        url_authentification = "https://www5.bgfionline.com/mg/index.ebk"

        with tempfile.TemporaryDirectory() as download_dir:
            firefox_options = Options()
            firefox_options.set_preference("browser.download.folderList", 2)
            firefox_options.set_preference("browser.download.dir", download_dir)
            firefox_options.set_preference("browser.download.useDownloadDir", True)
            firefox_options.set_preference("browser.helperApps.neverAsk.saveToDisk",
                                           "text/csv,application/csv")
            button_locator = (By.ID, "NWP_telecharger")
            from_date = (By.NAME, "dateDebutPeriode")
            to_date = (By.NAME, "dateFinPeriode")
            try:
                driver = webdriver.Firefox(options=firefox_options)
                driver.get(url_authentification)

                wait = WebDriverWait(driver, 60)
                # Wait until field date are visible
                wait.until(EC.presence_of_element_located(from_date))
                wait.until(EC.presence_of_element_located(to_date))

                # Find input field date
                from_date_input = driver.find_element(By.NAME, "dateDebutPeriode")
                to_date_input = driver.find_element(By.NAME, "dateFinPeriode")

                # Get value input field date
                from_date_value = from_date_input.get_attribute('value')
                to_date_value = to_date_input.get_attribute('value')

                while not from_date_value or not to_date_value:
                    from_date_value = from_date_input.get_attribute('value')
                    to_date_value = to_date_input.get_attribute('value')

                wait = WebDriverWait(driver, 60)
                button = wait.until(EC.presence_of_element_located(button_locator))
                button.click()

                downloaded_file = None
                for filename in os.listdir(download_dir):
                    if filename.endswith(".pdf"):
                        downloaded_file = os.path.join(download_dir, filename)
                        break

                if downloaded_file:
                    downloaded_csv_file = os.path.join(download_dir, 'bgfi.csv')
                    # convert PDF into CSV
                    tabula.convert_into(downloaded_file, downloaded_csv_file, output_format="csv", pages='all',
                                        lattice=True)
                    df = pd.read_csv(downloaded_csv_file)
                    df.drop(['Valeur', 'Solde (MGA)'], axis=1, inplace=True)
                    df_cleaned = self.clean_data_from_pdf_to_csv(df)
                    new_df = self.update_dataframe_with_payments(df_cleaned)
                    driver.quit()
                    return new_df

            except TimeoutException:
                raise UserError("Le fichier de relevé n'est pas encore prêt")

    def create_account_bank_statement_line(self):
        pass


