# -*- coding: utf-8 -*-

from odoo import models, fields, api
from whatsapp_api_client_python import API
import requests, json


def get_api_group(name):
    api_url = "http://10.68.132.2:3000/api/default/groups"

    # Remplacez ces en-têtes par les en-têtes requis par votre API
    headers = {
        "Content-Type": "application/json",
    }

    try:
        # Effectuer la requête GET
        response = requests.get(api_url, headers=headers)

        # Vérifier si la requête a réussi (code 2xx)
        if response.status_code // 100 == 2:
            # Afficher la réponse

            json_data = response.json()

            # Afficher chaque paire clé-valeur du JSON

            for data in json_data:
                if isinstance(data, dict) and data.get('name') == name and 'name' in data:
                    print("----")
                    print(f"Nom: {data['name']}")
                    if 'user' in data['id']:
                        print(f"ID: {data['id']['_serialized']}")
                    group = data['id']['_serialized']
                    group_name = data['name']
                else:
                    print('NOthing')
                    group = None
                    group_name = None
            return group, group_name



        else:
            print(f"Échec de la requête GET. Code d'erreur: {response.status_code}")
            print("Réponse du serveur:", response.text)



    except Exception as e:
        print(f"Une erreur s'est produite: {e}")


def send_whatsapp_message(self, id, message):

    api_url = "http://10.68.132.2:3000/api/sendText/"

    # Remplacez ces données par le corps de votre requête
    payload = {
        "chatId": id,
        "text": message,
        "session": "default"
    }

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

class viseo_whatsapp(models.TransientModel):
    _inherit = 'mail.compose.message'
    _description = 'viseo_whatsapp.viseo_whatsapp'

    whats = fields.Boolean('Envoyé par Whatsapp')
    receiver2 = fields.Many2many('res.partner', string="Client(s)")

    #     name = fields.Char() 	mail.email_compose_message_wizard_form
    #     value = fields.Integer()
    #     value2 = fields.Float(compute="_value_pc", store=True)
    #     description = fields.Text()
    #
    #     @api.depends('value')
    #     def _value_pc(self):
    #         for record in self:
    #             record.value2 = float(record.value) / 100

    def action_send_mail(self):
        print(self.whats)
        if self.whats == True:
            greenAPI = API.GreenAPI(
                "7103851220", "a7e6700873bb44bb91f191ee2abffff09050a9b71ed84850a8"
            )
            response = greenAPI.sending.sendMessage("261344903318@c.us", self.body)

            print(response.data)

            return super(viseo_whatsapp, self).action_send_mail()


class groupWhatsapp(models.Model):
    _name = 'whatsapp.group'

    name = fields.Char('Nom du groupe')
    chat_ids = fields.Char('Numero du groupe')


class WhhatsAppViseo(models.Model):
    _name = 'whatsapp.viseo'
    _description = 'Message whatsapp'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    body = fields.Text('Message(s)')
    current_user = fields.Many2one('res.users', string="Emetteur", readonly=True, default=lambda self: self.env.user.id)
    receiver = fields.Many2many('res.partner', string='Destinataires')
    attachment_ids = fields.Many2many('ir.attachment', string='Pièce(s) jointes(s)')
    id_model = fields.Char('Id')
    model_name = fields.Char('Model')
    group_id = fields.Many2one('whatsapp.group', string="Groupe")
    group_name = fields.Char('Groupe')
    choice = fields.Selection([('interne', 'Interne'), ('wclient', 'Interne avec client')], 'Envoyer en', default='interne')




    @api.onchange('choice')
    def compute_group(self):
        data = self.env[self.model_name].search([('id', '=', self.id_model)])
        if self.choice == 'interne':
            groups, group_name = get_api_group(data.name)
        users = self.env[self.model_name].search([('id', '=', self.id_model)])
        return users.message_follower_ids.partner_id
    def filter_by_type(self, data, type):
        filtered_data = [entry for entry in data if entry.get('type') == type]
        return filtered_data

    def openWhatsapp(self):

        print('Openn')
        return True

    def take_partner(self):
        users = self.env[self.model_name].search([('id', '=', self.id_model)])
        number = []

        for numb in users.message_follower_ids.partner_id:
            number.append(numb.mobile)
        return number


    def createGroup(self):

        url = "http://10.68.132.2:3000/api/default/groups"

        # Données pour la création du groupe
        data = {
            "name": "Test group",
            "participants": [
                {
                    "id": "261344903318@c.us"

                },
                {

                    "id": "261384900555@c.us"
                }
            ]
        }

        # Conversion des données en format JSON
        json_data = json.dumps(data)

        # En-têtes de la requête
        headers = {
            "Content-Type": "application/json"
        }

        # Envoi de la requête POST
        response = requests.post(url, data=json_data, headers=headers)

        # Vérification du code de réponse
        if response.status_code == 200:
            print("Le groupe a été créé avec succès !")
        else:
            print("Erreur lors de la création du groupe. Code de réponse :", response.status_code)

    def groupTest(self):
        url = "https://api.green-api.com/waInstance7103851220/getContacts/a7e6700873bb44bb91f191ee2abffff09050a9b71ed84850a8"

        payload = {}
        headers = {}

        response = requests.request("GET", url, headers=headers, data=payload)
        print(response, type(response))
        json_data_2 = json.loads(str(response.text.encode('utf8'), 'utf-8'))

        type_to_filter = "group"
        filtered_data = self.filter_by_type(json_data_2, "group")

        return filtered_data

    def action_send_whats(self):

        data = self.env[self.model_name].search([('id', '=', self.id_model)])

        groups, group_name = get_api_group(data.name)
        number = ""
        group = ""

        if groups:
            response = send_whatsapp_message(groups, self.body)
            bodyValue = (("<p>%s</p>"
                          '<p style="color:blue;">Envoyé par Whatsapp</p>') % (self.body))
            data.message_post(
                body=bodyValue)

        self.createGroup()

        #  return {
        #     'view_mode' : 'form',
        #     'res_model' : self.model_name,
        #     'type' : 'ir.actions.act_window',
        #     'target' : 'current',
        #     'res_id' : self[0].id_model,
        # }

    def _computeGroup(self):
        receiver = self.receiver



    users = fields.Many2many('res.users', string="Interne")


    def take_group_whatsapp(self, model_name, id_model):
        data = self.env[model_name].search([('id', '=', id_model)])

        group_id, group_name = get_api_group(data.name)
        return {'group':group_name,
                'name':data.name}


class MassWhatsapp(models.Model):
    _inherit = 'mailing.mailing'

    def format_numero_telephone(self, numero):
        numero_numerique = ''.join(filter(str.isdigit, numero))
        numero = numero_numerique[:10]
        if numero_numerique.startswith('261'):
            numero = numero_numerique[3:]

        if numero.startswith('0'):
            numero = numero[1:]



        numero = '261' + numero

        numero += '@c.us'

        return numero

    def action_send_now_whatsapp(self):

        for partner in self.partner_ids:
            try:
                number = self.format_numero_telephone(partner.mobile)
                self.send_message_api(number, self.body_plaintext)
                print(number)
            except:
                print("Mobile none")

        self.write({'state': 'done'})
        self.message_post(body="Messages envoyées")

        return True

    def send_message_api(id,message):
        # Remplacez cette URL par l'URL de votre API
        # print(message[0])
        api_url = "http://10.68.132.2:3000/api/sendText/"

        payload = {
            "chatId": id,
            "text": message,
            "session": "default"
        }

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
