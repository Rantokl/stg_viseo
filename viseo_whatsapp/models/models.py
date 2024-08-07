# -*- coding: utf-8 -*-

from odoo import models, fields, api
#from whatsapp_api_client_python import API
import requests, json
import re
from odoo.exceptions import UserError


def update_group_security(group_id, admins_only):
    url = f'http://10.68.132.2:3000/api/default/groups/{group_id}/settings/security/messages-admin-only'
    headers = {
        'accept': '*/*',
        'Content-Type': 'application/json'
    }
    data = {
        'adminsOnly': admins_only
    }

    response = requests.put(url, headers=headers, json=data)

    if response.status_code == 200:
        print('Group security settings updated successfully.')
    else:
        print(f'Failed to update group security settings. Status code: {response.status_code}')
        print(response.text)


def get_user(group_id):
    #group_id = "120363287502846533@g.us"

    # Définir l'URL et les en-têtes de la requête
    url = f'http://10.68.132.2:3000/api/default/groups/{group_id}'
    headers = {'accept': '*/*'}

    # Effectuer la requête GET
    response = requests.get(url, headers=headers)

    # Vérifier le code de statut de la réponse
    if response.status_code == 200:
        # Récupérer les données JSON
        data = response.json()

        # Extraire les IDs des participants en excluant celui avec l'ID '261341130307@c.us'
        participant_ids = [participant['id']['_serialized'] for participant in data['groupMetadata']['participants'] if
                           participant['id']['_serialized'] != '261341130307@c.us']

        return participant_ids
        # for participant_id in participant_ids:
        #     print(participant_id)
    else:
        print(f"Erreur lors de la requête : {response.status_code}")
        return None


def format_numero_telephone(numero):
    numero_numerique = ''.join(filter(str.isdigit, numero))

    if numero_numerique.startswith('261'):
        numero = numero_numerique[3:12]

    else:
        numero = numero_numerique[:10]
        if numero.startswith('0'):
            numero = numero[1:]

    numero = '261' + numero

    numero += '@c.us'

    return numero


def add_participant_to_group(group_id, participant_id):
    api_url = f"http://10.68.132.2:3000/api/default/groups/{group_id}/participants/add"

    headers = {
        "accept": "*/*",
        "Content-Type": "application/json",
    }

    payload = {
        "participants": [
            {
                "id": participant_id
            }
        ]
    }

    try:
        response = requests.post(api_url, headers=headers, json=payload)

        if response.status_code // 100 == 2:
            print(f"Participant {participant_id} ajouté au groupe {group_id} avec succès.")
        else:
            print(
                f"Échec de l'ajout du participant {participant_id} au groupe {group_id}. Code d'erreur : {response.status_code}")
            print("Réponse du serveur:", response.text)

    except Exception as e:
        print(f"Une erreur s'est produite lors de l'ajout du participant {participant_id} au groupe {group_id} : {e}")


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

            # Parcourir les données JSON
            for data in json_data:
                if isinstance(data, dict) and data.get('name') == name and 'name' in data:
                    print("----")
                    print(f"Nom: {data['name']}")
                    if 'user' in data['id']:
                        print(f"ID: {data['id']['_serialized']}")
                    group = data['id']['_serialized']
                    group_name = data['name']

                    if group and group_name:
                        return group, group_name
                    else:
                        print('Nothing')
                        return None, None

        else:
            print(f"Échec de la requête GET. Code d'erreur: {response.status_code}")
            print("Réponse du serveur:", response.text)
            return None, None

    except Exception as e:
        print(f"Une erreur s'est produite: {e}")

    return None, None


def send_whatsapp_message(id, message):
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
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char('Nom du groupe')
    chat_ids = fields.Char('Numero du groupe')
    users = fields.Char('Sender')
    body = fields.Text('Message(s)')
    model_id = fields.Char()
    id_model = fields.Char()
    partner_id = fields.Many2many('res.partner', string='Clients')


