# -*- coding: utf-8 -*-
import datetime
import random
import string

import psycopg2

from odoo import models, fields, api


class login_sav(models.Model):
    # _name = 'login.sav'
#     _description = 'login_sav.login_sav'
    _inherit = 'res.partner'
    login = fields.Char('Login')
    passwd = fields.Char('Password')
    contact_apk = fields.Boolean(string='Contact')

    @api.model
    def create(self, vals):
        res = super(login_sav, self).create(vals)
        connex = psycopg2.connect(database='mobile_101023',
                                  user='etech',
                                  password='3Nyy22Bv',
                                  host='10.68.132.2',
                                  port='5432')

        curs = connex.cursor()

        characters = string.ascii_letters + string.digits
        password = ''.join(random.choice(characters) for i in range(8))
        res.login = res.id
        res.passwd = password
        # vals['name'] = 'Test'
        try:
            curs.execute("""INSERT INTO public."viseoAccount_user"(
                                id,first_name,email,mobile,is_active,date_joined,"isAdmin", username, password)
                                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)
                             """, (
                res.id, res.name, res.email, res.mobile, True, datetime.datetime.now(), False, res.id,
                password))
            connex.commit()
        except:
            print('Error')
        connex.close()
        return res
    def write(self, vals):
        connex = psycopg2.connect(database='mobile_101023',
                                  user='etech',
                                  password='3Nyy22Bv',
                                  host='10.68.132.2',
                                  port='5432')

        curs = connex.cursor()
        res = super(login_sav, self).write(vals)
        if 'contact_apk' in vals:
            if vals['contact_apk'] == True:
                curs.execute("""
                        SELECT * FROM public."viseoApi_contact" WHERE id = %s
                """, (self.id,))
                data = curs.fetchone()
                if data:
                    curs.execute("""
                            UPDATE public."viseoApi_contact"
                            SET id=%s, site_web=%s, created_at=%s, type_contact_id=%s, email=%s, mobile=%s, name=%s, seat=%s
                            WHERE id=%s;
                    """, (self.id,self.website,datetime.datetime.now(),3,self.email,self.mobile,self.name,self.street2, self.id))
                else:
                    curs.execute("""
                                        INSERT INTO public."viseoApi_contact"(id, site_web,type_contact_id,email,mobile, name,seat, created_at ) VALUES (%s, %s,%s,%s,%s,%s,%s, %s);
                                    """, (self.id, self.website, 3, self.email, self.mobile, self.name, self.street2, datetime.datetime.now(),))


            else :
                if vals['contact_apk']== False :
                    curs.execute("""
                                DELETE FROM public."viseoApi_contact" WHERE id = %s
                    """, (self.id,))

            connex.commit()
            connex.close()

            return res

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
