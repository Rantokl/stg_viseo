# -*- coding: utf-8 -*-
import psycopg2

from odoo import models, fields, api


class viseo_contact_apk(models.Model):
    _name = 'viseo.contact.apk'
    _description = "Contact pour l'application"

    name = fields.Char('Nom du responsable')
    service = fields.Char('Nom du service')
    emplacement = fields.Char('Lieu')
    contact = fields.Char('Contact')
    email = fields.Char('Email')
    website=fields.Char('Site web')
    type_contact = fields.Many2one('type.contact.apk', 'Type de contact')
    user_id = fields.Integer()

    @api.model
    def create(self,vals):
        connex = psycopg2.connect(database='mobile_101023',
                                user='etech',
                                password='3Nyy22Bv',
                                host='10.68.132.2',
                                port='5432')

        curs = connex.cursor()
        res = super(viseo_contact_apk, self).create(vals)

        curs.execute("""
        			INSERT INTO public."viseoApi_contact"(id, site_web,type_contact_id,email,mobile, name,seat ) VALUES (%s, %s,%s,%s,%s,%s,%s);
        		""", (res.id,res.website,res.type_contact.id,res.email,res.contact,res.name,res.emplacement))
        connex.commit()
        connex.close()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100


class TypeContact(models.Model):
    _name = 'type.contact.apk'
    _description = 'Type de contact'

    name = fields.Char('Type de contact')
