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
        curs.execute("""INSERT INTO public."viseoApi_typereclamation"(
        	id, reclamation)
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
                        public."viseoApi_typereclamation"
                        SET
                        id =%s, reclamation =%s
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
        curs.execute("""DELETE FROM public."viseoApi_typereclamation" 
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
            to_suscribe = self.env['res.groups'].search([('name', '=', 'Réception reclamation')])

            devis = self.env['fleet.claim'].create(records)

            ask = devis.message_post(
                body='''Demande de réclamation de Mr(s) {} pour {}'''.format(devis.customer_id.name, devis.claim_type.name),
                subject='Demande de réclamation de Mr(s) {}'.format(devis.customer_id.name),
                partner_ids=to_suscribe.users.partner_id.ids)
            devis.message_subscribe(partner_ids=to_suscribe.users.partner_id.ids)
            rdv2 = self.env['mail.mail'].sudo().search([('mail_message_id', '=', ask.id)])
            mail = rdv2.send()
            if devis and mail:
                print('records create succeffully....')