class WhhatsAppViseo(models.Model):
    _name = 'whatsapp.viseo'
    _description = 'Message whatsapp'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    body = fields.Text('Message(s)')
    current_user = fields.Many2one('res.users', string="Emetteur", readonly=True, default=lambda self: self.env.user.id)
    receiver = fields.Many2one('res.partner', string='Client')
    attachment_ids = fields.Many2many('ir.attachment', string='Pièce(s) jointes(s)')
    id_model = fields.Char('Id')
    model_name = fields.Char('Model')
    group_id = fields.Many2one('whatsapp.group', string="Groupe")
    group_name = fields.Char('Groupe')
    choice = fields.Selection([('interne', 'Interne'), ('wclient', 'Interne avec client')], 'Envoyer en',
                              default='interne')
    customer = fields.Boolean(compute="_computeUser", default=False)

    @api.onchange('group_name')
    def _computeUser(self):
        if self.choice == 'wclient':
            group, group_name = get_api_group(self.group_name)
            if group:
                self.customer = True

            else:
                self.customer = False

        else:
            self.customer = False

    # @api.depends('current_user')
    def computeUser(self):
        if self.env.user.has_group('viseo_whatsapp.group_send_whatsapp'):
            return {'value': 'True'}
        else:
            return {'value': 'False'}

    # @api.onchange('receiver')
    # def addCustomer(self):
    #     client = self.receiver
    #     if client:
    #         group, group_name = get_api_group(self.group_name)
    #         if group:
    #             number = format_numero_telephone(client.mobile)
    #             add_participant_to_group(group, number)
    #         else:
    #             pass

    @api.onchange('group_name')
    def UpdateDeleteUser(self):
        users = self.env[self.model_name].search([('id', '=', self.id_model)])
        user_follower = users.message_follower_ids.partner_id.ids
        user_followers = users.message_follower_ids.partner_id
        if self.group_name == None:
            pass

        else:
            group = self.env['whatsapp.group'].sudo().search([('name', '=', self.group_name)])
            get_api_group(self.group_name)
            if group:
                users = group.partner_id.ids
                partner_ids = get_user(group.chat_ids)
                if len(users) == len(user_follower):
                    pass
                else:
                    for user in user_followers:
                        user_id = self.env['hr.employee'].sudo().search([('address_home_id.id', '=', user.id)])
                        number_user = user_id.mobile_phone
                        number = format_numero_telephone(number_user)
                        if number in partner_ids:
                            pass
                        else:

                            add_participant_to_group(group.chat_ids, number)
                    group.write({
                        'partner_id': user_follower
                    })

    @api.onchange('choice')
    def compute_group(self):

        data = self.env[self.model_name].search([('id', '=', self.id_model)])
        if self.choice == 'interne':
            if self.model_name == 'fleet.vehicle':
                group_name1 = 'INT_' + data.vin_sn[-7:]
            else:
                if self.model_name == 'res.partner':
                    group_name1 = 'INT_' + 'PARTNER_' + str(data.id)
                else:
                    group_name1 = 'INT_' + data.name
            # groups, group_name = get_api_group(group_name1)
            # if group_name is None:
            #     self.createGroup(group_name1)
            #     self.group_name = group_name1
            # else:
            self.group_name = group_name1
        else:
            if self.choice == 'wclient':
                if self.model_name == 'fleet.vehicle':
                    group_name1 = data.vin_sn[-7:]
                else:
                    if self.model_name == 'res.partner':
                        group_name1 = 'PARTNER_' + str(data.id)
                    else:
                        group_name1 = data.name
                groups, group_name = get_api_group(group_name1)

                # if not group_name:
                #     self.createGroup(group_name1)
                #     self.group_name = group_name1
                # else:
                self.group_name = group_name1

        # users = self.env[self.model_name].search([('id', '=', self.id_model)])
        # return users.message_follower_ids.partner_id

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

    def format_numero_telephone(self, numero):
        numero_numerique = ''.join(filter(str.isdigit, numero))

        if numero_numerique.startswith('261'):
            numero = numero_numerique[3:12]

        else:
            numero = numero_numerique[:10]
            if numero.startswith('0'):
                numero = numero[1:]

        numero = '261' + numero

        numero += '@c.us'

        return numero

    def createGroup(self, group):

        url = "http://10.68.132.2:3000/api/default/groups"
        users = self.env[self.model_name].search([('id', '=', self.id_model)])
        user_followers = users.message_follower_ids.partner_id

        numbers = []
        partner = []
        # if user_followers:
        for user in user_followers:
            user_id = self.env['hr.employee'].sudo().search([('address_home_id.id', '=', user.id)])
            number_user = user_id.mobile_phone
            numb = user.mobile
            number = self.format_numero_telephone(number_user)
            numbers.append(number)
            partner.append(user.id)
            if not user.mobile:
                user.sudo().write({'mobile': number[0:12],
                            'phone': number[0:12]})

        user_mobile = self.env['hr.employee'].sudo().search([('user_id.id', '=', self.env.user.id)])
        number_user = user_mobile.mobile_phone
        number_user = self.format_numero_telephone(number_user)
        numbers.append(number_user)
        partners = partner.append(self.env.user.partner_id.id)
        participant_numbers = numbers

        # Créer la liste des participants
        participants = [
            {
                "id": f"{num}"
            } for num in participant_numbers
        ]
        # Données pour la création du groupe
        data = {
            "name": group,
            "participants": participants
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
        if response.status_code == 201:
            print("Le groupe a été créé avec succès !")
            response_data = json.loads(response.text)
            serialized_id = response_data["gid"]["_serialized"]
            update_group_security(serialized_id, False)

            message = "Group created by {}".format(self.env.user.name)
            send_whatsapp_message(serialized_id, message)

            # print(f"Valeur de _serialized : {serialized_id}")
            groups = {
                'name': group,
                'chat_ids': serialized_id,
                'users': '261341130307@c.us',
                'body': 'Group created',
                'model_id': self.model_name,
                'id_model': self.id_model,
                'partner_id': partner

            }
            self.env['whatsapp.group'].sudo().create(groups)
            return serialized_id
        else:
            print("Erreur lors de la création du groupe. Code de réponse :", response.status_code)


    def takeallgroup(self):

        # Endpoint de l'API
        url = "http://10.68.132.2:3000/api/default/groups"

        # Faire la requête GET
        response = requests.get(url, headers={"accept": "*/*"})

        # Vérifier le statut de la réponse
        if response.status_code == 200:
            # Récupérer les données JSON
            data = json.loads(response.text)

            # Extraire les valeurs de 'subject' et '_serialized' dans des tableaux séparés
            subjects = []
            serialized_ids = []
            for group in data:
                if 'subject' in group['groupMetadata']:
                    subjects.append(group['groupMetadata']['subject'])
                    serialized_ids.append(group['groupMetadata']['id']['_serialized'])

            return serialized_ids
        else:
            print(f"Erreur lors de la requête : {response.status_code}")
            return None

    def checkMessage(self):

        chat_ids = self.takeallgroup()

        for chat_id in chat_ids:
            url = f'http://10.68.132.2:3000/api/messages?chatId={chat_id}&downloadMedia=true&limit=10&session=default'
            headers = {'accept': '*/*'}

            response = requests.get(url, headers=headers)
            data = response.json()

            if data:
                message_data = data[-1]
                message = message_data['body']
                group = self.env['whatsapp.group'].search([('chat_ids', '=', chat_id)])
                if group.body == message:
                    pass
                else:
                    if 'author' in message_data['_data']:
                        author = message_data['_data']['author']['_serialized']
                    else:
                        author = message_data['from']

                    local = '0' + author[3:-5]
                    interna = '+261' + author[3:-5]
                    intern = '261' + author[3:-5]

                    partner = self.env['res.partner'].sudo().search(
                        ['|', '|', ('mobile', '=', local), ('mobile', '=', interna), ('mobile', '=', intern)])
                    if partner:
                        group.write({
                            'body': message
                        })
                        if group:
                            data = self.env[group.model_id].search([('id', '=', group.id_model)])
                            bodyValue = (("<p>%s</p>"
                                          '<p style="color:blue;">Envoyé par Whatsapp</p>') % (message))
                            data.message_post(
                                body=bodyValue,
                                author_id=partner.id)
                # print(f"Message pour le chat_id {chat_id}: {message}")
            else:
                print(f"Pas de message pour le chat_id {chat_id}")
        return True

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

        groups, group_name = get_api_group(self.group_name)
        group = self.env['whatsapp.group'].search([('name', '=', group_name)])
        if group:
            group.write({
                'users': '261341130307@c.us',
                'body': self.body
            })
        if groups:
            response = send_whatsapp_message(groups, self.body)
            bodyValue = (("<p>%s</p>"
                          '<p style="color:blue;">Envoyé par Whatsapp</p>') % (self.body))
            data.message_post(
                body=bodyValue)
            data.message_subscribe(partner_ids=self.env.user.partner_id.ids)
        else:
            if self.receiver is None:
                raise UserError("Veuillez remplir le champ client")
            else:
                if self.receiver:
                    serialized_id = self.createGroup(self.group_name)
                    add_participant_to_group(serialized_id, self.receiver.mobile)
                    response = send_whatsapp_message(serialized_id, self.body)
                    bodyValue = (("<p>%s</p>"
                                  '<p style="color:blue;">Envoyé par Whatsapp</p>') % (self.body))
                    data.message_post(
                        body=bodyValue)
                    data.message_subscribe(partner_ids=self.env.user.partner_id.ids)

                else:

                    serialized_id = self.createGroup(self.group_name)
                    response = send_whatsapp_message(serialized_id, self.body)
                    bodyValue = (("<p>%s</p>"
                                  '<p style="color:blue;">Envoyé par Whatsapp</p>') % (self.body))
                    data.message_post(
                        body=bodyValue)
                    data.message_subscribe(partner_ids=self.env.user.partner_id.ids)

        return {
            'type': 'ir.actions.client',
            'tag': 'reload',
        }

    def _computeGroup(self):
        receiver = self.receiver

    users = fields.Many2many('res.users', string="Interne")

    def take_group_whatsapp(self, model_name, id_model):
        data = self.env[model_name].search([('id', '=', id_model)])
        # users = self.env[self.model_name].search([('id', '=', self.id_model)])
        user_followers = data.message_follower_ids.partner_id
        if user_followers:
            if self.choice == 'interne':
                if self.model_name == 'fleet.vehicle':
                    group_name1 = 'INT_' + data.vin_sn[-7:]
                else:
                    if self.model_name == 'res.partner':
                        group_name1 = 'INT_' + 'PARTNER_' + str(data.id)
                    else:
                        group_name1 = 'INT_' + data.name

            else:
                if self.model_name == 'fleet.vehicle':
                    group_name1 = data.vin_sn[-7:]
                else:
                    if self.model_name == 'res.partner':
                        group_name1 = 'PARTNER_' + str(data.id)
                    else:
                        group_name1 = data.name

            return {'group': 'Test',
                    'name': group_name1}
        else:
            raise UserError("Veuillez rajouter des abonnés avant d'envoyer des messages")


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

    def send_message_api(self, id, message):
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


class InviteWhatsapp(models.TransientModel):
    """ Wizard to invite partners (or channels) and make them followers. """
    _inherit = 'mail.wizard.invite'
    whatsapp = fields.Boolean('Invite whatsapp', default=True,
                              help="If checked, the partners will add in whatsapp group, they have been added in the document's followers.")

    def add_followers(self):
        return super(InviteWhatsapp, self).add_followers()


class MailMessage(models.Model):
    _inherit = 'mail.message'

    @api.model
    def fields_view_get(self, view_id=None, view_type='form', toolbar=False, submenu=False):
        res = super(MailMessage, self).fields_view_get(view_id=view_id, view_type=view_type, toolbar=toolbar,
                                                       submenu=submenu)
        context = dict(self.env.context)
        context['user_has_group'] = self.env.user.has_group('viseo_whatsapp.group_send_whatsapp')
        res['context'] = context
        return res


class Respartner(models.Model):
    _inherit = 'res.partner'

    def normalize_phone_number(self, phone):
        """
        Normalize phone numbers to international format without spaces.
        :param phone: str
        :return: str
        """
        # Remove all non-digit characters
        phone_clean = re.sub(r'\D', '', phone)

        # Check if it starts with the country code
        if phone_clean.startswith('261'):
            phone_clean = phone_clean[3:]
        elif phone_clean.startswith('0'):
            phone_clean = phone_clean[1:]
        elif phone_clean.startswith('+261'):
            phone_clean = phone_clean[4:]

        # Return the normalized phone number in international format
        return f'+261{phone_clean}'

    def update_phone_numbers(self):
        """
        Update phone numbers to international format and use employee's mobile_phone if phone is missing.
        """
        Employee = self.env['hr.employee'].sudo().search([])

        for partner in self.env['res.partner'].sudo().search([]):
            employee = self.env['hr.employee'].sudo().search([('address_home_id', '=', partner.id)])
            # if not partner.phone and partner.employee_ids:
            # Get the employee's mobile phone number if available

            if employee and employee.mobile_phone:
                partner_phone = self.normalize_phone_number(employee.mobile_phone)
                partner.sudo().write({'phone': partner_phone})

            if partner.phone:
                # Normalize the phone number
                # partner.phone = self.normalize_phone_number(partner.phone)
                partner.sudo().write({'phone':self.normalize_phone_number(partner.phone)})


