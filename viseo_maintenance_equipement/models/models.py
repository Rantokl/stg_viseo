# -*- coding: utf-8 -*-

from odoo import models, fields, api


# class viseo_maintenance_equipement(models.Model):
#     _name = 'viseo.maintenance.equipement'
#     _description = 'Maintenance des equipements internes'
#
#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()


class EquipementBT(models.Model):
    _name = 'equipement.bike.tools'
    _description = 'Equipement interne'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name= fields.Char()
    model = fields.Many2one('model.equipment', string="Modèle")
    owner = fields.Many2one('res.partner', string="Proprietaire")
    date_start = fields.Date('Date mise en service')
    cost_reported = fields.Float('Coût réportée(s)')
    emplacement= fields.Many2one('viseo.vehicle.location')
    address = fields.Char('Adresse')
    serial_number = fields.Char('Numéro de série')
    year_model = fields.Char('Année du modèle')
    partner_id = fields.Many2one('res.partner', string="Fournisseur")
    expire_date = fields.Date("Date d'expiration de garantie" )
    meeting_count = fields.Integer()
    contract_count = fields.Integer()
    fuel_logs_count= fields.Integer()
    cost_total = fields.Integer()
    maintenance_count = fields.Integer()


class ModelEquipement(models.Model):
    _name = 'model.equipment'

    name = fields.Char()


class MaintenanceBT(models.Model):
    _name = 'maintenance.bike.tools'

    name=fields.Char()
    customer_id = fields.Many2one('res.partner', string="client")
    tools_id = fields.Many2one('equipement.bike.tools')

    address = fields.Char('Adresse')
    previous_date = fields.Date('Date prévisionnelle')
    end_date= fields.Date('Date fin')
    invoice_date = fields.Date('Date de  facturation')
