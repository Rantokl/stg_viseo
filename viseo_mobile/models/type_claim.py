# -*- coding: utf-8 -*-
from . import database
from odoo import models, fields, api
import psycopg2

class TypeReclamation(models.Model):

    _inherit = 'fleet.claim.type'
    resp_id = fields.Many2one('res.users', 'Responsable(s)', required=True)

    @api.model
    def create(self,vals):
        curs, connex = database.dbconnex(self)
        res = super(TypeReclamation, self).create(vals)
        curs.execute("""INSERT INTO public.viseoApi_typereclamation(
        	id, name)
        	VALUES (%s, %s);
         """, (res.id, res.name))
        connex.commit()
        connex.close()

        return res


    def write(self,vals):
        curs, connex = database.dbconnex(self)

        res = super(TypeReclamation, self).write(vals)
        id = self.id
        name = self.name
        curs.execute("""UPDATE
                        public.viseoApi_typereclamation
                        SET
                        id =%s, name =%s
                        WHERE id = %s;
                 """, (id, name,id))
        connex.commit()
        connex.close()
        return res

    def unlink(self):
        res = super(TypeReclamation,self).unlink()
        id = self.id
        print(id)
        curs, connex = database.dbconnex(self)
        curs.execute("""DELETE FROM public.viseoApi_typereclamation 
        WHERE id = %s
        """, (str(id)))
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


class ReclamationMobile(models.Model):
    _inherit = 'fleet.claim'
    claim_id = fields.Integer()
    customer_id = fields.Many2one('res.partner', string="Client", related="vehicle_id.driver_id")
    def check_claim(self):
        curs, connex = database.dbconnex(self)
        curs.execute("""SELECT * FROM public."viseoApi_reclamation"
        """)

        rows = curs.fetchall()
        for row in rows:
            existing_record = self.env['fleet.claim'].search([('claim_id','=',row[0])])
            if existing_record:
                continue

            records = {
                'claim_id': row[0],
                'customer_id': row[2],
                'claim': row[1],
                'vehicle_id': row[4],
                'claim_type': row[3]
            }
            customer_id = self.env['res.partner'].sudo().search([('id','=',row[2])])
            resp_id = self.env['res.users'].sudo().search([('id', '=', 7612)])
            self.env['fleet.claim'].create(records)
            mails = dict(email_from=customer_id.email,
                         partner_ids= resp_id.partner_id.ids,
                         subject= "Reclamation sur {}".format(row[3]),
                         body=row[1],
                         )

            mail = self.env['mail.message'].create(mails)
            print(mail)
            rdv2 = self.env['mail.mail'].sudo().search([('mail_message_id', '=', mail.id)])
            print(rdv2)
            mail1 = rdv2.send()



