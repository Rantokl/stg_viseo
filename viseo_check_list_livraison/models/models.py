# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Check_list_livraison(models.Model):
     _name = 'viseo_check.list_livraison'
     _inherit = ['mail.thread', 'mail.activity.mixin']
     _description = 'Check list livraison'

    
     name = fields.Char(default='Nouveau')
     oil_motor = fields.Boolean('Huile Moteur')
     liquid_refroid = fields.Boolean('Liquide de refroidissement')
     battery = fields.Boolean('Niveau/Charge batterie')
     brake_liquid = fields.Boolean('Liquide de freins')
     liquid_direction = fields.Boolean('Liquide de directions assistée')
     liquid_lave_glace = fields.Boolean('Liquide de lave-glace AV/AR')

     code = fields.Boolean('Code / Phare / Veuilleuse')
     clignotant = fields.Boolean('Clignotants / Feux de détresse')
     led_immatricul = fields.Boolean('Feu AR plaque immatriculation')
     led_recul = fields.Boolean('Feux de recul / anti brouillard AV/AR')
     sonor = fields.Boolean('Avertisseur sonore')

     essui_gl = fields.Boolean('Balai essuie-glace AV/AR')
     pare_brise = fields.Boolean('Etat pare-brise')
     lunette = fields.Boolean('Lunette AR')
     retro = fields.Boolean('Rétroviseurs')

     brake_plaque = fields.Boolean('Plaquettes de frein')
     circuit_frein = fields.Boolean('Circuit de freinage')
     flexible_frein = fields.Boolean('Flexibles de freins')
     hand_brake = fields.Boolean('Câble frein à main')
     brake_disk = fields.Boolean('Disque de freins / Tambours')
     etrier = fields.Boolean('Etriers et cylindre de roues')
     brake_service= fields.Boolean('Pédale de frein de service')
     brake_station = fields.Boolean('Frein de stationnement')

     wheel = fields.Boolean('Volant de direction')
     cremaillere = fields.Boolean('Crémaillère ou boîtier de direction')
     biellette = fields.Boolean('Biellettes / Rotules / relais')
     assistance_direction = fields.Boolean('Système assistance de direction')

     amort = fields.Boolean('Amortisseurs AV/AR')
     barre = fields.Boolean('Barres stabilisatrices AV/AR')
     trainV = fields.Boolean('Demi train AV')
     trainR = fields.Boolean('Demi train AR / Essieu AR')
     jante = fields.Boolean('Jantes')
     pneum = fields.Boolean('Pneumatiques')
     roueS = fields.Boolean('Roues de secours')

     motor = fields.Boolean('Moteur')
     gearbox = fields.Boolean('Boîte de vitesses / Boîte de transfert')
     pont = fields.Boolean('Pont AV/AR')
     transmission = fields.Boolean('Transmission et accouplement')
     fuel_circuit = fields.Boolean('Circuit de carburant')
     tank = fields.Boolean('Réservoir carburant')
     echap = fields.Boolean('Système échappement')
     courroie = fields.Boolean('Ensemble de courroies')
     durite = fields.Boolean('Ensemble de durites')

     key_roue = fields.Boolean('Clé de roue / Cric / manivelle')
     gilet = fields.Boolean('Gilet / triangle')

     customer_vehicle_id = fields.Many2one('fleet.vehicle', 'Véhicule')
     customer_id = fields.Many2one('res.partner', string='Client' ,related='customer_vehicle_id.driver_id')

     @api.model
     def create(self, sequence):
          sequence['name'] = self.env['ir.sequence'].next_by_code('viseo_check.list_livraison') or '/'
          # place_pont = f"Place: {sequence.get('place_id')}" if sequence['place_id'] else f"Pont: {sequence.get('pont_id')}"
          sequence['name'] = f"{sequence['name']}"
          return super(Check_list_livraison, self).create(sequence)
     #     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100


class BoutonCheckList(models.Model):
     _inherit = 'fleet.vehicle'


     def open_check_list(self):

          self.ensure_one()
          vehicle_id = self.id
          check = self.env['viseo_check.list_livraison'].sudo().search([('customer_vehicle_id','=',vehicle_id)])
          if check:
               return {
               'type': 'ir.actions.act_window',
               'name': 'Check list livraison',
               'view_mode': 'form',
               'res_id':check.id,
               'res_model': 'viseo_check.list_livraison',
               'domain': [('customer_vehicle_id', '=', vehicle_id)],
               'context': {'default_customer_vehicle_id': self.id,
                           'default_customer_id':self.driver_id},
               }
          else:
               return {
                    'type': 'ir.actions.act_window',
                    'name': 'Check list livraison',
                    'view_mode': 'form',
                    'res_model': 'viseo_check.list_livraison',
                    'domain': [('customer_vehicle_id', '=', vehicle_id)],
                    'context': {'default_customer_vehicle_id': self.id,
                                'default_customer_id': self.driver_id},
                    'target': 'current'
               }
