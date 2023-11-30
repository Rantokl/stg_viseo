# -*- coding: utf-8 -*-
import psycopg2
from odoo import models, fields, api


class Reclamation(models.Model):
#     _name = 'viseo_mobile.viseo_mobile'
#     _description = 'viseo_mobile.viseo_mobile'
    _inherit = 'fleet.claim.type'
    @api.model
    def create(self,vals):

        res = super(Reclamation, self).create(vals)
        connex = psycopg2.connect(database='mobile_test',
                          user='postgres',
                          password='1234',
                          host='10.68.132.2',
                          port='5432')
        curs = connex.cursor()
        curs.execute("""INSERT INTO public."viseo_api_typereclamation"(
            	id,name)
            	VALUES (%s,%s)
             """, (res.id, res.name))
        connex.commit()
        connex.close()
        return res

#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
