# -*- coding: utf-8 -*-
import random
import string
from datetime import timedelta, datetime
from odoo import models, fields, api
from odoo.exceptions import ValidationError
from odoo.tools.translate import _
from pprint import pprint
import requests
import time
import psycopg2

from odoo.exceptions import UserError


def dbconnex(self):
    connex = psycopg2.connect(database='mobile_101023',
                              user='etech',
                              password='3Nyy22Bv',
                              host='10.68.132.2',
                              port='5432')
    curs = connex.cursor()

    return curs, connex


def send_notif(title, message, type_notif, customer_id):
    # Remplacez cette URL par l'URL de votre API
    # print(message[0])
    api_url = "http://10.68.132.2:8090/api/v1/send_notification/"

    # Remplacez ces données par le corps de votre requête
    payload = {
        "titre": title,
        "message": message[0],
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


class viseo_rdv_mobile(models.Model):
    _name = 'viseo_rdv_mobile.viseo_rdv_mobile'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Rendez-vous véhicule'

    name = fields.Char(string=f"RDV")
    date_today = fields.Date(string='Date today', default=fields.Date.today)

    current_user = fields.Many2one('res.users', string="Démandeur", readonly=True,
                                   default=lambda self: self.env.user.id)

    @api.model
    def create(self, sequence):
        sequence['name'] = self.env['ir.sequence'].next_by_code('viseo_rdv_mobile.viseo_rdv_mobile') or '/'
        # place_pont = f"Place: {sequence.get('place_id')}" if sequence['place_id'] else f"Pont: {sequence.get('pont_id')}"
        sequence['name'] = f"{sequence['name']}"

        # sequence['date_rdv'] = time.strptime(sequence['date_start'],"%Y-%m-%d %H:%M:%S").date()
        date = datetime.strptime(sequence['date_start'], "%Y-%m-%d %H:%M:%S").date()
        print(date)
        sequence['date_rdv'] = date
        return super(viseo_rdv_mobile, self).create(sequence)

    def insertData(self, query, value):
        curs, conn = dbconnex(self)
        try:
            # Exécuter la requête SQL pour insérer un nouvel enregistrement
            curs.execute(query, value)
            # Récupérer l'ID du nouvel enregistrement
            record_id = curs.fetchone()
            print(record_id)
            # Valider la transaction
            conn.commit()
            return record_id
        except Exception as error:
            # En cas d'erreur, annuler la transaction
            conn.rollback()
            print("Erreur lors de l'insertion de l'enregistrement :", error)

    @api.model
    def create(self, vals):
        vals['name'] = self.env['ir.sequence'].next_by_code('viseo_rdv_mobile.viseo_rdv_mobile') or '/'
        # place_pont = f"Place: {sequence.get('place_id')}" if sequence['place_id'] else f"Pont: {sequence.get('pont_id')}"
        vals['name'] = f"{vals['name']}"
        curs, connex = dbconnex(self)
        # sequence['date_rdv'] = time.strptime(sequence['date_start'],"%Y-%m-%d %H:%M:%S").date()
        date = datetime.strptime(str(vals['date_start']), "%Y-%m-%d %H:%M:%S").date()
        print(date)
        vals['date_rdv'] = date
        date = datetime.strptime(str(vals['date_start']), "%Y-%m-%d %H:%M:%S").date()
        car = self.env['fleet.vehicle'].search([('id', '=', vals['customer_vehicle_id'])])
        if car.tag_ids.id == 11:
            if 'rdv_id' in vals:
                query = """SELECT * FROM public."viseoApi_rendezvous" WHERE id = %s"""
                curs.execute(query, (vals['rdv_id'],))
                datas = curs.fetchall()
                if datas:
                    return super(viseo_rdv_mobile, self).create(vals)
                    pass
                    # if car.tag_ids.id == 11:
            else:
                query = """INSERT INTO public."viseoApi_daterendezvous"(
                 type_rendez_vous_id, is_take, date_rendez_vous, heure_rendez_vous, owner_id, vehicle_id, is_take_by_date)
                VALUES ( %s, %s, %s, %s, %s, %s, %s) RETURNING id;
                        """
                value = (1, 'false', date, datetime.strptime(vals['date_start'], "%Y-%m-%d %H:%M:%S").time(), vals['customer_id'],
                vals['customer_vehicle_id'], 'false',)
                record_id = self.insertData(query, value)
                query = """INSERT INTO public."viseoApi_rendezvous"(
                 message, owner_id, status_rendez_vous_id, vehicle_id, date_rendez_vous_id)
                VALUES ( %s, %s, %s, %s, %s) RETURNING id;
                                    """
                value = (vals['note'], vals['customer_id'], 1, vals['customer_vehicle_id'], record_id[0],)

                record_id = self.insertData(query, value)
                connex.commit()

                vals['rdv_id'] = record_id[0]
                return super(viseo_rdv_mobile, self).create(vals)

        else:
            return super(viseo_rdv_mobile, self).create(vals)

    date_rdv = fields.Date('Date rdv')
    date_start = fields.Datetime(string="Date RDV", default=False)
    date_stop = fields.Datetime(string="Date fin", store=True)
    duration_unit = fields.Selection(
        string="Unité du durrée",
        selection=[
            ('day', 'Jour(s)'),
            ('hour', 'Heure(s)'),
            ('minute', 'Minute(s)')
        ],
        default='hour',
        required=True
    )
    duration = fields.Integer(
        string='Durrée',
        default=1
    )
    note = fields.Text(string='Messages')
    color = fields.Integer(default=1)
    etat = fields.Boolean('Etat', default=False)
    state = fields.Selection(string="Etat", selection=[
        ('new', 'Demande'),
        ('draft', 'En attente de validation'),
        ('accepted', 'Validé'),
        ('refused', 'Refusé'),
        ('canceled', 'Annulée')
    ], default="new", copy=False)

    # fleet.vehicle.model
    customer_id = fields.Many2one('res.partner', string="Client", related="customer_vehicle_id.driver_id")
    customer_vehicle_id = fields.Many2one('fleet.vehicle', 'Vehicules', required=True)

    customer_vehicle_tag = fields.Many2one('viseo.tag.rfid', string='Tag rfid', related='customer_vehicle_id.tag_rfid')
    customer_vehicle_model = fields.Many2one('fleet.vehicle.model', string='Modèle du vehicule',
                                             related='customer_vehicle_id.model_id')

    emplacement = fields.Selection(string="Emplacement", selection=[
        ('pl', 'Place'),
        ('pt', 'Pont'),
    ], default='pl', required=True)

    @api.onchange("emplacement")
    def _onchange_emplacement(self):
        if self.pont_id:
            self.pont_id = False
        if self.place_id:
            self.place_id = False

    atelier_id = fields.Many2one('fleet.workshop.type', string='Atelier', group_expand="_read_group_atelier_ids",
                                 readonly=True)
    responsable_atelier_id = fields.Many2many('res.users', string='Responsable atelier',
                                              related='atelier_id.responsable_id')
    mecanicien_id = fields.Many2one('hr.employee', string='Mecaniciens')

    place_id = fields.Many2one('place_vehicle.place_vehicle', 'Place', domain="[('atelier_id.id','=',atelier_id)]",
                               copy=False, default=False)
    pont_id = fields.Many2one('pont_vehicle.pont_vehicle', 'pont', domain="[('atelier_id.id','=',atelier_id)]",
                              copy=False, default=False)

    type_rendez_vous_id = fields.Many2one('type_rdv.type_rdv', string='Type de Rendez-vous',
                                          domain="[('atelier_id.id','=',atelier_id)]")

    validator = fields.Boolean(compute='_check_validator')
    rdv_id = fields.Integer()

    @api.model
    def _read_group_atelier_ids(self, atelier_id, domain, order):
        if self._context.get('restrict_rdv'):
            return atelier_id
        all_atelier = atelier_id.search([], order='name')
        return all_atelier

    def action_ask_rdv(self):
        to_subscribe = self.responsable_atelier_id
        substitute_leave = self.env['ir.module.module'].sudo().search(
            [('name', '=', 'viseo_substitute_leave'), ('state', '=', 'installed')])
        if substitute_leave:
            if to_subscribe.substitute_id:
                to_subscribe |= to_subscribe.substitute_id
        rdv = self.message_post(

            body='''Demande de rendez-vous de Mr(s) {} pour {} le {}'''.format(self.customer_id.name,
                                                                               self.type_rendez_vous_id.name,
                                                                               self.date_start, ),
            subject="Demande de rendez-vous de Mr(s) {}".format(self.customer_id.name),
            partner_ids=self.responsable_atelier_id.partner_id.ids
        )
        print(rdv.email_from)
        self.message_subscribe(partner_ids=to_subscribe.partner_id.ids)
        return self.write({'state': 'draft', 'color': 3}), rdv

    def action_validate_rdv(self):

        mecano = self.mecanicien_id
        place = self.place_id
        pont = self.pont_id
        date_start = self.date_start
        choice = self.emplacement
        if choice == 'pl':
            if mecano.id == False or place.id == False:
                raise ValidationError(('Veuillez ajouter un mecano ou une place'))
            else:
                records = self.env['viseo_rdv_mobile.viseo_rdv_mobile'].search(
                    [('state', '=', 'accepted'), ('id', '<', self.id)])
                if records:
                    for record in records:
                        if record.mecanicien_id.id == mecano.id and record.date_start == date_start:
                            raise ValidationError(('Vous ne pouvez pas avoir la mécano à la même période'))
                        else:
                            self.message_post(
                                body="Votre demande de rendez-vous du {} pour {} a été validée".format(self.date_start,
                                                                                                       self.type_rendez_vous_id.name),
                                subject="Demande de rendez-vous pour {}".format(self.type_rendez_vous_id.name),
                                # partner_ids=self.customer_id.ids
                            )
                            message = '''Votre demande de rendez-vous du {} pour {} au véhicule {} a été validée'''.format(
                                self.date_start,
                                self.type_rendez_vous_id.name, self.customer_vehicle_id.model_id.name),
                            title = "Rendez-vous"
                            send_notif(title, message, 3, self.customer_id.id)
                            curs, connex = dbconnex(self)
                            self.message_subscribe(partner_ids=self.customer_id.ids)
                            curs.execute("""UPDATE
										public."viseoApi_rendezvous"
										SET
										status_rendez_vous_id = %s
										WHERE id = %s;
									""", (2, self.rdv_id))
                            connex.commit()
                            connex.close()
                            return self.write({'state': 'accepted', 'color': 4})
                else:
                    return self.write({'state': 'accepted', 'color': 4})
        elif choice == 'pt':
            if mecano.id == False or pont.id == False:
                raise ValidationError(('Veuillez ajouter un mecano ou un pont'))
            else:
                records = self.env['viseo_rdv_mobile.viseo_rdv_mobile'].search(
                    [('state', '=', 'accepted'), ('id', '<', self.id)])
                if records:
                    for record in records:
                        if record.mecanicien_id.id == mecano.id and record.date_start == date_start:
                            raise ValidationError(('Vous ne pouvez pas avoir la mécano à la même période'))
                        else:
                            # print("Validé Mecano :", mecano.id)
                            return self.write({'state': 'accepted', 'color': 4})
                else:
                    self.message_post(
                        body="Votre demande de rendez-vous du {} pour {} a été validée".format(self.date_start,
                                                                                               self.type_rendez_vous_id.name),
                        subject="Demande de rendez-vous pour {}".format(self.type_rendez_vous_id.name),
                        # partner_ids=self.customer_id.ids
                    )
                    message = '''Votre demande de rendez-vous du {} pour {} au véhicule {} a été validée'''.format(
                        self.date_start,
                        self.type_rendez_vous_id.name, self.customer_vehicle_id.model_id.name),
                    title = "Rendez-vous"
                    send_notif(title, message, 3, self.customer_id.id)
                    curs, connex = dbconnex(self)
                    self.message_subscribe(partner_ids=self.customer_id.ids)
                    curs.execute("""UPDATE
								public."viseoApi_rendezvous"
								SET
								status_rendez_vous_id = %s
								WHERE id = %s;
							""", (2, self.rdv_id))
                    connex.commit()
                    connex.close()
                    return self.write({'state': 'accepted', 'color': 4})

    def action_not_validate_rdv(self):
        if not self.validator:
            raise UserError("Vous ne pouvez pas refuser cette rendez-vous")
        else:

            # self.write({'state': 'refused', 'color': 1})
            return {

                'type': 'ir.actions.act_window',
                'res_model': 'date.propose',
                'view_mode': 'form',
                # 'views':[(False,'form')],
                'target': 'new',
                'context': {'default_rdv_id': self.id,
                            },

            }

    def action_cancel_rdv(self):
        # if not self.validator:
        # 	raise UserError("Vous ne pouvez pas annuler cette rendez-vous")
        # else:
        self.message_post(body="Votre rendez-vous du {} est annulée".format(self.date_start),
						  subject="Retour demande de rendez-vous",
						  # partner_ids=self.customer_id.ids
						  )

        message = '''Votre rendez-vous du {} est annulée'''.format(self.date_start,
                                                                   ),
        title = "Rendez-vous"
        send_notif(title, message, 3, self.customer_id.id)
        curs, connex = dbconnex(self)

        rdv_id = self.rdv_id
        curs.execute("""UPDATE public."viseoApi_rendezvous"
						SET
						status_rendez_vous_id = %s
						WHERE id = %s;
						""", (3, rdv_id))
        connex.commit()
        connex.close()
        return self.write({'state': 'canceled', 'color': 1})

    def _check_validator(self):
        current_user = self.env.user.id
        responsables = self.responsable_atelier_id.ids
        if current_user == responsables or self.env.user.id == 2:
            self.validator = True
        else:
            self.validator = False

    @api.onchange('date_start')
    def _onchange_start_date(self):
        if self.date_start and self.duration:
            if self.duration_unit == 'day':
                self.date_stop = self.date_start + timedelta(days=self.duration)
            elif self.duration_unit == 'hour':
                self.date_stop = self.date_start + timedelta(hours=self.duration)
            elif self.duration_unit == 'minute':
                self.date_stop = self.date_start + timedelta(minutes=self.duration)

    @api.onchange('duration_unit')
    def _onchange_duration_unit(self):
        if self.duration > 0:
            if self.date_start:
                if self.duration_unit == 'day':
                    self.date_stop = self.date_start + timedelta(days=self.duration)
                elif self.duration_unit == 'hour':
                    self.date_stop = self.date_start + timedelta(hours=self.duration)
                elif self.duration_unit == 'minute':
                    self.date_stop = self.date_start + timedelta(minutes=self.duration)
            else:
                self.date_start = datetime.now()
                if self.duration_unit == 'day':
                    self.date_stop = self.date_start + timedelta(days=self.duration)
                elif self.duration_unit == 'hour':
                    self.date_stop = self.date_start + timedelta(hours=self.duration)
                elif self.duration_unit == 'minute':
                    self.date_stop = self.date_start + timedelta(minutes=self.duration)

    @api.onchange('duration')
    def _onchange_duration(self):
        self._onchange_start_date()

    @api.onchange('date_stop')
    def _onchange_date_stop(self):
        if self.date_stop and self.date_start:
            diff_date = self.date_stop - self.date_start
            if self.duration_unit != 'hour':
                self.duration_unit == 'hour'
            self.duration = diff_date.total_seconds() / 3600

    @api.constrains('date_start', 'date_stop', 'pont_id', 'place_id')
    def _check_date(self):
        if self.emplacement == 'pl':
            domain = [
                ('date_start', '<', self.date_stop),
                ('date_stop', '>', self.date_start),
                ('atelier_id', '=', self.atelier_id.id),
                ('id', '!=', self.id),
                ('place_id', '=', self.place_id.id),
                ('place_id', '!=', False),
            ]

        if self.emplacement == 'pt':
            domain = [
                ('date_start', '<', self.date_stop),
                ('date_stop', '>', self.date_start),
                ('atelier_id', '=', self.atelier_id.id),
                ('id', '!=', self.id),
                ('pont_id', '=', self.pont_id.id),
                ('pont_id', '!=', False),
            ]

        if self.search_count(domain):
            appointments = self.search(domain)

            print()
            print(domain)
            print()
            print()
            for x in appointments:
                print(x.name)
                print(x.place_id.name)
                print(x.pont_id.name)
            print()
            print()
            print()

            raise ValidationError(
                _('Vous ne pouvez pas avoir deux rendez-vous qui se superposent à la même période sur un meme place ou pont'))

    def get_ganttt_data(self):
        rdv_id = self.env['viseo_rdv_mobile.viseo_rdv_mobile'].search([('atelier_id', '!=', False)])
        atelier_id = self.env['fleet.workshop.type'].search([('name', '!=', False)])
        datasets = []
        for x in atelier_id:
            data = {
                'redirection_Id': '',
                'id': '',
                'name': '',
                'actualStart': None,
                'actualEnd': None,
                'children': []
            }
            data["id"] = x.id
            data["name"] = x.name
            datasets.append(data)

            if x.pont_id:
                for y in x.pont_id:
                    children = {
                        'redirection_Id': '',
                        'id': '',
                        'name': '',
                        'actualStart': None,
                        'actualEnd': None,
                        'children': []
                    }
                    children["id"] = y.id
                    children["name"] = y.name
                    data['children'].append(children)

            if x.place_id:
                for y in x.place_id:
                    children = {
                        'redirection_Id': '',
                        'id': '',
                        'name': '',
                        'actualStart': None,
                        'actualEnd': None,
                        'children': []
                    }
                    children["id"] = y.id
                    children["name"] = y.name
                    data['children'].append(children)

        for x in rdv_id:

            if x.place_id:
                print(x.place_id.name)
            if x.pont_id:
                print(x.pont_id.name)
            print()
            for data in datasets:
                if data["id"] == x.atelier_id.id:
                    for place in data['children']:
                        if x.place_id:
                            if place["id"] == x.place_id.id and place["name"] == x.place_id.name:
                                place["actualStart"] = x.date_start
                                place["actualEnd"] = x.date_stop

                        if x.pont_id:
                            if place["id"] == x.pont_id.id and place["name"] == x.pont_id.name:
                                place["actualStart"] = x.date_start
                                place["actualEnd"] = x.date_stop

        print()
        pprint(datasets, sort_dicts=False)

        return datasets

    def repair_order(self):
        self.ensure_one()
        demand = self.id
        repair_id = self.env['fleet.vehicle.log.services'].sudo().search([('rdv_id.id', '=', demand)])
        if repair_id:
            return {
                'type': 'ir.actions.act_window',
                'name': 'RMA',
                'view_mode': 'form',
                'res_model': 'fleet.vehicle.log.services',
                'res_id': repair_id.id,
                'context': {'default_customer_id': self.customer_id,
                            'default_vehicle_id': self.customer_vehicle_id},
                'target': 'current'
            }
        else:
            return {
                'type': 'ir.actions.act_window',
                'name': 'RMA',
                'view_mode': 'form',
                'res_model': 'fleet.vehicle.log.services',

                'context': {'default_customer_id': self.customer_id.id,
                            'default_vehicle_id': self.customer_vehicle_id.id,
                            'default_rdv_id': self.id},
                'target': 'current'
            }

    def checkpanic(self):
        conn = psycopg2.connect(database='mobile_101023',
                                user='etech',
                                password='3Nyy22Bv',
                                host='10.68.132.2',
                                port='5432')

        cur = conn.cursor()
        query = """SELECT pa.id ,vp.menu_panique, pa.owner_id FROM "viseoApi_paniquealert" pa INNER JOIN "viseoApi_panique" vp on vp.id = pa.panique_id 
		 ORDER BY id DESC """
        cur.execute(query)
        rows = cur.fetchone()
        panique_id = 0

        if panique_id == rows[0]:
            print('pass')
        else:
            panique_id = rows[0]
            mess = []
            message = '''Votre alerte panique est belle et bien envoyé au responsable'''
            mess.append(message)
            send_notif('Panique', mess, 4, rows[2])

    def rdv_check(self):

        conn = psycopg2.connect(database='mobile_101023',
                                user='etech',
                                password='3Nyy22Bv',
                                host='10.68.132.2',
                                port='5432')

        cur = conn.cursor()
        cur.execute(f"""
			SELECT 
				rv.id, 
				rv.message, 
				rv.owner_id, 
				rv.vehicle_id, 
				drv.type_rendez_vous_id, 
				drv.date_rendez_vous, 
				drv.heure_rendez_vous
			FROM public."viseoApi_rendezvous" rv INNER JOIN public."viseoApi_daterendezvous" drv on rv.date_rendez_vous_id = drv.id
			
			
		""")

        rows = cur.fetchall()
        # print(rows)
        if rows:
            for row in rows:

                existing_record = self.env['viseo_rdv_mobile.viseo_rdv_mobile'].search([('rdv_id', '=', row[0])])
                if existing_record:
                    # print("pass")
                    continue

                type_rdv_id = self.env['type_rdv.type_rdv'].search([('id', '=', int(row[4]))])
                date_start = str(row[5]) + ' ' + str(row[6])
                print(date_start)
                date_format = "%Y-%m-%d %H:%M:%S"
                parsed_datetime = datetime.strptime(str(date_start), date_format)
                time_duration = timedelta(hours=1)
                gmt = timedelta(hours=3)
                parsed_datetime = parsed_datetime - gmt
                new_datetime = parsed_datetime + time_duration
                # print(atel.atel.id)
                record = {
                    'rdv_id': row[0],
                    'customer_id': row[2],
                    'note': row[1],
                    'atelier_id': type_rdv_id.atelier_id.id,
                    'place_id': False,
                    'pont_id': False,
                    'customer_vehicle_id': row[3],
                    'type_rendez_vous_id': row[4],
                    'date_start': str(parsed_datetime),
                    'date_stop': str(new_datetime),
                    'state': 'draft'
                }

                rdv = self.env['viseo_rdv_mobile.viseo_rdv_mobile'].create(record)
                if rdv:
                    rdv1, rdv2 = rdv.action_ask_rdv()
                    rdv2 = self.env['mail.mail'].sudo().search([('mail_message_id', '=', rdv2.id)])
                    mail = rdv2.send()
                    if mail:
                        print("Create success")
                else:
                    pass


class DatePropose(models.Model):
    _name = "date.propose"

    rdv_id = fields.Many2one('viseo_rdv_mobile.viseo_rdv_mobile', string="Ref rendez-vous")
    future_date = fields.Datetime('Proposition de date')
    note = fields.Text('Motif')

    def action_propose_date(self):
        self.rdv_id.message_post(
            body="""<p>Votre demande de rendez-vous du {} pour {} a été refusée</p>
					<p>Date proposée {} </p>""".format(self.rdv_id.date_start, self.rdv_id.type_rendez_vous_id.name,
                                                       self.future_date),
            subject="Demande de rendez-vous pour {}".format(self.rdv_id.type_rendez_vous_id),
            partner_ids=self.rdv_id.current_user.ids
        )
        self.rdv_id.write({'state': 'refused', 'color': 1})
        message = '''Votre demande de rendez-vous du {} pour {} a été refusée, nous proposons la date {}'''.format(
            self.rdv_id.date_start,
            self.rdv_id.type_rendez_vous_id.name,
            self.future_date),
        title = "Rendez-vous"
        send_notif(title, message, 3, self.customer_id.id)
        return


class ViseoTagRfidInherit(models.Model):
    _inherit = 'viseo.tag.rfid'

    name = fields.Char(string='Tag RFID')
    vehicle_id = fields.Many2one('fleet.vehicle', 'Vehicules')
    partner_id = fields.Many2one('res.partner', string="Propriétaire")


class AtelierVehicle(models.Model):
    _inherit = 'fleet.workshop.type'
    responsable_id = fields.Many2many('res.users', string='Responsable(s)')

    pont_id = fields.One2many('pont_vehicle.pont_vehicle', 'atelier_id', string="pont")
    place_id = fields.One2many('place_vehicle.place_vehicle', 'atelier_id', string="Place")
    type_rdv_id = fields.One2many('type_rdv.type_rdv', 'atelier_id', string="Type de rendez-vous")


class PlaceVehicle(models.Model):
    _name = 'place_vehicle.place_vehicle'

    name = fields.Char("Place")
    atelier_id = fields.Many2one('fleet.workshop.type', 'Atelier')


class PondVehicle(models.Model):
    _name = 'pont_vehicle.pont_vehicle'

    name = fields.Char("pont")
    atelier_id = fields.Many2one('fleet.workshop.type', 'Atelier')


class Typerdv(models.Model):
    _name = 'type_rdv.type_rdv'

    name = fields.Char("Type de rendez-vous")
    atelier_id = fields.Many2one('fleet.workshop.type', 'Atelier')
    sms = fields.Text("Sms pour client", size=170)

    @api.model
    def create(self, vals):
        res = super(Typerdv, self).create(vals)

        curs, connex = dbconnex(self)
        curs.execute("""
			INSERT INTO public."viseoApi_typerendezvous"(id, libelle) VALUES (%s, %s);
		""", (res.id, res.name))
        connex.commit()
        connex.close()
        print()
        print()
        print()
        print('database record created')
        print()
        print()
        print()
        print()

        return res

    def write(self, vals):
        curs, connex = dbconnex(self)
        res = super(Typerdv, self).write(vals)
        id = self.id
        name = self.name
        curs.execute("""
			UPDATE public."viseoApi_typerendezvous"
			SET id =%s, libelle =%s
			WHERE id = %s;
		""", (id, name, id))
        curs.execute("""SELECT * FROM public."viseoApi_typerendezvous";
		""")

        connex.commit()
        connex.close()

        print('database record modified')

        return res

    def unlink(self):
        res = super(Typerdv, self).unlink()
        id = self.id
        print(id)
        curs, connex = dbconnex(self)
        curs.execute("""
			DELETE FROM public."viseoApi_typerendezvous" WHERE id = %s
		""", (str(id)))
        connex.commit()
        connex.close()

        print('database record created')

        return res


class Repair_order_viseo(models.Model):
    _inherit = 'fleet.vehicle.log.services'

    rdv_id = fields.Many2one('viseo_rdv_mobile.viseo_rdv_mobile', 'Ref RDV')

    @api.model
    def create(self, vals):
        curs, connex = dbconnex(self)
        res = super(Repair_order_viseo, self).create(vals)

        curs.execute("""
					SELECT * FROM public."viseoApi_vehicle" where id=%s
		""", (self._context['default_vehicle_id'],))
        value = curs.fetchall()
        if value:

            if vals['rdv_id'] == False:
                print('No')
                # print(res.id,res.rdv_id.name ,res.name2, res.customer_id.id, res.vehicle_id.id)
                curs.execute("""
										INSERT INTO public."viseoApi_suivisav"(
						rendez_vous, owner_id, vehicle_id, reference,status_commande_reparation_id, status_contrat_id, status_devis_id, status_diagnostic_id, status_facturation_id, status_lavage_id,
						 status_liste_des_pieces_id, status_livraison_id, status_reception_id, status_rendez_vous_id, status_sav_id, status_termine_id,
						 reception, diagnostic, liste_des_pieces, devis, commande_reparation, contrat, facturation, lavage, livraison, termine,rma_id)
						VALUES ( %s, %s, %s, %s,%s, %s, %s, %s,%s, %s, %s, %s,%s, %s, %s, %s, %s, %s,%s, %s, %s, %s, %s,%s, %s, %s,%s
						);
									""", (
                    'Rendez-vous', vals['customer_id'], self._context['default_vehicle_id'], vals['name2'], 1, 3, 1, 1,
                    1, 1, 1, 1, 3, 3, 1, 1,
                    'Réception', 'Diagnostic', 'Pièces', 'Devis', 'Réparation', 'Contrat', 'Facturation', 'Lavage',
                    'Livraison',
                    'Terminé', res.id,))
            else:
                print(vals, self.customer_id, self.vehicle_id)

                curs.execute("""
							INSERT INTO public."viseoApi_suivisav"(
			rendez_vous, owner_id, vehicle_id, reference,status_commande_reparation_id, status_contrat_id, status_devis_id, status_diagnostic_id, status_facturation_id, status_lavage_id,
			 status_liste_des_pieces_id, status_livraison_id, status_reception_id, status_rendez_vous_id, status_sav_id, status_termine_id,
			 reception, diagnostic, liste_des_pieces, devis, commande_reparation, contrat, facturation, lavage, livraison, termine,type_sav,rma_id)
			VALUES ( %s, %s, %s, %s,%s, %s, %s, %s,%s, %s, %s, %s,%s, %s, %s, %s, %s, %s,%s, %s, %s, %s, %s,%s, %s, %s,%s,%s
			);
						""", (
                'Rendez-vous', vals['customer_id'], self._context['default_vehicle_id'], vals['name2'], 1, 3, 1, 1, 1,
                1, 1, 1, 1, 3, 1, 1, 'Réception', 'Diagnostic', 'Pièces', 'Devis', 'Réparation', 'Contrat',
                'Facturation', 'Lavage', 'Livraison', 'Terminé', self.rdv_id.type_rendez_vous_id.name, res.id))

            connex.commit()
            curs.close()
            connex.close()
            print('Ram created')

            return res
        else:
            return res

    def write(self, vals):
        curs, connex = dbconnex(self)
        res = super(Repair_order_viseo, self).write(vals)

        # try:
        if 'state_ro' in vals:
            if vals['state_ro'] == 'diag':
                curs.execute("""
					UPDATE public."viseoApi_suivisav"
		SET   status_reception_id=%s
		WHERE rma_id=%s;
				""", (3, self.id,))
            if vals['state_ro'] == 'repair':
                curs.execute("""
						UPDATE public."viseoApi_suivisav"
			SET   status_diagnostic_id=%s
			WHERE rma_id=%s;
					""", (3, self.id,))
            if vals['state_ro'] == 'trying':
                curs.execute("""
						UPDATE public."viseoApi_suivisav"
			SET   status_commande_reparation_id=%s
			WHERE rma_id=%s;
					""", (3, self.id,))
            if vals['state_ro'] == 'invoice':
                curs.execute("""
							UPDATE public."viseoApi_suivisav"
				SET   status_sav_id=%s
				WHERE rma_id=%s;
						""", (3, self.id,))
            if vals['state_ro'] == 'done':
                curs.execute("""
							UPDATE public."viseoApi_suivisav"
				SET   status_facturation_id=%s
				WHERE rma_id=%s;
						""", [3, self.id, ])
        if 'is_washed' in vals:
            if vals['is_washed']:
                curs.execute("""
								UPDATE public."viseoApi_suivisav"
					SET   status_lavage_id=%s
					WHERE rma_id=%s;
							""", (3, self.id,))
                print('True')
        if 'is_pieces_ok' in vals:
            if vals['is_pieces_ok'] == True:
                print('OK')
                curs.execute("""
									UPDATE public."viseoApi_suivisav"
						SET   status_liste_des_pieces_id=%s
						WHERE rma_id=%s;
								""", (3, self.id,))
                print('OK')
        if 'is_delivered' in vals:
            if vals['is_delivered'] == True:
                print('OK')
                curs.execute("""
									UPDATE public."viseoApi_suivisav"
						SET   status_livraison_id=%s, status_termine_id=%s
						WHERE rma_id=%s;
								""", (3, 3, self.id,))
                print('OK')
        # except:
        # 	print('Nothing')
        connex.commit()
        curs.close()
        connex.close()

        return res


class ConfirmSaleOrder(models.Model):
    _inherit = 'sale.order'

    def write(self, vals):
        curs, connex = dbconnex(self)
        res = super(ConfirmSaleOrder, self).write(vals)
        if self.repair_id:
            if 'state' in vals:
                if vals['state'] == 'sale':
                    curs.execute("""
										UPDATE public."viseoApi_suivisav"
										SET   status_devis_id=%s
										WHERE rma_id=%s;
										""", (3, self.repair_id.id,))
            connex.commit()
            curs.close()
            connex.close()

        return res


class Writevehicleapk(models.Model):
    _inherit = 'fleet.vehicle'

    def write(self, vals):
        curs, connex = dbconnex(self)

        res = super(Writevehicleapk, self).write(vals)
        print(vals)
        if 'driver_id' in vals:
            curs.execute("""SELECT * FROM public."viseoAccount_user" WHERE id = %s""", (vals['driver_id'],))
            account = curs.fetchall()
            if account:
                print('pass')

            else:
                partner = self.env['res.partner'].search([('id', '=', vals['driver_id'])])
                # query = """SELECT id, name, email, mobile FROM res_partner WHERE id=%s"""
                # curs.execute(query, (str(vals['driver_id']),))
                # rows = curs.fetchall()
                characters = string.ascii_letters + string.digits

                password = ''.join(random.choice(characters) for i in range(8))
                curs.execute("""INSERT INTO public."viseoAccount_user"(
					id,first_name,email,mobile,is_active,date_joined,"isAdmin", username, password)
					VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)
				 """, (
                partner.id, partner.name, partner.email, partner.mobile, True, datetime.now(), False, vals['driver_id'],
                password))
                connex.commit()
                contact = self.env['res.partner'].search([('id', '=', vals['driver_id'])])
                contact.write({
                    'login': str(vals['driver_id']),
                    'passwd': password,
                })

        curs.execute("""
					SELECT * FROM public."viseoApi_vehicle" where id = %s
		""", (self.id,))
        data = curs.fetchall()
        if data:
            if 'driver_id' in vals:

                curs.execute("""
										UPDATE public."viseoApi_vehicle"
										SET "number"=%s, model=%s, owner_id=%s
										WHERE id=%s;
								""", (self.license_plate, self.lot_id.name, vals['driver_id'], self.id))
            else:
                print('vehicle already here')
                curs.execute("""
						UPDATE public."viseoApi_vehicle"
						SET "number"=%s, model=%s, owner_id=%s
						WHERE id=%s;
				""", (self.license_plate, self.lot_id.name, self.driver_id.id, self.id))

        else:
            tag_id = self.env['fleet.vehicle.tag'].search([('name', '=', 'CLIENT')])
            if 'tag_ids' in vals:
                if tag_id.id == vals['tag_ids'] or self.tag_ids == tag_id.id:
                    curs.execute("""INSERT INTO public."viseoApi_vehicle"(
						id, number, model, owner_id)
						VALUES (%s, %s, %s, %s);
					""", (self.id, self.license_plate, self.lot_id.name, vals['driver_id'],))
                    print('Vehicle inserted')
                else:
                    print('passs')

        connex.commit()
        connex.close()

        return res

    def action_schedule_meeting2(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "res_model": "viseo_rdv_mobile.viseo_rdv_mobile",
            "name": "Mes rendez-vous",
            "views": [[False, "gantt"]],
            "context": {'default_customer_vehicle_id': self.id},
            "domain": [('customer_vehicle_id', '=', self.id)],
            "target": "current",
        }


class ValidateFacture(models.Model):
    _inherit = 'account.move'

    def insertData(self, query, value):
        curs, conn = dbconnex(self)

        curs.execute(query, value)

        record_id = curs.fetchone()
        print(record_id)

        conn.commit()
        return record_id

    def action_post(self):

        partner_id = self.partner_id

        if self.type == 'out_invoice':
            sale_order = self.env['sale.order'].search([('name','=',self.invoice_origin)])
            for car in sale_order.vehicle_ids:
                query = """INSERT INTO public."viseoApi_vehicle" (id, number, model,owner_id) VALUES (%s,%s,%s,%s) RETURNING id;"""
                value = (car.id, car.license_plate, car.model_id.name, partner_id.id)
                try:
                    result = self.insertData(query, value)
                    if result:
                        car.sudo().write({'driver_id': partner_id.id})
                except:
                    print('Error')
                        # stock = self.env['stock.picking'].search([('origin', '=', self.invoice_origin)])
                        # if stock:
                        #     vehicles = self.env['stock.move.line'].search([('picking_id', '=', stock.id)])
                        #     # for cars in vehicles: veh = sum(cars.product_uom_)
                        #     for vehicle in vehicles:
                        #         car = vehicle.lot_id.vehicle_id
                        #
                        #         if car:


        return super(ValidateFacture, self).action_post()




# class InvoiceVehicle(models.Model):
#     _inherit = 'sale.order'
#
#     def action_confirm(self):
#         veh_qty=0
#         # sale_order = self.env['sale.order'].search([('name', '=', self.invoice_origin)])
#         for sales in filter(lambda x: x.product_id.model_id, self.order_line): veh_qty += sales.product_uom_qty
#         if veh_qty >= 1:
#             if (self.vehicle_ids is None):
#                 raise ValidationError(('Ajouter le(s) VIN de véhicule(s) dans la vente'))
#             else:
#                 if veh_qty != len(self.vehicle_ids):
#                     raise ValidationError(('Ajuster le nombre de véhicule suivant la commande dans le vente'))
#         return super(InvoiceVehicle, self).action_confirm()