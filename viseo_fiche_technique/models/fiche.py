from odoo import models, api, fields
from odoo.exceptions import UserError


class FicheTechnique(models.Model):
	_inherit = ['fleet.vehicle.model']


	vehicle_type_corrected = fields.Char(string="Type de véhicule")
	truck_type_corrected = fields.Char(string="Type de camion")
	fuel_type_corrected = fields.Char(string="Carburant")
	loudspeaker_corrected = fields.Integer(string="Nombre Haut Parleur")
	transmission_mode_corrected = fields.Char(string="Transmission Mode")
	jantes_corrected = fields.Char(string="Jantes")
	antibrouillard_corrected = fields.Char(string="Antibrouillards")
	power_steering_corrected = fields.Char(string="Direction Assistée")
	abs_corrected = fields.Char(string="ABS ")
	reversing_radar_corrected = fields.Char(string="Radar de recul")
	reversing_cam_corrected = fields.Char(string="Caméra de recul")
	anti_vol_corrected = fields.Char(string="Sytème de verouillage anti-vol")
	nombre_de_cylindre = fields.Integer(string="Nombre de cylindre")
	puissance_max = fields.Char(string="Puissance Max")
	freins_AV = fields.Char(string="Freins AV")
	freins_AR = fields.Char(string="Freins AR")
	rearview_electric_corrected = fields.Char(string="Rétroviseurs extérieurs couleur caisse éléctriques avec répetiteur")
	rearview_rabatable = fields.Char(string="Rétroviseurs exterieurs rabatable éléctriquement")
	degivreur_lunette = fields.Char(string="Dégivreur de lunette AR")
	essui_glace = fields.Char(string="Essuie-glace AR")
	galerie_monochrome = fields.Char(string="Galerie de toit monochrome")
	screen = fields.Char(string='Ecran 9" ')
	haut_parleur = fields.Char(string="Haut parleur")
	reglage_automatique_son = fields.Char(string="Réglage automatique du son par détéction de la vitesse")
	selerie = fields.Char(string="Selerie")
	reglage_siege_conducteur = fields.Char(string="Réglage - Siège conducteur ")
	reglage_siege_passager = fields.Char(string="Réglage siège passager")
	appui_tete = fields.Char(string="3 appuis-têtes des sièges arrières")
	siege_arriere_rabatable = fields.Char(string="Siège arrière rabattable 4/6")
	liseuse = fields.Char(string="Liseuse arrière")
	lampe_coffre = fields.Char(string="Lampe de coffre")
	etui_lunette = fields.Char(string="Etui à lunettes")
	accoudoir_goblet = fields.Char(string="Accoudoir central avant avec 2 porte goblets")
	accoudoir_arriere = fields.Char(string="Accoudoir central arrière")
	portiere_courtoisie = fields.Char(string="Portière avec lumière de courtoisie")
	retroviseur_manuel = fields.Char(string="Rétroviseur manuel anti-éblouissement")
	toit_electrique = fields.Char(string="Toit ouvrant électrique")
	toit_panoramique = fields.Char(string="Toit ouvrant panoramique")
	#image
	
	image_vehicle_corrected = fields.Binary(
		string='Image Véhicule',
	)
	image_logo_corrected = fields.Binary(
		string='Image Logo',
	)
	image_face_corrected = fields.Binary(
		string='Vue de Face ',
	)
	image_profil_corrected = fields.Binary(
		string='Vue de profil ',
	)
	image_inside_corrected = fields.Binary(
		string='Vue Intérieur ',
	)

	def get_report_action(self):
		active_ids = self.env.context.get('active_ids', [])
		if active_ids:
			# Récupérer les enregistrements des véhicules sélectionnés
			selected_vehicles = self.env['fleet.vehicle.model'].browse(active_ids)
			selected_company =self.env['res.company'].browse(self._context.get('allowed_company_ids'))
			if len(selected_vehicles) > 4:
				raise UserError("Nombre maximal de véhicules séléctionnés : 4")
			if len(selected_vehicles) < 2:
				raise UserError("Nombre minimal de véhicules séléctionnés : 2")

			# Afficher les IDs des véhicules sélectionnés dans la console pour vérification
			print(
				f"Selected Vehicles: {selected_vehicles} £££££££££££££££££££££££££££££££££££££££££££££££££££££££££££££££££££££")
			print(f"company id:{selected_company}) $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
			if len(selected_company) != 1:
				return {
					'type': 'ir.actions.report',
					'report_name': 'viseo_fiche_technique.report_vehicle_comparison_new',
					'model': 'fleet.vehicle.model',
					'report_type': 'qweb-pdf',
					'context': {'active_ids': active_ids},
				}
			else:
				if int(selected_company.id) == 1:
					return {
						'type': 'ir.actions.report',
						'report_name': 'viseo_fiche_technique.report_vehicle_comparison_ocentrade',
						'model': 'fleet.vehicle.model',
						'report_type': 'qweb-pdf',
						'context': {'active_ids': active_ids},
					}
				else:
					return {
						'type': 'ir.actions.report',
						'report_name': 'viseo_fiche_technique.report_vehicle_comparison_continental_auto',
						'model': 'fleet.vehicle.model',
						'report_type': 'qweb-pdf',
						'context': {'active_ids': active_ids},
					}







	
