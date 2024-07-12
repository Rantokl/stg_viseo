# -*- coding: utf-8 -*-
import datetime

from odoo import models, fields, api


class ViseoExit(models.Model):
    _name = 'viseo.exit'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Bon de sortie'

    name = fields.Char(default="Nouveau")

    user_id = fields.Many2one('res.users', string="Démandeur", readonly=True,
                                   default=lambda self: self.env.user.id)
    chief_user_id = fields.Many2one('res.users', string="Responsable(s)")
    validator_id = fields.Many2one('res.users', string="Direction(s)")
    userback_id = fields.Many2one('res.users', string="Direction(s)")
    expediteur = fields.Many2one('res.partner', string="Expediteur")

    start = fields.Char('Emplacement')
    partner_id = fields.Many2one('res.partner', string="Transporteur")
    vehicle_id = fields.Many2one('fleet.vehicle', string="Véhicule N°")

    date = fields.Date('Date', default=datetime.datetime.today())
    receiver = fields.Many2one('res.partner', string="Destinataire")
    address = fields.Text('Adresse')
    motif = fields.Text('Motif')

    direction = fields.Boolean(default=False,compute="_compute_test_group")
    back = fields.Boolean(default=False,compute="_compute_test_group")
    back_date = fields.Date("Date retour")

    state = fields.Selection(string="Etat", selection=[
        ('new', 'Demande'),
        ('resp', 'Responsable'),
        ('dir', 'Direction'),
        ('liv', 'Livrable'),
        ('back', 'Retourné'),
        ('not_back',('Non retourné'))
    ], default="new", copy=False)

    status = fields.Selection(string="Type", selection=[
        ('transfert', 'Transfert'),
        ('back','A retourner'),

    ], default='transfert')


    product_id = fields.One2many('product.exit','exit_id')

    @api.model
    def create(self, sequence):
        sequence['name'] = self.env['ir.sequence'].next_by_code('viseo.exit') or '/'

        sequence['name'] = f"{sequence['name']}"

        return super(ViseoExit, self).create(sequence)


    @api.onchange('receiver')
    def _takeadress(self):
        if self.receiver:
            self.address = self.receiver.street + ' '+ self.receiver.street2

        # if self.product_id:
        #     for i in self.product_id:
        #         i.designation = i.article.designation

    @api.depends('user_id')
    def _compute_test_group(self):
        if self.env.user.has_group('viseo_exit.group_validation_direction_viseo_exit') or self.env.user.has_group('viseo_exit.group_validation_direction_viseo_exit_not_notified'):
            self.direction = True
        else:
            self.direction = False


    def checkReturn(self):
        today = datetime.date.today()
        records = self.search([
            ('status', '=', 'back'),
            ('state', '=', 'liv'),
            ('back_date', '=', today)
        ])

        if records:
            for record in records:
                record.write({
                    'state':'not_back'
                })

        # if self.status == 'back':
        #     self.back=True
        # else:
        #     self.back=False



    def request_exit(self):

        employee = self.env['hr.employee'].sudo().search([('user_id','=',self.env.user.id)])
        responsable = self.env['hr.employee'].sudo().search([('id','=',employee.parent_id.id)])

        self.write({'state': 'resp'})
        self.message_post(

            body='''Demande de bon de sortie de Mr(s) {} pour {}'''.format(self.expediteur.name,
                                                                               self.receiver.name),
            subject="Demande bon de sortie",
            partner_ids=responsable.user_id.partner_id.ids
        )

    def resp_validation(self):
        # employee = self.env['hr.employee'].sudo().search([('user_id', '=', self.env.user.id)])
        # responsable = self.env['hr.employee'].sudo().search([('id', '=', employee.parent_id)])
        directions = self.env['res.groups'].sudo().search([('name','=','Validation direction bon de sortie')])

        self.write({'state': 'dir',
                    'chief_user_id': self.env.user.id})
        self.message_post(

            body='''Demande de validation bon de sortie de Mr(s) {} pour {}'''.format(self.expediteur.name,
                                                                           self.receiver.name),
            subject="Demande de validation bon de sortie",
            partner_ids=directions.users.partner_id.ids

        )

    def dir_validation(self):
        # employee = self.env['hr.employee'].sudo().search([('user_id', '=', self.env.user.id)])
        # responsable = self.env['hr.employee'].sudo().search([('id', '=', employee.parent_id)])

        self.write({'state': 'liv',
                    'validator_id': self.env.user.id})
        self.message_post(

            body='''Bon de sortie validée de Mr(s) {} pour {}'''.format(self.expediteur.name,
                                                                           self.receiver.name),
            subject="Demande de validation bon de sortie",

        )

    def back_validation(self):
        self.write({'state': 'back',
                    'userback_id': self.env.user.id})
        self.message_post(

            body='''Bon de sortie retournée''',
            subject="Bon de sortie retournée",

        )
        

    def _print_report(self, data):
        return self.env.ref('viseo.action_report_viseo_exit').report_action(self, data=data)



#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100

class ProductExit(models.Model):
    _name="product.exit"
    _description = "Article à sortir"

    # article = fields.Many2one('viseo_product.exit', string="Article(s)")
    designation = fields.Char('Designation/Article')
    quantity = fields.Integer('Quantité')
    unity = fields.Char(string="Unité")
    obs = fields.Char('Observation')

    exit_id = fields.Many2one('viseo.exit', string="Ref Bon de sortie")


class unityProduct(models.Model):
    _name = "unity.product"

    name = fields.Char('unité')

class ViseoProductexit(models.Model):
    _name = "viseo_product.exit"

    name= fields.Char('Article(s)')
    designation = fields.Char('Designation')

